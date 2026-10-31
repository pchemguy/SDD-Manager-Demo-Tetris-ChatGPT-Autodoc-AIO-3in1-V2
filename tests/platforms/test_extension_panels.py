"""Built panel/background integration with test transport; does not prove native sidebar UI."""
import functools,json,os,shutil,threading
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright,expect
import test_extension_native as scenarios
R=Path(__file__).resolve().parents[2]
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def end_headers(self):
  if self.path.split('?')[0].endswith('/panel.html'):self.send_header('Content-Security-Policy',"script-src 'self' 'wasm-unsafe-eval'; object-src 'self'")
  super().end_headers()
@pytest.fixture(params=['chromium','firefox'])
def extension_panel(request,tmp_path):
 family=request.param;root=tmp_path/'host';root.mkdir();shutil.copy(R/'tests/support/extension-host.html',root/'host.html');shutil.copytree(R/f'dist/{family}',root/family)
 (root/'harness-bridge.js').write_text("const api={storage:parent.chrome.storage,runtime:{connect:()=>parent.connectPanel(window)}};window.chrome=api;window.browser=api;")
 html=root/family/'panel.html';html.write_text(html.read_text().replace('<script type="module"','<script src="/harness-bridge.js"></script><script type="module"'))
 server=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(root)));thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
 try:
  with sync_playwright() as p:
   engine=os.environ.get('TETRIS_BROWSER','chromium');options={'headless':True,'timeout':10000}
   if engine=='firefox':options['env']={**os.environ,'MOZ_DISABLE_CONTENT_SANDBOX':'1'}
   browser=getattr(p,engine).launch(**options);context=browser.new_context()
   page=context.new_page();page.set_default_timeout(5000);errors=[];page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{server.server_port}/host.html?family={family}');page.wait_for_function('window.ready')
   class Panel:
    def __init__(self,name):self.name=name;self.frame=page.frame(name=name);self.keyboard=page.keyboard
    def locator(self,*args,**kw):return self.frame.locator(*args,**kw)
    def wait_for_timeout(self,ms):page.wait_for_timeout(ms)
    def expect_download(self):return page.expect_download()
    def close(self):page.evaluate('(name)=>document.querySelector(`iframe[name="${name}"]`).remove()',self.name)
    def goto(self,url):self.frame.goto(url)
   def panel(search=''):
    name=page.evaluate('(search)=>window.openPanel(search)',search)
    try:page.frame_locator(f'iframe[name="{name}"]').locator('#board').wait_for()
    except Exception as e:raise AssertionError({'body':page.frame(name=name).locator('body').inner_text(),'errors':errors}) from e
    return Panel(name)
   yield context,page,panel
   assert errors==[],errors
   context.close();browser.close()
 finally:server.shutdown();server.server_close();thread.join(timeout=5)
def test_panel_ownership_reopen_settings(extension_panel):scenarios.test_real_extension_ownership_reopen_and_local_settings(extension_panel)
def test_panel_validated_files(extension_panel,tmp_path):scenarios.test_real_extension_both_file_formats_and_invalid_nonmutation(extension_panel,tmp_path)
def test_storage_failure_pauses_and_explains(extension_panel):
 _,host,panel=extension_panel;p=panel();p.locator('#start').click();host.evaluate('window.failure=true');p.keyboard.press('ArrowLeft');expect(p.locator('#state')).to_have_text('Paused');expect(p.locator('#host-notice')).to_contain_text('storage unavailable');expect(p.locator('#start')).to_be_disabled()

def test_background_recreation_recovers_paused_without_away_gravity(extension_panel):
 _,host,panel=extension_panel;p=panel('?ghost=dynamic');p.locator('#start').click();p.keyboard.press('Enter');p.keyboard.press('p');scenarios.wait_saved(p,host,'session','session',lambda s:s and s['session']['game']['status']=='paused')
 before=scenarios.saved(host,'session','session')['session'];host.reload();host.wait_for_function('window.ready');p2=panel();expect(p2.locator('#state')).to_have_text('Paused');expect(p2.locator('#setting-ghost')).to_have_value('dynamic');assert scenarios.saved(host,'session','session')['session']==before
 p2.close();host.wait_for_timeout(50);host.evaluate('sessionStorage.clear()');host.reload();host.wait_for_function('window.ready');fresh=panel();expect(fresh.locator('#state')).to_have_text('Ready');expect(fresh.locator('#setting-ghost')).to_have_value('dynamic');expect(fresh.locator('#leaderboard-body tr')).to_have_count(0)
