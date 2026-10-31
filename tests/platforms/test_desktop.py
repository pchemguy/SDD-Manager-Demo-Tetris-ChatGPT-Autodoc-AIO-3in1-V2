"""Real host/mapper code through injected Electron capabilities, distinct from native execution."""
import json,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def desktop(**values):
    run=subprocess.run(['node','tests/support/desktop-driver.cjs'],cwd=ROOT,input=json.dumps(values),text=True,capture_output=True,timeout=15)
    assert run.returncode==0,run.stderr
    return json.loads(run.stdout)
@pytest.mark.parametrize('url',['https://tetris.invalid/index.html?ghost=hide#stay','https://tetris.invalid/runtime/sql-wasm.wasm'])
def test_fixed_local_resource_mapping(url):
    value=desktop(op='map',url=url);assert value['status']==200 and value['file']
@pytest.mark.parametrize('url',['app://tetris/index.html','https://example.invalid/index.html','file:///etc/passwd','https://evil.invalid/index.html','https://user@tetris.invalid/index.html','https://tetris.invalid:99/index.html','https://tetris.invalid/../index.html','https://tetris.invalid/%2e%2e/index.html','https://tetris.invalid/%252e%252e/index.html','https://tetris.invalid/assets%2f..%2findex.html','https://tetris.invalid/%ZZ','https://tetris.invalid/unknown.js','https://tetris.invalid/assets\\main.js'])
def test_traversal_foreign_origins_and_nonwhitelisted_paths_rejected(url):
    assert desktop(op='map',url=url)['status']!=200
@pytest.mark.parametrize('method',['POST','PUT','DELETE'])
def test_unexpected_methods_rejected(method):
    assert desktop(op='map',url='https://tetris.invalid/index.html',method=method)['status']==405

def test_isolated_persistent_host_protocol_mime_lifecycle_and_download_policy():
    r=desktop(op='policy',args=['--game-url=https://tetris.invalid/index.html?ghost=hide#stay'])
    assert 'schemes' not in r['calls'] and r['calls'].index('ready')<r['calls'].index('handler:https')
    assert 'persist:tetris' in r['calls'] and 'handler:https' in r['calls']
    prefs=r['windowOptions']['webPreferences'];assert prefs['partition']=='persist:tetris' and prefs['sandbox'] and prefs['contextIsolation'] and not prefs['nodeIntegration'] and prefs['webSecurity'] and not prefs['webviewTag'] and 'preload' not in prefs
    assert r['url']=='https://tetris.invalid/index.html?ghost=hide#stay'
    assert r['response']['status']==200 and r['response']['body']=='game'
    assert "'wasm-unsafe-eval'" in r['response']['csp'] and "'unsafe-eval'" not in r['response']['csp']
    assert r['wasm']==dict(status=200,type='application/wasm') and r['head']==''
    assert r['remotePrevented'] and not r['localPrevented'] and r['open']=={'action':'deny'} and not r['permissionAllowed']
    assert r['badDownloadPrevented'] and r['downloadOptions']['defaultPath'].endswith('tetris-save.sqlite')
    assert r['flush']==1 and r['quit']==1
    assert len(r['scripts'])==3 and len(set(r['scripts']))==1 and 'dispatchEvent' in r['scripts'][0] and 'blur' in r['scripts'][0]

def test_unsupported_launch_url_cannot_open_remote_content():
    assert desktop(op='startup',args=['--game-url=https://example.invalid/'])=='https://tetris.invalid/index.html'
