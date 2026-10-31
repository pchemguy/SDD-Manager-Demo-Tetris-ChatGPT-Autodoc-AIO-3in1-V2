"""Immutable, strict completed results; rank ties by time then ASCII UUID."""
import pytest

def result(n=1,score=0,time='2026-01-01T00:00:00.000Z'):
    return dict(id=f'00000000-0000-4000-8000-{n:012}',score=score,timestamp=time)

def test_rank_top_ten_ties_and_detached_input(driver):
    rows=[result(n,n//2) for n in range(1,13)]
    r=driver('results',results=list(reversed(rows)),rank=True)
    assert r['immutable'] and len(r['results'])==10
    assert [v['id'] for v in r['results']]==[result(n)['id'] for n in [12,10,11,8,9,6,7,4,5,2]]
    r=driver('results',results=[result(1,5,'2026-01-02T00:00:00.000Z'),result(2,5)],rank=True)
    assert r['results'][0]['id']==result(2)['id']
@pytest.mark.parametrize('patch',[{'score':-1},{'score':True},{'score':1.5},{'score':9007199254740992},{'timestamp':'2023-02-29T00:00:00.000Z'},{'timestamp':'2026-04-31T00:00:00.000Z'},{'timestamp':'2026-01-01T00:00:60.000Z'},{'timestamp':'0000-01-01T00:00:00.000Z'},{'timestamp':'2026-01-01T00:00:00Z'},{'id':'ABC'},{'extra':1}])
def test_bad_record_rejected(driver,patch):
    assert 'error' in driver('results',results=[{**result(),**patch}])
@pytest.mark.parametrize('time',['0001-01-01T00:00:00.000Z','2024-02-29T23:59:59.999Z','9999-12-31T23:59:59.999Z'])
def test_utc_roundtrip_and_safe_max(driver,time):
    assert driver('results',results=[result(score=9007199254740991,time=time)])['results'][0]['timestamp']==time

def test_duplicates_and_excess_import_history_rejected(driver):
    assert 'error' in driver('results',results=[result(),result()])
    assert 'error' in driver('results',results=[result(n) for n in range(11)])

def test_controller_zero_gameover_once_and_unfinished_restart(driver):
    r=driver('session',steps=[{'command':{'type':'start'}},{'at':300000,'tick':True},{'at':400000,'tick':True},{'command':{'type':'pause'}}])
    assert r['state']['status']=='game-over' and len(r['results'])==1
    assert r['results'][0]==result(time='2026-01-01T00:05:00.000Z')
    assert driver('session',steps=[{'command':{'type':'start'}},{'command':{'type':'start'}}])['results']==[]

def test_late_restart_records_old_completion_before_new_game(driver):
    r=driver('session',steps=[{'command':{'type':'start'}},{'at':300000,'command':{'type':'start'}},{'at':600000,'tick':True}])
    assert len(r['results'])==2 and r['results'][0]['timestamp']<r['results'][1]['timestamp']
    assert r['results'][0]['id']!=r['results'][1]['id']

def test_uuid_port_works_without_secure_context_random_uuid(driver):
    import re
    ids=driver('hostIDs')
    assert len(set(ids))==100
    assert all(re.fullmatch('[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}',v) for v in ids)
