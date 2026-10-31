"""Occupied projected cells, rather than origin/bounding box, determine visibility."""
import pytest
@pytest.mark.parametrize('kind,rotation,y,visible',[('T',0,9,False),('T',0,10,True),('I',0,8,False),('I',0,9,True),('I',1,9,False),('I',1,10,True)])
def test_midline_and_straddling(driver,kind,rotation,y,visible):
    assert driver('ghostVisible',piece={'kind':kind,'rotation':rotation,'x':3,'y':y}) is visible
