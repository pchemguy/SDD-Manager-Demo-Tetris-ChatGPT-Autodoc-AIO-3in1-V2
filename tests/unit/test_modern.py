"""Modern source/hold contracts with independent bag and lifecycle expectations."""
import pytest
@pytest.mark.parametrize('seed', [1, 7, 12345, 4294967295])
def test_each_seven_draws_form_a_bag(driver, seed):
    draws=driver('source', seed=seed, count=28)
    for start in range(0,28,7): assert sorted(draws[start:start+7])==sorted('IOTSZJL')
def test_hold_consumes_once_and_swap_preserves_queue(driver):
    p={'kind':'T','rotation':2,'x':2,'y':8}
    r=driver('game',fixture={'status':'running','piece':p,'queue':['I','L'],'holdKind':None,'heldUsed':False},actions=[{'type':'hold'},{'type':'hold'}])['state']
    assert r['piece']=={'kind':'I','rotation':0,'x':3,'y':-1}
    assert r['holdKind']=='T' and r['heldUsed']
    r=driver('game',fixture={'status':'running','piece':p,'queue':['I','L'],'holdKind':'O','heldUsed':False},actions=[{'type':'hold'}])['state']
    assert r['piece']['kind']=='O' and r['queue']==['I','L'] and r['holdKind']=='T'
def test_blocked_hold_spawn_ends_game(driver):
    b=[[None]*10 for _ in range(20)];b[0]=['J']*10
    r=driver('game',fixture={'status':'running','board':b,'piece':{'kind':'T','rotation':0,'x':3,'y':10},'holdKind':'I','heldUsed':False},actions=[{'type':'hold'}])
    assert r['state']['status']=='game-over' and len([e for e in r['events'] if e['type']=='complete'])==1
