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

def test_rejects_accidentally_bundled_view_harness(tmp_path):
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
