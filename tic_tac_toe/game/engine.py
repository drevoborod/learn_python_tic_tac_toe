from itertools import cycle
from random import shuffle
from typing import Self, Iterator

from tic_tac_toe.game.interface import GameField, HEIGHT, WIDTH
from tic_tac_toe.game.players import Player

# How many items should be placed in one row to win the game:
WIN_LEN = 3


class GameError(Exception): pass


class Game:

    def __init__(self, board_width: int = WIDTH, board_height: int = HEIGHT, win_len: int = WIN_LEN):
        self._gamefield: GameField = GameField(width=board_width, height=board_height)
        self._win_len: int = win_len
        self._players: dict[int, Player] = {}
        self._winner: Player | None = None

    def init_players(self, player1, player2) -> Self:
        """
        Determines which player will play which figure (zero/cross). Should be run firstly.

        """
        roles = [self._gamefield.cross, self._gamefield.zero]
        shuffle(roles)
        self._players[roles[0]] = player1
        self._players[roles[1]] = player2
        return self

    @property
    def first_players_name(self):
        self._check_players_ready()
        return self._players[self._gamefield.cross].name

    def draw_field(self) -> None:
        """
        Draws the board.

        """
        self._gamefield.draw()

    def play(self) -> Iterator[str]:
        """
        Runs main game cycle and returns message which explains the results.

        """
        self._check_players_ready()
        # The player playing with "X" should always start first:
        for role in cycle(sorted(self._players, key=lambda k: 0 if k == self._gamefield.cross else 1)):
            if not self._empty_cells_remain():
                yield "No moves left! There is no winner!"
                break
            x, y = self._players[role].next_move(self._gamefield)
            self._gamefield.set(x, y, role)
            if self._check_victory(role):
                yield f"{self._players[role].name.title()} wins!"
                break
            yield ""

    def _check_victory(self, role: int) -> bool:
        """
        Returns True if provided role wins the game.

        :param role: player role to check.
        :return: True if provided role wins, False otherwise.

        """
        for cell in self._gamefield.filter_cells(role):
            # Check if there are winning chains in four dimensions from located cell:
            # eastwards, south-east, southwards, south-west.
            for steps in ((1, 0), (1, 1), (0, 1), (-1, 1)):
                chain_len = self._gamefield.locate_cells_count_by_offset(*cell, *steps, role)
                if chain_len >= self._win_len:
                    return True
        return False

    def _empty_cells_remain(self) -> bool:
        empty_cells = list(self._gamefield.filter_cells(self._gamefield.empty))
        if empty_cells:
            return True
        return False

    def _check_players_ready(self):
        if not self._players:
            raise GameError("No players set!")
