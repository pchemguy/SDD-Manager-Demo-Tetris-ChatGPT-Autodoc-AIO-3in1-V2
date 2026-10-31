"""Landing/drop agreement, distance scoring and rotated wall-kick integration."""
import pytest
def test_stops_before_first_blocker_and_matches_drop(driver):
    b=[[None]*10 for _ in range(20)];b[10][4]='J'
    p={'kind':'T','x':3,'y':0,'rotation':0}
    assert driver('landing',board=b,piece=p)['y']==8
    r=driver('game',fixture={'status':'running','board':b,'piece':p},actions=[{'type':'hardDrop'}])
    assert r['state']['piece']['y']==8 and r['state']['score']==16
    assert not r['events']
def test_floor_drop_scores_only_actual_distance(driver):
    r=driver('game',fixture={'status':'running','piece':{'kind':'T','x':3,'y':0,'rotation':0}},actions=[{'type':'hardDrop'},{'type':'hardDrop'}])
    assert r['state']['piece']['y']==18 and r['state']['score']==36
    assert not r['events']
@pytest.mark.parametrize('kind,x,expected_x', [('T',8,7),('I',7,5)])
def test_counterclockwise_wall_kick_then_drop(driver,kind,x,expected_x):
    r=driver('game',fixture={'status':'running','piece':{'kind':kind,'x':x,'y':0,'rotation':3}},actions=[{'type':'ccw'},{'type':'hardDrop'}])
    assert r['state']['piece']=={'kind':kind,'x':expected_x,'y':17,'rotation':2}
    assert r['state']['score']==34
