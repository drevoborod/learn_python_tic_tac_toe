import pytest

from src.game.engine import Game


@pytest.fixture
def game():
    return Game().init_game()


@pytest.mark.parametrize("field", (
    [
        [None, None, None],
        [0, None, 0],
        [1, 1, 1],
    ],
    [
        [1, 1, 1],
        [0, None, 0],
        [None, None, None],
    ],
    [
        [1, 0, 1],
        [1, None, 0],
        [1, 0, None],
    ],
    [
        [1, 0, 1],
        [0, None, 1],
        [1, 0, 1],
    ],
    [
        [1, 0, None],
        [0, 1, None],
        [0, 0, 1],
    ],
    [
        [1, 0, 1],
        [0, 1, None],
        [1, 0, None],
    ],
    [
        [None, 1, 1],
        [0, 1, None],
        [0, 1, None],
    ],
    [
        [None, 0, 0],
        [1, 1, 1],
        [1, 0, None],
    ],

))
def test_check_victory_true(game, field):
    """
    Field configurations when the game should be winned.
    """
    game._gamefield._gamefield = field
    assert game._check_victory(1) is True


@pytest.mark.parametrize("field", (
    [
        [0, 1, None],
        [1, 0, None],
        [None, None, 1],
    ],
    [
        [0, 1, None],
        [1, 0, 1],
        [None, None, 1],
    ],
    [
        [0, 1, None],
        [1, 0, 1],
        [1, None, 1],
    ],
    [
        [0, 1, None],
        [1, 0, 1],
        [0, 1, 1],
    ],
))
def test_check_victory_false(game, field):
    """
    Field configurations when the game should be lost.
    """
    game._gamefield._gamefield = field
    assert game._check_victory(1) is False
