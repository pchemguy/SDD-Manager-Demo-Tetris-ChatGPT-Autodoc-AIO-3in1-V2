"""Independent artifact gates reject invalid manifests and stale/missing runtime resources."""
import importlib.util,json,zipfile,struct
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('verify_extensions',R/'scripts/verify_packages.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
def files(family):
 result={p.relative_to(R/f'dist/extensions/{family}').as_posix():p.read_bytes() for p in (R/f'dist/extensions/{family}').rglob('*') if p.is_file()}
 for name in ['THIRD-PARTY-NOTICES.md','LICENSE','FILES.md']:result[name]=(R/name).read_bytes()
 result['INSTALL.md']=(R/'platforms/extensions/INSTALL.md').read_bytes();result['build-info.json']=b'{}';return result
def check(tmp_path,family,data):
 path=tmp_path/'extension.zip'
 with zipfile.ZipFile(path,'w') as z:
  for key,value in data.items():z.writestr(key,value)
 with zipfile.ZipFile(path) as z:module.verify_extension(z,family,json.loads((R/'package.json').read_text())['version'])
@pytest.mark.parametrize('family',['chromium','firefox'])
def test_accept_complete_extension(tmp_path,family):check(tmp_path,family,files(family))
@pytest.mark.parametrize('fault',['missing-wasm','wrong-wasm','missing-schema','missing-background','remote-panel','site-permission','wrong-version','wrong-floor','bad-icon','test-bridge'])
def test_reject_wrong_extension_resource_or_policy(tmp_path,fault):
 data=files('chromium');manifest=json.loads(data['manifest.json'])
 if fault=='missing-wasm':del data['runtime/sql-wasm.wasm']
 if fault=='wrong-wasm':data['runtime/sql-wasm.wasm']=b'corrupt'
 if fault=='missing-schema':del data['schemas/tetris-save.schema.json']
 if fault=='missing-background':del data['background.js']
 if fault=='remote-panel':data['panel.html']=b'<script src="https://example.invalid/remote.js"></script>'
 if fault=='site-permission':manifest['host_permissions']=['<all_urls>']
 if fault=='wrong-version':manifest['version']='0.0.0'
 if fault=='wrong-floor':manifest['minimum_chrome_version']='100'
 if fault=='bad-icon':data['icons/tetris-16.png']=b'wrong'
 if fault=='test-bridge':data['harness-bridge.js']=b'fake'
 data['manifest.json']=json.dumps(manifest).encode()
 with pytest.raises(ValueError):check(tmp_path,'chromium',data)
