"""Actual cookie/query continuity, precedence and blocked-host diagnostics."""
from playwright.sync_api import expect

def cookies(page):
    return {c['name']:c['value'] for c in page.context.cookies() if c['name'].startswith('tetris_')}

def test_mixed_startup_explicit_defaults_and_omitted_cookie_retention(page,app_url):
    page.context.add_cookies([{'name':'tetris_'+k,'value':v,'url':app_url} for k,v in {'ghost':'hide','next':'off','hold':'off','lock':'failed'}.items()])
    page.goto(app_url+'/?ghost=show&hardDrop=off&keep=abc#anchor')
    for key,value in {'ghost':'show','hardDrop':'off','next':'off','hold':'off','lock':'failed','hardDropLock':'general'}.items():
        expect(page.locator('#setting-'+key)).to_have_value(value)
    assert cookies(page)==dict(tetris_ghost='show',tetris_next='off',tetris_hold='off',tetris_lock='failed',tetris_hardDrop='off')
    page.goto(app_url+'/')
    expect(page.locator('#setting-ghost')).to_have_value('show')
    expect(page.locator('#setting-next')).to_have_value('off')
    expect(page.locator('#setting-hardDrop')).to_have_value('off')

def test_change_preserves_unrelated_query_and_fragment_and_reloads(page,app_url):
    page.goto(app_url+'/?ghost=hide&ghost=show&unrelated=one&unrelated=two#stay')
    expect(page.locator('#notice')).to_contain_text('ghost')
    page.locator('#setting-ghost').select_option('dynamic')
    assert page.evaluate("new URL(location.href).searchParams.getAll('ghost')")==['dynamic']
    assert page.evaluate("new URL(location.href).searchParams.getAll('unrelated')")==['one','two']
    assert page.url.endswith('#stay')
    assert cookies(page)=={'tetris_ghost':'dynamic'}
    page.reload();expect(page.locator('#setting-ghost')).to_have_value('dynamic')
    cookie=next(c for c in page.context.cookies() if c['name']=='tetris_ghost')
    assert cookie['sameSite']=='Lax' and cookie['path']=='/' and cookie['expires']>0

def test_invalid_explicit_keeps_valid_cookie_and_original_url(page,app_url):
    page.context.add_cookies([{'name':'tetris_ghost','value':'dynamic','url':app_url}])
    page.goto(app_url+'/?ghost=%ZZ&hold=FALSE#preserve')
    expect(page.locator('#setting-ghost')).to_have_value('dynamic')
    expect(page.locator('#setting-hold')).to_have_value('on')
    assert cookies(page)=={'tetris_ghost':'dynamic'}
    assert page.url.endswith('?ghost=%ZZ&hold=FALSE#preserve')
    expect(page.locator('#notice')).to_contain_text('ghost')
    expect(page.locator('#notice')).to_contain_text('hold')

def test_cookie_write_rejection_reports_but_keeps_session_selection(page):
    page.add_init_script("Object.defineProperty(document,'cookie',{get(){return ''},set(v){}})")
    page.reload();page.locator('#setting-ghost').select_option('hide')
    expect(page.locator('#setting-ghost')).to_have_value('hide')
    expect(page.locator('#notice')).to_contain_text('could not be confirmed')
    page.locator('#start').click();expect(page.locator('#state')).to_have_text('Running')

def test_all_six_settings_cookie_url_default_and_reload_branches(page,app_url):
    defaults=dict(ghost='show',hardDrop='on',next='on',hardDropLock='general',lock='interval',hold='on')
    alternate=dict(ghost='hide',hardDrop='off',next='off',hardDropLock='immediate',lock='failed',hold='off')
    page.add_init_script("for(const k of ['getItem','setItem'])Storage.prototype[k]=function(){throw Error('No persistent score/storage channel is in scope')}")
    page.context.add_cookies([{'name':'tetris_'+k,'value':v,'url':app_url} for k,v in alternate.items()])
    page.goto(app_url+'/')
    for key,value in alternate.items():expect(page.locator('#setting-'+key)).to_have_value(value)
    page.goto(app_url+'/?'+'&'.join(k+'='+v for k,v in defaults.items()))
    for key,value in defaults.items():expect(page.locator('#setting-'+key)).to_have_value(value)
    assert cookies(page)=={'tetris_'+k:v for k,v in defaults.items()}
    for key,value in alternate.items():page.locator('#setting-'+key).select_option(value)
    page.reload()
    for key,value in alternate.items():expect(page.locator('#setting-'+key)).to_have_value(value)
    page.goto(app_url+'/')
    for key,value in alternate.items():expect(page.locator('#setting-'+key)).to_have_value(value)
