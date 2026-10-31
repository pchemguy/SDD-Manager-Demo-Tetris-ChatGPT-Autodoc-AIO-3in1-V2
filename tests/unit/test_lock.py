"""Grounded timing boundaries, lift-off, hard drop and policy-history preservation."""
def floor_fixture(y=18):
    return {'status':'running','piece':{'kind':'T','rotation':0,'x':3,'y':y},'queue':['I','L']}
def locks(r):
    return sum(e['type']=='lock' for e in r['events'])
def test_waits_exact_interval_and_failed_down_does_not_lock_early(driver):
    f=floor_fixture()
    r=driver('game',fixture=f,actions=[{'type':'down'},{'type':'advance','ms':999}]);assert locks(r)==0
    r=driver('game',fixture=f,actions=[{'type':'down'},{'type':'advance','ms':1000}]);assert locks(r)==1

def test_grounded_moves_rotations_and_repeat_drop_do_not_reset(driver):
    acts=[{'type':'advance','ms':400},{'type':'left'},{'type':'cw'},{'type':'hardDrop'},{'type':'hardDrop'},{'type':'advance','ms':599}]
    r=driver('game',fixture=floor_fixture(),actions=acts);assert locks(r)==0 and r['state'].get('lockAt')==1000
    assert locks(driver('game',fixture=floor_fixture(),actions=acts+[{'type':'advance','ms':1}]))==1

def test_actual_liftoff_starts_a_new_interval(driver):
    f=floor_fixture(17);b=[[None]*10 for _ in range(20)];b[19][4]='J';f['board']=b
    acts=[{'type':'advance','ms':400},{'type':'left'},{'type':'left'},{'type':'hardDrop'},{'type':'advance','ms':999}]
    r=driver('game',fixture=f,actions=acts);assert locks(r)==0 and r['state'].get('lockAt')==1400
    assert locks(driver('game',fixture=f,actions=acts+[{'type':'advance','ms':1}]))==1

def test_pause_and_delayed_frames_preserve_deadline(driver):
    r=driver('game',fixture=floor_fixture(),actions=[{'type':'advance','ms':400},{'type':'pause'},{'type':'advance','ms':9000},{'type':'resume'},{'type':'advance','ms':599}]);assert locks(r)==0
    r=driver('game',fixture=floor_fixture(),actions=[{'type':'advance','ms':3500}]);assert locks(r)==1 and r['state']['piece']['y']==1

def test_immediate_hard_drop_and_failed_general_policy(driver):
    f=floor_fixture(0)
    assert locks(driver('game',fixture=f,rules={'lock':'interval','hardDropLock':'immediate'},actions=[{'type':'hardDrop'}]))==1
    assert locks(driver('game',fixture=f,rules={'lock':'failed','hardDropLock':'general'},actions=[{'type':'hardDrop'}]))==0
    assert locks(driver('game',fixture=f,rules={'lock':'failed','hardDropLock':'general'},actions=[{'type':'hardDrop'},{'type':'down'}]))==1

def test_policy_changes_cannot_regrant_an_expired_interval(driver):
    f=floor_fixture();f['gravityAt']=5000
    r=driver('game',fixture=f,rules={'lock':'failed','hardDropLock':'general'},actions=[{'type':'advance','ms':1200},{'type':'configure','rules':{'lock':'interval','hardDropLock':'general'}}])
    assert locks(r)==1

def test_input_clock_advances_due_lock_before_late_key(driver):
    r=driver('clock',steps=[{'at':0,'command':{'type':'start'}},{'at':0,'command':{'type':'hardDrop'}},{'at':1000,'command':{'type':'left'}}])
    assert locks(r)==1 and r['state']['time']==1000
    assert sum(v is not None for row in r['state']['board'] for v in row)==4

def test_host_pause_clock_excludes_hidden_wall_time(driver):
    r=driver('clock',steps=[{'at':0,'command':{'type':'start'}},{'at':0,'command':{'type':'hardDrop'}},{'at':400,'command':{'type':'pause'}},{'at':10000,'command':{'type':'resume'}},{'at':10600,'command':{'type':'left'}}])
    assert locks(r)==1 and r['state']['time']==1000
