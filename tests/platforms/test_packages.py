"""Stable asset names reject an apparently complete versioned-name inventory."""
import importlib.util
from pathlib import Path
import pytest
spec = importlib.util.spec_from_file_location('verify_packages', Path(__file__).resolve().parents[2]/'scripts/verify_packages.py')
module = importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
@pytest.mark.parametrize('names', [
    ['tetris-browser-0.1.0.zip', 'SHA256SUMS.txt'],
    ['tetris-browser.zip', 'tetris-browser.zip', 'SHA256SUMS.txt'],
    ['tetris-browser.zip'],
])
def test_reject_names(names):
    with pytest.raises(ValueError):
        module.verify_names(names, ['tetris-browser.zip', 'SHA256SUMS.txt'])
def test_accept_stable_names():
    module.verify_names(['tetris-browser.zip', 'SHA256SUMS.txt'], ['tetris-browser.zip', 'SHA256SUMS.txt'])

def test_rejects_accidentally_bundled_view_harness(tmp_path,monkeypatch):
    monkeypatch.setattr(module,'expected_names',lambda:['tetris-browser.zip','SHA256SUMS.txt'])
    import json
    import hashlib
    import zipfile
    version=json.loads((module.ROOT/'package.json').read_text())['version']
    files={'index.html':'<!doctype html><title>Fixture</title>','INSTALL.md':'Install','THIRD-PARTY-NOTICES.md':'Notices','LICENSE':'MIT','build-info.json':json.dumps({'version':version,'sourceCommit':'0'*40,'dirty':False}),'tests/support/render.html':'test-only fixture'}
    path=tmp_path/'tetris-browser.zip'
    with zipfile.ZipFile(path,'w') as z:
        for name,content in files.items():z.writestr(name,content)
    (tmp_path/'SHA256SUMS.txt').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  tetris-browser.zip\n')
    with pytest.raises(ValueError,match='Development'):
        module.verify(tmp_path)

@pytest.mark.parametrize('fault',['missing-wasm','bad-wasm','bad-schema'])
def test_reject_incomplete_or_wrong_file_runtime(tmp_path,fault,monkeypatch):
    monkeypatch.setattr(module,'expected_names',lambda:['tetris-browser.zip','SHA256SUMS.txt'])
    import json,hashlib,zipfile
    files={p.relative_to(module.ROOT/'dist/browser').as_posix():p.read_bytes() for p in (module.ROOT/'dist/browser').rglob('*') if p.is_file()}
    for name in ['INSTALL.md','THIRD-PARTY-NOTICES.md','LICENSE']:files[name]=(module.ROOT/name).read_bytes()
    files['build-info.json']=json.dumps(dict(version=json.loads((module.ROOT/'package.json').read_text())['version'],sourceCommit='0'*40,dirty=False)).encode()
    if fault=='missing-wasm':files.pop('runtime/sql-wasm.wasm')
    if fault=='bad-wasm':files['runtime/sql-wasm.wasm']=b'corrupt'
    if fault=='bad-schema':files['schemas/tetris-save.schema.json']=b'{}'
    path=tmp_path/'tetris-browser.zip'
    with zipfile.ZipFile(path,'w') as z:
        for name,data in files.items():z.writestr(name,data)
    (tmp_path/'SHA256SUMS.txt').write_text(hashlib.sha256(path.read_bytes()).hexdigest()+'  tetris-browser.zip\n')
    with pytest.raises(ValueError,match='runtime|Wasm|schema'):module.verify(tmp_path)

def pe_header(machine=0x8664,magic=0x20b):
    import struct
    data=bytearray(512);data[:2]=b'MZ';struct.pack_into('<I',data,0x3c,0x80);data[0x80:0x84]=b'PE\0\0';struct.pack_into('<HH',data,0x84,machine,1);struct.pack_into('<H',data,0x94,240);struct.pack_into('<H',data,0x96,2);struct.pack_into('<H',data,0x98,magic);return bytes(data)

def test_accepts_windows_x64_pe_header():
    module.verify_pe(pe_header())

@pytest.mark.parametrize('data',[b'',b'not exe',pe_header(0x14c),pe_header(magic=0x10b),b'MZ'+b'\0'*60],ids=['empty','not-pe','x86','pe32','truncated'])
def test_rejects_invalid_or_wrong_architecture_pe(data):
    with pytest.raises(ValueError):module.verify_pe(data)
