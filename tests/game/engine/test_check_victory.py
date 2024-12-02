import pytest

from tic_tac_toe.game.engine import Game


def matrix_to_dict(matrix: list[list[int]]) -> dict[int, set[tuple[int, int]]]:
    result = {0: set(), 1: set(), 2: set()}
    for line_num, line in enumerate(matrix):
        for col_num, value in enumerate(line):
            result[value].add((col_num, line_num))
    return result


@pytest.mark.parametrize("field", (
    [
        [0, 0, 0],
        [1, 0, 1],
        [2, 2, 2],
    ],
    [
        [2, 2, 2],
        [1, 0, 1],
        [0, 0, 0],
    ],
    [
        [2, 1, 2],
        [2, 0, 1],
        [2, 1, 0],
    ],
    [
        [2, 1, 2],
        [1, 0, 2],
        [2, 1, 2],
    ],
    [
        [2, 1, 0],
        [1, 2, 0],
        [1, 1, 2],
    ],
    [
        [2, 1, 2],
        [1, 2, 0],
        [2, 1, 0],
    ],
    [
        [0, 2, 2],
        [1, 2, 0],
        [1, 2, 0],
    ],
    [
        [0, 1, 1],
        [2, 2, 2],
        [2, 1, 0],
    ],

))
def test__check_victory__return_true(game: Game, field):
    """
    Field configurations when the game should be winned.
    """
    game._gamefield._board = matrix_to_dict(field)
    assert game._check_victory(2) is True


@pytest.mark.parametrize("field", (
    [
        [1, 2, 0],
        [2, 1, 0],
        [0, 0, 2],
    ],
    [
        [1, 2, 0],
        [2, 1, 2],
        [0, 0, 2],
    ],
    [
        [1, 2, 0],
        [2, 1, 2],
        [2, 0, 2],
    ],
    [
        [1, 2, 0],
        [2, 1, 2],
        [1, 2, 2],
    ],
))
def test__check_victory__return_false(game: Game, field):
    """
    Field configurations when the game should be lost.
    """
    game._gamefield._board = matrix_to_dict(field)
    assert game._check_victory(2) is False
