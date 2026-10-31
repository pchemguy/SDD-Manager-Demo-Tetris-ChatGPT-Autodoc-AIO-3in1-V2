"""Strict JSON and staged restore: invalid data has no application/host effects."""
import json
import pytest
from test_snapshot import doc,row

@pytest.mark.parametrize('text',['{}','null','[]','{"formatVersion":1,"formatVersion":1}','{"settings":{"hold":"on","hold":"off"}}','{"settings":{"hold":"on","\\u0068old":"off"}}','{"results":[{"id":"a","id":"b"}]}','{"x":NaN}','{"x":1,}','/*comment*/{}','\ufeff\ufeff{}'])
def test_invalid_or_duplicate_content_rejected(driver,text):
    assert 'error' in driver('json',text=text)
    tx=driver('fileTransaction',text=text);assert tx['error'] and tx['before']==tx['after'] and tx['writes']==0

def test_duplicate_key_error_is_lexical_not_salvaged(driver):
    text=json.dumps(doc()).replace('"hold": "on"','"hold": "on", "hold": "off"')
    assert 'Duplicate JSON' in driver('json',text=text)['error']

def test_utf8_bom_and_roundtrip(driver):
    candidate={**doc(),'results':[row(1,0),row(2,9007199254740991)]}
    r=driver('json',encode=True,document=candidate)
    assert r['snapshot']['results'][0]['score']==9007199254740991
    assert driver('json',text='\ufeff'+r['text'])['snapshot']==r['snapshot']
    assert 'error' in driver('json',bytes=[0xc0,0xaf])
    assert '2 MiB' in driver('json',text=' '*2097153)['error']

def test_invalid_restore_preserves_all_observables(driver):
    candidate=doc();candidate['settings']['ghost']='invalid'
    r=driver('fileTransaction',text=json.dumps(candidate))
    assert r['error'] and r['before']==r['after'] and r['writes']==0
    assert r['locked'] and not r['busy'] and not r['settingsLocked'] and 'already in progress' in r['concurrent']

def test_valid_restore_pauses_and_replaces_all_settings_and_results(driver):
    candidate={**doc(),'results':[row(1,50)]}
    r=driver('fileTransaction',text=json.dumps(candidate))
    assert not r['error'] and not r['busy'] and r['locked']
    assert r['after']['state']=={**r['before']['state'],'status':'paused'}
    assert r['after']['results']==candidate['results'] and r['after']['settings']==candidate['settings']
    assert 'keep=abc' in r['after']['href'] and r['after']['href'].endswith('#stay')
    assert r['writes']==6

def test_partial_host_failure_rolls_back_before_application_commit(driver):
    r=driver('fileTransaction',text=json.dumps(doc()),failAt=3)
    assert r['error'] and r['before']==r['after'] and not r['blocked'] and not r['busy']

def test_rollback_failure_is_explicit_and_blocks_persistence(driver):
    r=driver('fileTransaction',text=json.dumps(doc()),failAt=3,failAlways=True)
    assert 'rollback' in r['error'].lower() and r['blocked'] and not r['busy'] and r['blockedWritePrevented']
    for key in ['state','settings','results']:assert r['before'][key]==r['after'][key]

def test_export_captures_before_async_encoding_and_live_completion(driver):
    r=driver('exportCapture')
    assert r['snapshot']['results']==[] and len(r['currentResults'])==1 and not r['busy']
