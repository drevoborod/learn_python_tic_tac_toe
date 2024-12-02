import pytest

from tic_tac_toe.game.engine import Game


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
def test_check_victory_return_true(game: Game, field):
    """
    Field configurations when the game should be winned.
    """
    game._gamefield._board = field
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
def test_check_victory_return_false(game: Game, field):
    """
    Field configurations when the game should be lost.
    """
    game._gamefield._board = field
    assert game._check_victory(2) is False
