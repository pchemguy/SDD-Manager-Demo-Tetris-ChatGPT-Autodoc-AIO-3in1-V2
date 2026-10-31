"""Phase-4 configuration must be entirely page-local, including startup."""
from playwright.sync_api import expect

def test_reload_ignores_url_cookie_storage_and_never_writes_them(page,app_url):
    page.context.add_cookies([{'name':'tetris_ghost','value':'hide','url':app_url}])
    page.add_init_script("""window.configIO=[];
const cookie=Object.getOwnPropertyDescriptor(Document.prototype,'cookie');
Object.defineProperty(document,'cookie',{get(){configIO.push('cookie-read');return cookie.get.call(this)},set(v){configIO.push('cookie-write');return cookie.set.call(this,v)}});
for(const k of ['getItem','setItem','removeItem','clear']){Storage.prototype[k]=function(){configIO.push('storage-'+k);throw Error('Unexpected persistent storage')}};
for(const k of ['pushState','replaceState']){const fn=history[k];history[k]=function(...args){configIO.push(k);return fn.apply(this,args)}};
""")
    page.goto(app_url+'/?ghost=hide&hold=off#keep')
    expect(page.locator('#setting-ghost')).to_have_value('show')
    expect(page.locator('#setting-hold')).to_have_value('on')
    page.locator('#setting-ghost').select_option('dynamic')
    page.locator('#setting-lock').select_option('failed')
    page.locator('#start').click();page.keyboard.press('Enter');page.keyboard.press('ArrowDown')
    expect(page.locator('#setting-ghost')).to_have_value('dynamic')
    assert page.evaluate('configIO')==[]
    assert page.url.endswith('/?ghost=hide&hold=off#keep')
    page.reload()
    expect(page.locator('#setting-ghost')).to_have_value('show')
    expect(page.locator('#setting-lock')).to_have_value('interval')
    assert page.evaluate('configIO')==[]
    assert next(c for c in page.context.cookies() if c['name']=='tetris_ghost')['value']=='hide'
