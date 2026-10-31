"""Shared panel-page geometry only; native sidebar lifecycle is tested separately."""
import itertools,os,json
from pathlib import Path
import pytest
from test_layout import text_overflow
from test_panels import select_panels
from test_files import restore
from test_file_validation import full_candidate
from playwright.sync_api import expect
@pytest.mark.parametrize('width',[280,360,480])
def test_sidebar_all_panels_resize_and_keyboard(page,width):
 page.evaluate("document.body.classList.add('sidebar')")
 page.set_viewport_size(dict(width=width,height=1000))
 restore(page,json.dumps(full_candidate()).encode());expect(page.locator('#notice')).to_contain_text('Restored')
 page.locator('#start').click();page.keyboard.press('p');expect(page.locator('#state')).to_have_text('Paused')
 before=page.locator('#board').get_attribute('aria-label')
 for scale in [14,28]:
  page.evaluate('(scale)=>document.documentElement.style.fontSize=scale+"px"',scale)
  for visible in itertools.product([False,True],repeat=3):
   select_panels(page,visible)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
   assert text_overflow(page)==[]
   boxes=page.evaluate("""()=>['.info','#board','#leaderboard','#settings','#help'].filter(s=>!document.querySelector(s).hidden).map(s=>{const r=document.querySelector(s).getBoundingClientRect();return {s,left:r.left,right:r.right,top:r.top,bottom:r.bottom};})""")
   for a,b in zip(boxes,boxes[1:]):assert a['bottom']<=b['top']+1
   assert all(b['left']>=0 and b['right']<=width for b in boxes)
   assert page.locator('#board').get_attribute('aria-label')==before
  select_panels(page,[True,True,True]);page.evaluate('window.scrollTo(0,0)')
  Path('test-results').mkdir(exist_ok=True);page.screenshot(path=f"test-results/sidebar-{os.environ.get('TETRIS_BROWSER','chromium')}-{width}-{scale}.png",full_page=True)
 assert page.locator('[data-gameplay]').count()==2
 page.locator('#board').focus();page.keyboard.press('p');expect(page.locator('#state')).to_have_text('Running');page.keyboard.press('p')
 page.set_viewport_size(dict(width=360 if width!=360 else 480,height=1000));expect(page.locator('#state')).to_have_text('Paused')
