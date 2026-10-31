"""Classic G-1/G-2 state, timing, score and completion boundaries."""
def piece(kind='T', x=3, y=0, rotation=0):
    return {'kind': kind, 'x': x, 'y': y, 'rotation': rotation}
def board():
    return [[None]*10 for _ in range(20)]
def test_start_gravity_and_immutable_transition(driver):
    r = driver('game', actions=[{'type': 'start'}, {'type': 'advance', 'ms': 1000}])
    assert r['state']['status'] == 'running'
    assert r['state']['piece']['y'] == 0
    assert r['immutable']
def test_pause_freezes_time_and_resume_remaining_interval(driver):
    r = driver('game', actions=[{'type': 'start'}, {'type': 'advance', 'ms': 400}, {'type': 'pause'}, {'type': 'advance', 'ms': 9000}, {'type': 'resume'}, {'type': 'advance', 'ms': 600}])
    assert r['state']['time'] == 1000
    assert r['state']['piece']['y'] == 0
def test_failed_down_locks_and_awards_preclear_level_score(driver):
    b = board(); b[19] = ['J']*10
    for x in range(3, 7): b[19][x] = None
    r = driver('game', fixture={'status': 'running', 'board': b, 'piece': piece('I', y=18), 'lines': 9}, actions=[{'type': 'down'}])
    assert r['state']['score'] == 100
    assert r['state']['lines'] == 10 and r['state']['level'] == 2
    assert all(v is None for v in r['state']['board'][19])
    assert [e['type'] for e in r['events']] == ['lock', 'clear']
def test_soft_drop_and_rejected_wall_move(driver):
    r = driver('game', fixture={'status': 'running', 'piece': piece('T', x=0)}, actions=[{'type': 'left'}, {'type': 'down'}])
    assert r['state']['piece']['x'] == 0 and r['state']['piece']['y'] == 1
    assert r['state']['score'] == 1
def test_top_out_completes_only_once_and_restart_abandons(driver):
    b = board();b[1] = ['J']*10
    r = driver('game', fixture={'status': 'running', 'board': b, 'piece': piece(y=-1), 'score': 7}, actions=[{'type': 'down'}, {'type': 'down'}, {'type': 'advance', 'ms': 10000}])
    assert r['state']['status'] == 'game-over'
    assert [e for e in r['events'] if e['type'] == 'complete'] == [{'type': 'complete', 'score': 7}]
    r = driver('game', fixture={'status': 'running', 'score': 99}, actions=[{'type': 'start'}])
    assert r['state']['score'] == 0 and not r['events']
