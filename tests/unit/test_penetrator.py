"""Bonus lifecycle, occupied transit, valid deepest landings and lock invariants."""
import pytest

def blank(): return [[None]*10 for _ in range(20)]
def fixture(y=8):
    b=blank();b[10][4]='J'
    return {'status':'running','piece':{'kind':'T','rotation':0,'x':3,'y':y},'board':b,'bonuses':2,'queue':['I','L']}
@pytest.mark.parametrize('before,after',[(0,1),(2,3),(3,3)])
def test_four_rows_award_one_capped_bonus(driver,before,after):
    b=blank()
    for y in range(16,20):
        b[y]=['J']*10;b[y][5]=None
    f={'status':'running','board':b,'piece':{'kind':'I','rotation':1,'x':3,'y':16},'bonuses':before}
    r=driver('game',fixture=f,rules={'lock':'failed','hardDropLock':'general'},actions=[{'type':'down'}])
    assert r['state']['bonuses']==after and r['state']['lines']==4

def test_activation_spends_once_lifts_from_blocker_and_passes_through(driver):
    f=fixture();f.update(time=400,groundedAt=0,groundedInterval=1000,lockAt=1000)
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'activate'},{'type':'down'}])['state']
    assert r['penetrator'] and r['bonuses']==1 and r['piece']['y']==9
    assert r['board'][10][4]=='J' and r['lockAt'] is None

def test_drop_and_ghost_choose_deepest_valid_position_and_white_lock(driver):
    f=fixture();p=f['piece']
    target=driver('landing',board=f['board'],piece=p,penetrator=True)
    assert target['y']==18
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'hardDrop'}])
    assert r['state']['piece']==target and r['state']['score']==20
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'hardDrop'},{'type':'advance','ms':1000}])['state']
    assert not r['penetrator'] and sum(v=='P' for row in r['board'] for v in row)==4
    assert r['board'][10][4]=='J'

def test_lowest_valid_cavity_is_not_first_blocker_or_floor(driver):
    f=fixture(0);f['board'][19]=['J']*10
    assert driver('landing',board=f['board'],piece=f['piece'],penetrator=True)['y']==17

def test_hold_is_blocked_and_activation_with_no_landing_is_not_spent(driver):
    f=fixture(0);f['holdKind']='O'
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'hold'}])['state']
    assert r['piece']['kind']=='T' and r['holdKind']=='O' and r['bonuses']==1
    f={'status':'running','board':[['J']*10 for _ in range(20)],'piece':{'kind':'T','rotation':0,'x':3,'y':-2},'bonuses':1}
    r=driver('game',fixture=f,actions=[{'type':'activate'}])['state'];assert not r['penetrator'] and r['bonuses']==1

def test_invalid_transit_transform_rejected_and_grounding_not_reset(driver):
    b=blank()
    for row in b:row[9]='J'
    f={'status':'running','board':b,'piece':{'kind':'I','rotation':1,'x':6,'y':0},'bonuses':1}
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'right'}])['state']
    assert r['penetrator'] and r['piece']['x']==6
    f=fixture(18);f.update(time=400,groundedAt=0,groundedInterval=1000,lockAt=1000)
    r=driver('game',fixture=f,actions=[{'type':'activate'}])['state'];assert r['lockAt']==1000

def test_rotation_transits_occupancy_and_locks_only_valid_cells(driver):
    f=fixture(0);f['board']=blank();f['board'][2][4]='J'
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'cw'}])['state']
    assert r['piece']=={'kind':'T','rotation':1,'x':3,'y':0} and r['board'][2][4]=='J'
    r=driver('game',fixture=f,actions=[{'type':'activate'},{'type':'cw'},{'type':'hardDrop'},{'type':'advance','ms':1000}])['state']
    assert sum(v=='P' for row in r['board'] for v in row)==4
    assert r['board'][2][4]=='J' and not r['penetrator'] and not r['heldUsed']

@pytest.mark.parametrize('status,bonuses',[('running',0),('paused',1),('game-over',1)])
def test_ineligible_activation_is_a_noop(driver,status,bonuses):
    f=fixture(0);f.update(status=status,bonuses=bonuses)
    r=driver('game',fixture=f,actions=[{'type':'activate'}])['state']
    assert not r['penetrator'] and r['bonuses']==bonuses
