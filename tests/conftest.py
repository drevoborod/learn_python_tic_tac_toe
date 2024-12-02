import pytest

from tic_tac_toe.game.engine import Game


@pytest.fixture
def game():
    return Game().assign_player_roles()
