"""Three independent panel toggles precede exactly two native gameplay controls."""
import itertools
from playwright.sync_api import expect
from test_files import observable
TARGETS=['leaderboard','settings','help']

def select_panels(page,visible):
    for name,shown in zip(TARGETS,visible):
        button=page.locator('#toggle-'+name)
        if (button.get_attribute('aria-expanded')=='true')!=shown:button.click()
        assert button.get_attribute('aria-controls')==name
        assert button.get_attribute('aria-expanded')==str(shown).lower()
        expect(page.locator('#'+name)).to_be_visible() if shown else expect(page.locator('#'+name)).to_be_hidden()
    page.wait_for_function("Math.abs((document.querySelector('#board').getBoundingClientRect().left+document.querySelector('#board').getBoundingClientRect().right)/2-innerWidth/2)<1")

def test_all_eight_combinations_preserve_game_configuration_and_persistence(page):
    page.locator('#setting-ghost').select_option('dynamic');page.locator('#start').click();page.keyboard.press('p')
    before=observable(page);kind=page.locator('#active-kind').inner_text()
    assert page.locator('.info button').count()==5 and page.locator('[data-gameplay]').count()==2
    for visible in itertools.product([False,True],repeat=3):
        select_panels(page,visible)
        assert observable(page)==before
        assert page.locator('#active-kind').inner_text()==kind
        expect(page.locator('#state')).to_have_text('Paused')
        expect(page.locator('.info')).to_be_visible();expect(page.locator('#board')).to_be_visible()
        expect(page.locator('#save')).to_be_visible() if visible[1] else expect(page.locator('#save')).to_be_hidden()
        expect(page.locator('#restore')).to_be_visible() if visible[1] else expect(page.locator('#restore')).to_be_hidden()
    start=page.locator('#start').bounding_box();pause=page.locator('#pause').bounding_box()
    assert start['x']<pause['x'] and abs(start['y']-pause['y'])<1
    for name in TARGETS:
        box=page.locator('#toggle-'+name).bounding_box();assert box['y']+box['height']<start['y']+1

def test_native_select_keyboard_does_not_move_or_restart_game(page):
    page.locator('#start').click();page.keyboard.press('p');kind=page.locator('#active-kind').inner_text()
    page.locator('#setting-ghost').focus();page.keyboard.press('Home');page.keyboard.press('ArrowDown');page.keyboard.press('Enter')
    expect(page.locator('#setting-ghost')).to_have_value('dynamic')
    expect(page.locator('#state')).to_have_text('Paused');assert page.locator('#active-kind').inner_text()==kind
    page.keyboard.press('r');expect(page.locator('#state')).to_have_text('Paused')
