"""Real keyboard, lifecycle and Canvas checks for the playable classic loop."""
from playwright.sync_api import expect
from pathlib import Path
import os
def test_game_controls_keyboard_pause_and_canvas(page):
    expect(page.locator('#start')).to_have_text('Start')
    expect(page.locator('#pause')).to_have_text('Start')
    assert page.locator('[data-gameplay]').count() == 2
    page.locator('#start').click()
    expect(page.locator('#state')).to_have_text('Running')
    page.keyboard.press('ArrowDown')
    expect(page.locator('#score')).to_have_text('1')
    page.keyboard.press('p')
    expect(page.locator('#state')).to_have_text('Paused')
    score = page.locator('#score').inner_text()
    page.keyboard.press('ArrowDown')
    assert page.locator('#score').inner_text() == score
    page.locator('#pause').click()
    expect(page.locator('#state')).to_have_text('Running')
    assert page.locator('#board').evaluate('''(c)=>{const d=c.getContext("2d").getImageData(0,0,c.width,c.height).data;const colors=new Set(["53,198,215","237,201,79","164,129,237","105,201,124","238,113,123","99,142,232","239,170,89"]);let n=0;for(let i=0;i<d.length;i+=4)if(colors.has(`${d[i]},${d[i+1]},${d[i+2]}`))n++;return n>100;}''')
    Path('test-results').mkdir(exist_ok=True)
    page.screenshot(path='test-results/classic-'+os.environ.get('TETRIS_BROWSER','chromium')+'.png')
    page.locator('#start').click()
    expect(page.locator('#score')).to_have_text('0')
def test_native_button_keyboard_does_not_double_dispatch(page):
    page.locator('#start').focus();page.keyboard.press('Enter')
    expect(page.locator('#state')).to_have_text('Running')
    expect(page.locator('#score')).to_have_text('0')
