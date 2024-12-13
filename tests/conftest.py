import pytest

from tic_tac_toe.game.engine import Game


@pytest.fixture()
def make_gamefield():
    def inner(matrix: list[list[int]]) -> dict[int, set[tuple[int, int]]]:
        result = {0: set(), 1: set(), 2: set()}
        for line_num, line in enumerate(matrix):
            for col_num, value in enumerate(line):
                result[value].add((col_num, line_num))
        return result
    return inner


@pytest.fixture
def make_game(make_gamefield):
    def inner(field):
        game = Game()
        game._gamefield._board = make_gamefield(field)
        return game
    return inner
