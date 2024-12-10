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
def test__check_victory__return_true_when_game_should_be_winned(make_game, field):
    game = make_game(field)
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
def test__check_victory__return_false_when_game_should_be_lost(field, make_game):
    game = make_game(field)
    assert game._check_victory(2) is False
