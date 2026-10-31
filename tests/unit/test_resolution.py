"""Resolve each key independently; malformed explicit inputs never poison saved values."""
import pytest
from test_settings import DEFAULTS

def test_mixed_sources_and_explicit_default(driver):
    r=driver('resolveSettings',search='?ghost=show&hold=off&unrelated=1',cookie='tetris_ghost=hide; tetris_next=off; tetris_lock=failed')
    assert r['settings']=={**DEFAULTS,'hold':'off','next':'off','lock':'failed'}
    assert r['explicit']=={'ghost':'show','hold':'off'}
    assert r['invalid']==[]
@pytest.mark.parametrize('search',['?ghost=','?ghost=SHOW','?ghost=hide&ghost=show','?ghost=%ZZ','?ghost=%E0%A4%A','?ghost=off'])
def test_bad_url_falls_back_without_write(driver,search):
    r=driver('resolveSettings',search=search,cookie='tetris_ghost=dynamic')
    assert r['settings']['ghost']=='dynamic' and r['explicit']=={} and r['invalid']==['ghost']
@pytest.mark.parametrize('cookie',['tetris_hold=true','tetris_hold=%ZZ','tetris_hold=off; tetris_hold=on'])
def test_bad_cookie_falls_back(driver,cookie):
    r=driver('resolveSettings',cookie=cookie)
    assert r['settings']==DEFAULTS and r['invalid']==['hold']
def test_encoded_names_values_and_omitted_saved_values(driver):
    r=driver('resolveSettings',search='?%67host=%64ynamic',cookie='tetris_hold=off; tetris_hardDrop=off; tetris_hardDropLock=immediate')
    assert r['settings']=={**DEFAULTS,'ghost':'dynamic','hold':'off','hardDrop':'off','hardDropLock':'immediate'}
    assert r['explicit']=={'ghost':'dynamic'}
@pytest.mark.parametrize('key',list(DEFAULTS))
def test_every_key_has_three_source_precedence(driver,key):
    alternatives={'ghost':'hide','hardDrop':'off','next':'off','hardDropLock':'immediate','lock':'failed','hold':'off'}
    saved=alternatives[key]
    assert driver('resolveSettings')['settings'][key]==DEFAULTS[key]
    assert driver('resolveSettings',cookie=f'tetris_{key}={saved}')['settings'][key]==saved
    r=driver('resolveSettings',search=f'?{key}={DEFAULTS[key]}',cookie=f'tetris_{key}={saved}')
    assert r['settings'][key]==DEFAULTS[key] and r['explicit'][key]==DEFAULTS[key]
