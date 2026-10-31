"""Canonical settings are strict and transitions retain original grounding history."""
import pytest
DEFAULTS=dict(ghost='show',hardDrop='on',next='on',hardDropLock='general',lock='interval',hold='on')
def test_defaults_and_disabled_commands(driver):
    r=driver('settings',steps=[{'command':{'type':'start'}},{'settings':{'hold':'off','hardDrop':'off'}},{'command':{'type':'hold'}},{'command':{'type':'hardDrop'}}])
    assert r['settings']=={**DEFAULTS,'hold':'off','hardDrop':'off'}
    assert r['state']['holdKind'] is None and not r['state']['heldUsed']
    assert r['state']['piece']['y']==-1
@pytest.mark.parametrize('bad',[{'ghost':'SHOW'},{'hold':True},{'next':1},{'other':'on'},{'lock':None}])
def test_invalid_patch_is_atomic(driver,bad):
    r=driver('settings',steps=[{'settings':{'ghost':'hide',**bad}}])
    assert r['settings']==DEFAULTS and len(r['errors'])==1
@pytest.mark.parametrize('key,values',[('ghost',['hide','dynamic','show']),('hardDrop',['off','on']),('next',['off','on']),('hardDropLock',['immediate','general']),('lock',['failed','interval']),('hold',['off','on'])])
def test_all_domains(driver,key,values):
    for value in values:
        assert driver('settings',steps=[{'settings':{key:value}}])['settings'][key]==value
def test_policy_transition_does_not_restart_ground_time(driver):
    r=driver('settings',steps=[{'command':{'type':'start'}},{'command':{'type':'hardDrop'}},{'at':500,'settings':{'lock':'failed'}},{'at':999,'settings':{'lock':'interval'}}])
    assert r['state']['groundedAt']==0 and r['state']['lockAt']==1000
    r=driver('settings',steps=[{'command':{'type':'start'}},{'command':{'type':'hardDrop'}},{'settings':{'lock':'failed'}},{'at':1500,'settings':{'lock':'interval'}}])
    assert any(any(c for c in row) for row in r['state']['board'])
def test_restart_preserves_settings_and_hold_toggle_eligibility(driver):
    r=driver('settings',steps=[{'command':{'type':'start'}},{'command':{'type':'hold'}},{'settings':{'hold':'off'}},{'settings':{'hold':'on'}},{'command':{'type':'hold'}}])
    assert r['state']['heldUsed']
    r=driver('settings',steps=[{'settings':{'ghost':'hide'}},{'command':{'type':'start'}}])
    assert r['settings']['ghost']=='hide'
