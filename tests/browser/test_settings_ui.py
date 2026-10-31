"""Native settings controls update the shared application without extra gameplay buttons."""
from playwright.sync_api import expect

def test_settings_disable_preview_hold_drop_and_keep_native_keys(page):
    assert page.locator('#settings select').count()==6
    page.locator('#setting-next').select_option('off')
    expect(page.locator('#next-piece').locator('..')).to_be_hidden()
    page.locator('#setting-hold').select_option('off')
    page.locator('#setting-hardDrop').select_option('off')
    page.locator('#start').click();kind=page.locator('#active-kind').inner_text()
    page.keyboard.press('c');page.keyboard.press('Enter')
    assert page.locator('#score').inner_text()=='0'
    assert page.locator('#active-kind').inner_text()==kind
    expect(page.locator('#hold-piece')).to_contain_text('Empty')
    page.locator('#setting-ghost').focus();page.keyboard.press('r')
    assert page.locator('#state').inner_text()=='Running'
    page.locator('#setting-hold').select_option('on');page.locator('#board').focus();page.keyboard.press('c')
    expect(page.locator('#hold-piece')).to_contain_text(kind)
    assert page.locator('[data-gameplay]').count()==2

def test_hidden_settings_retain_values_and_stop_held_input(page):
    page.locator('#setting-lock').select_option('failed')
    page.locator('#toggle-settings').click();expect(page.locator('#settings')).to_be_hidden()
    page.locator('#start').click();page.keyboard.down('ArrowDown')
    page.locator('#toggle-settings').click();page.locator('#setting-lock').focus()
    score=page.locator('#score').inner_text();page.wait_for_timeout(180);page.keyboard.up('ArrowDown')
    assert page.locator('#score').inner_text()==score
    assert page.locator('#setting-lock').input_value()=='failed'
