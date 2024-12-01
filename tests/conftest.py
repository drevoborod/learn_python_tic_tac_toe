import pytest

from tic_tac_toe.game.engine import Game


@pytest.fixture
def game():
    return Game().init_game()
