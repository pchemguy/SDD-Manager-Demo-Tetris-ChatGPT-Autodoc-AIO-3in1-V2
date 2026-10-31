import json,subprocess
from pathlib import Path
import pytest
R=Path(__file__).resolve().parents[2]
def run(op,**kw):
 p=subprocess.run(['node','.test-build/tests/support/extension-driver.js'],cwd=R,input=json.dumps(dict(op=op,**kw)),text=True,capture_output=True,timeout=10)
 assert p.returncode==0,p.stderr
 return json.loads(p.stdout)
def test_single_owner_and_acknowledged_transfer():
 q=run('owner'); assert q['a']['owner']=='a' and q['b']['owner']=='a'; assert q['claim']['owner']=='b' and q['claim']['session']['game']['status']=='paused';assert q['claim']['session']['game']['score']==47 and q['yields']==1 and q['rejected'];assert q['local']=={}
def test_failed_write_never_advances_confirmed_state():
 q=run('failure');assert q['error'] and q['unchanged'];assert q['view']['session']['game']['score']==0
def test_disconnect_reopen_and_browser_restart_separate_stores():
 q=run('restart');assert q['reopened']['session']['game']['status']=='paused';assert q['fresh']['session'] is None and q['fresh']['settings']['ghost']=='dynamic';assert list(q['local'])==['settings'];assert 'results' not in str(q['local'])
def test_old_sequence_rejected():
 q=run('sequence');assert q['error'] and q['view']['session']['game']['score']==0
def test_query_valid_explicit_invalid_fallback():
 q=run('query');assert q['resolved']['invalid']==['hold'];assert q['view']['settings']['ghost']=='hide' and q['view']['settings']['hold']=='on'
@pytest.mark.parametrize('value',[{},[],None,{'game':{},'results':[]},{'game':None,'results':[]},{'game':{},'results':[{'score':-1}]}])
def test_invalid_transient_snapshot(value):assert run('validation',value=value)['error']
def test_actual_game_snapshot_valid():assert not run('validation')['error']

@pytest.mark.parametrize('patch',[{'board':[]},{'score':-1},{'level':0},{'seed':4294967296},{'queue':['I','I']},{'bonuses':4},{'time':-1},{'heldUsed':1},{'piece':{'kind':'I','rotation':9,'x':3,'y':0}},{'groundedAt':0,'groundedInterval':None},{'extra':True}])
def test_transient_state_invariants(patch):assert run('validation',mutate=patch)['error']
def test_restore_coordinates_both_stores_and_pauses():
 q=run('restore');assert q['view']['settings']['ghost']=='hide';assert q['view']['session']['game']['status']=='paused';assert q['local']['settings']['formatVersion']==1;assert q['session']['session']['session']['game']['time']==0
