"""Real host/mapper code through injected Electron capabilities, distinct from native execution."""
import json,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def desktop(**values):
    run=subprocess.run(['node','tests/support/desktop-driver.cjs'],cwd=ROOT,input=json.dumps(values),text=True,capture_output=True,timeout=15)
    assert run.returncode==0,run.stderr
    return json.loads(run.stdout)
@pytest.mark.parametrize('url',['app://tetris/index.html?ghost=hide#stay','app://tetris/runtime/sql-wasm.wasm'])
def test_fixed_local_resource_mapping(url):
    value=desktop(op='map',url=url);assert value['status']==200 and value['file']
@pytest.mark.parametrize('url',['https://example.invalid/index.html','file:///etc/passwd','app://evil/index.html','app://user@tetris/index.html','app://tetris:99/index.html','app://tetris/../index.html','app://tetris/%2e%2e/index.html','app://tetris/%252e%252e/index.html','app://tetris/assets%2f..%2findex.html','app://tetris/%ZZ','app://tetris/unknown.js','app://tetris/assets\\main.js'])
def test_traversal_foreign_origins_and_nonwhitelisted_paths_rejected(url):
    assert desktop(op='map',url=url)['status']!=200
@pytest.mark.parametrize('method',['POST','PUT','DELETE'])
def test_unexpected_methods_rejected(method):
    assert desktop(op='map',url='app://tetris/index.html',method=method)['status']==405

def test_isolated_persistent_host_protocol_mime_lifecycle_and_download_policy():
    r=desktop(op='policy',args=['--game-url=app://tetris/index.html?ghost=hide#stay'])
    assert r['calls'][0]=='schemes' and r['calls'].index('ready')>r['calls'].index('schemes')
    privileges=r['calls'][1][0]['privileges'];assert privileges['standard'] and privileges['secure'] and privileges['supportFetchAPI'] and not privileges.get('bypassCSP',False)
    assert 'persist:tetris' in r['calls'] and 'handler:app' in r['calls']
    prefs=r['windowOptions']['webPreferences'];assert prefs['partition']=='persist:tetris' and prefs['sandbox'] and prefs['contextIsolation'] and not prefs['nodeIntegration'] and prefs['webSecurity'] and not prefs['webviewTag'] and 'preload' not in prefs
    assert r['url']=='app://tetris/index.html?ghost=hide#stay'
    assert r['response']['status']==200 and r['response']['body']=='game'
    assert "'wasm-unsafe-eval'" in r['response']['csp'] and "'unsafe-eval'" not in r['response']['csp']
    assert r['wasm']==dict(status=200,type='application/wasm') and r['head']==''
    assert r['remotePrevented'] and not r['localPrevented'] and r['open']=={'action':'deny'} and not r['permissionAllowed']
    assert r['badDownloadPrevented'] and r['downloadOptions']['defaultPath'].endswith('tetris-save.sqlite')
    assert r['flush']==1 and r['quit']==1

def test_unsupported_launch_url_cannot_open_remote_content():
    assert desktop(op='startup',args=['--game-url=https://example.invalid/'])=='app://tetris/index.html'
