"""Production gameplay records completion once and keeps history only in this page."""
from playwright.sync_api import expect

def complete(page):
    page.locator('#start').click()
    for _ in range(35):page.keyboard.press('Enter')
    expect(page.locator('#state')).to_have_text('Game over')

def test_completed_game_once_hidden_panel_retention_and_reload(page):
    assert page.locator('#leaderboard-body tr').count()==0
    page.locator('#setting-hardDropLock').select_option('immediate')
    complete(page)
    rows=page.locator('#leaderboard-body tr');assert rows.count()==1
    before=rows.first.get_attribute('data-id')
    stamp=rows.first.locator('time').get_attribute('datetime');assert stamp.endswith('Z')
    page.keyboard.press('Enter');page.keyboard.press('p');assert rows.count()==1
    page.locator('#toggle-leaderboard').click();expect(page.locator('#leaderboard')).to_be_hidden()
    page.locator('#start').click();page.keyboard.press('r')
    page.locator('#toggle-leaderboard').click();assert rows.count()==1
    assert rows.first.get_attribute('data-id')==before
    page.reload();assert page.locator('#leaderboard-body tr').count()==0
    expect(page.locator('#setting-hardDropLock')).to_have_value('immediate')
    assert page.locator('[data-gameplay]').count()==2

def test_twelve_real_completed_games_keep_ten_without_persisting_scores(page,app_url):
    page.locator('#setting-hardDropLock').select_option('immediate')
    page.add_init_script("window.scoreStorageIO=[];for(const k of ['getItem','setItem'])Storage.prototype[k]=function(){scoreStorageIO.push(k);throw Error('Scores must stay session-only')}")
    requests=[];page.on('request',lambda r:requests.append(r.url))
    page.reload();before=page.context.cookies();url=page.url
    for _ in range(12):complete(page)
    rows=page.locator('#leaderboard-body tr');assert rows.count()==10
    ids=rows.evaluate_all('(rows)=>rows.map(r=>r.dataset.id)');assert len(set(ids))==10
    scores=[int(rows.nth(n).locator('td').nth(1).inner_text()) for n in range(10)]
    assert scores==sorted(scores,reverse=True)
    assert page.evaluate('scoreStorageIO')==[]
    assert page.context.cookies()==before and page.url==url
    assert all(u.startswith(app_url) for u in requests)
