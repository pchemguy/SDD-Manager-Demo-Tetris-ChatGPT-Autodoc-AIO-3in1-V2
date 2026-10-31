"""Hand-checked SRS wall/floor fixtures in downward-y coordinates."""
import pytest
@pytest.mark.parametrize('kind,x,y,rotation,expected', [
    ('T',-1,0,1,{'kind':'T','x':0,'y':0,'rotation':2}),
    ('I',-2,0,1,{'kind':'I','x':0,'y':0,'rotation':2}),
    ('T',3,18,0,{'kind':'T','x':2,'y':17,'rotation':1}),
    ('I',3,18,0,{'kind':'I','x':4,'y':16,'rotation':1}),
])
def test_ordered_wall_and_floor_kicks(driver,kind,x,y,rotation,expected):
    r=driver('game',fixture={'status':'running','piece':{'kind':kind,'x':x,'y':y,'rotation':rotation}},actions=[{'type':'cw'}])
    assert r['state']['piece']==expected

def test_all_candidates_blocked_rejects_rotation(driver):
    b=[['J']*10 for _ in range(20)]
    for x,y in [(4,10),(3,11),(4,11),(5,11)]:b[y][x]=None
    p={'kind':'T','x':3,'y':10,'rotation':0}
    assert driver('game',fixture={'status':'running','piece':p,'board':b},actions=[{'type':'cw'}])['state']['piece']==p
