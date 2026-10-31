"""Actual isolated unpacked Chromium extension, not an HTTP/mock host."""
import json,os,tempfile
from pathlib import Path
import pytest
from playwright.sync_api import sync_playwright,expect
R=Path(__file__).resolve().parents[2]
@pytest.fixture
def native_extension():
 binary=os.environ.get('TETRIS_CHROMIUM_BINARY')
 if not binary:pytest.skip('Set TETRIS_CHROMIUM_BINARY for real unpacked extension checks')
 with tempfile.TemporaryDirectory(prefix='tetris-extension-') as profile,sync_playwright() as p:
  c=p.chromium.launch_persistent_context(profile,executable_path=binary,headless=True,args=['--no-sandbox','--disable-extensions-except='+str(R/'dist/extensions/chromium'),'--load-extension='+str(R/'dist/extensions/chromium')],timeout=15000)
  try:
   sw=c.service_workers[0] if c.service_workers else c.wait_for_event('serviceworker',timeout=10000)
   base=sw.url.rsplit('/',1)[0];errors=[]
   def panel(search=''):
    page=c.new_page();page.set_default_timeout(5000);page.on('pageerror',lambda e:errors.append(str(e)));page.goto(base+'/panel.html'+search,timeout=15000);page.wait_for_selector('#board');return page
   yield c,sw,panel
   assert errors==[],errors
  finally:c.close()
def saved(sw,area,key):return sw.evaluate('async ([area,key])=>(await chrome.storage[area].get(key))[key]',[area,key])
def wait_saved(page,sw,area,key,predicate):
 for _ in range(100):
  value=saved(sw,area,key)
  if predicate(value):return value
  page.wait_for_timeout(25)
 raise AssertionError(f'Unconfirmed {area}.{key}: {value}')
def test_real_extension_ownership_reopen_and_local_settings(native_extension):
 c,sw,panel=native_extension;p=panel('?ghost=dynamic&hardDropLock=immediate')
 wait_saved(p,sw,'local','settings',lambda s:s and s['settings']['ghost']=='dynamic')
 p.locator('#start').click();p.keyboard.press('Enter');p.keyboard.press('p');expect(p.locator('#state')).to_have_text('Paused')
 old=wait_saved(p,sw,'session','session',lambda s:s and s['session']['game']['status']=='paused')['session']
 secondary=panel();expect(secondary.locator('#setting-ghost')).to_have_value('dynamic');expect(secondary.locator('#start')).to_be_disabled();expect(secondary.locator('#state')).to_have_text('Paused')
 secondary.locator('#pause').click();expect(secondary.locator('#state')).to_have_text('Running');expect(p.locator('#start')).to_be_disabled();expect(p.locator('#state')).to_have_text('Paused')
 secondary.keyboard.press('p');expect(secondary.locator('#state')).to_have_text('Paused');snapshot=wait_saved(secondary,sw,'session','session',lambda s:s and s['session']['game']['status']=='paused')['session'];assert snapshot['game']['board']==old['game']['board']
 secondary.close();p.close();reopened=panel('?hold=invalid');expect(reopened.locator('#state')).to_have_text('Paused');expect(reopened.locator('#setting-ghost')).to_have_value('dynamic');expect(reopened.locator('#setting-hold')).to_have_value('on');assert saved(sw,'session','session')['session']==snapshot
 reopened.locator('#pause').click();expect(reopened.locator('#state')).to_have_text('Running');reopened.goto('about:blank')
 # Actual document teardown/disconnect must persist a paused recovery snapshot.
 p2=panel();expect(p2.locator('#state')).to_have_text('Paused');assert saved(sw,'local','settings')['settings']['ghost']=='dynamic'
def test_real_extension_both_file_formats_and_invalid_nonmutation(native_extension,tmp_path):
 c,sw,panel=native_extension;p=panel();p.locator('#start').click();p.keyboard.press('p');wait_saved(p,sw,'session','session',lambda s:s and s['session']['game']['status']=='paused')
 for format in ['json','sqlite']:
  p.locator('#file-format').select_option(format)
  with p.expect_download() as downloaded:p.locator('#save').click()
  path=tmp_path/('saved.'+format);downloaded.value.save_as(path)
  assert path.read_bytes().startswith(b'{' if format=='json' else b'SQLite format 3\0')
  p.locator('#restore-input').set_input_files(path);expect(p.locator('#notice')).to_contain_text('Restored')
 before=(saved(sw,'local','settings'),saved(sw,'session','session'))
 p.locator('#restore-input').set_input_files(dict(name='bad.json',mimeType='application/json',buffer=b'{"formatVersion":1}'));expect(p.locator('#notice')).to_contain_text('failed')
 assert (saved(sw,'local','settings'),saved(sw,'session','session'))==before
 candidate=json.loads((tmp_path/'saved.json').read_text());candidate['settings']['ghost']='hide';candidate['results']=[dict(id='00000000-0000-4000-8000-000000000001',score=987,timestamp='2026-01-01T00:00:00.000Z')]
 p.locator('#restore-input').set_input_files(dict(name='valid.json',mimeType='application/json',buffer=json.dumps(candidate).encode()));expect(p.locator('#notice')).to_contain_text('Restored');expect(p.locator('#leaderboard-body')).to_contain_text('987');expect(p.locator('#setting-ghost')).to_have_value('hide');wait_saved(p,sw,'session','session',lambda s:s and len(s['session']['results'])==1)
 assert 'results' not in json.dumps(saved(sw,'local','settings'))
