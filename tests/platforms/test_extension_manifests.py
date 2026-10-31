import json,subprocess
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
@pytest.mark.parametrize('family',['chromium','firefox'])
def test_manifest_local_sidebar_without_site_access(family):
 m=json.loads((R/f'platforms/extensions/{family}/manifest.json').read_text());assert m['manifest_version']==3
 assert set(m['permissions'])==({'storage','sidePanel'} if family=='chromium' else {'storage'})
 assert not any(k in m for k in ['host_permissions','content_scripts','externally_connectable'])
 assert m['content_security_policy']['extension_pages']=="script-src 'self' 'wasm-unsafe-eval'; object-src 'self'"
 if family=='chromium':assert m['minimum_chrome_version']=='116' and m['side_panel']['default_path']=='panel.html' and m['background']['service_worker']=='background.js'
 else:assert m['browser_specific_settings']['gecko']['strict_min_version']=='115.0' and m['sidebar_action']['default_panel']=='panel.html' and m['background']['scripts']==['background.js']
@pytest.mark.parametrize('family',['chromium','firefox'])
def test_explicit_family_and_direct_user_gesture_launch(family):
 p=subprocess.run(['node','.test-build/tests/support/extension-api-driver.js',family],cwd=R,text=True,capture_output=True,timeout=10)
 assert p.returncode==0,p.stderr
 q=json.loads(p.stdout);assert q['calls']==[family] and q['stored']=={'v':3}
