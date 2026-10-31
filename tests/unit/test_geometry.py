"""Independent spawn, rotation and collision fixtures from G-1."""
import pytest
SHAPES = {
    'I': [[0, 1], [1, 1], [2, 1], [3, 1]],
    'O': [[1, 0], [2, 0], [1, 1], [2, 1]],
    'T': [[1, 0], [0, 1], [1, 1], [2, 1]],
    'S': [[1, 0], [2, 0], [0, 1], [1, 1]],
    'Z': [[0, 0], [1, 0], [1, 1], [2, 1]],
    'J': [[0, 0], [0, 1], [1, 1], [2, 1]],
    'L': [[2, 0], [0, 1], [1, 1], [2, 1]],
}
@pytest.mark.parametrize('kind', SHAPES)
def test_spawn_cells(driver, kind):
    actual = driver('geometry', piece={'kind': kind, 'rotation': 0, 'x': 3, 'y': -1})
    assert actual['cells'] == [[x+3, y-1] for x, y in SHAPES[kind]]
    assert actual['valid']
@pytest.mark.parametrize('x,y', [(-2, 0), (9, 0), (3, 20), (3, -4)])
def test_active_bounds(driver, x, y):
    assert not driver('geometry', piece={'kind': 'T', 'rotation': 0, 'x': x, 'y': y})['valid']
def test_collision_and_clockwise_rotation(driver):
    board = [[None]*10 for _ in range(20)]
    board[1][4] = 'I'
    piece = {'kind': 'T', 'rotation': 0, 'x': 3, 'y': 0}
    assert not driver('geometry', piece=piece, board=board)['valid']
    piece['rotation'] = 1
    assert driver('geometry', piece=piece)['cells'] == [[5, 1], [4, 0], [4, 1], [4, 2]]
