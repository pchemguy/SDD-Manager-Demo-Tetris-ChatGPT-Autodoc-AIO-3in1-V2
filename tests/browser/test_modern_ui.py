"""Modern controls use the keyboard; previews reflect the same live game queue."""
from playwright.sync_api import expect

def test_hold_preview_and_once_per_piece(page):
    page.locator('#start').click()
    before=page.locator('#active-kind').inner_text()
    expect(page.locator('#next-piece')).not_to_contain_text('Empty')
    page.keyboard.press('c')
    expect(page.locator('#hold-piece')).to_contain_text(before)
    active=page.locator('#active-kind').inner_text()
    page.keyboard.press('c')
    assert page.locator('#active-kind').inner_text()==active
    expect(page.locator('#hold-piece')).to_contain_text(before)
    assert page.locator('[data-gameplay]').count()==2

def test_hard_drop_is_keyboard_only_and_repeat_is_timed(page):
    page.locator('#start').click();page.keyboard.press('Enter')
    assert int(page.locator('#score').inner_text())>=30
    page.locator('#start').click()
    page.keyboard.down('ArrowDown');page.wait_for_timeout(230);page.keyboard.up('ArrowDown')
    score=int(page.locator('#score').inner_text());assert 4<=score<=9
    page.wait_for_timeout(100)
    assert int(page.locator('#score').inner_text())==score
