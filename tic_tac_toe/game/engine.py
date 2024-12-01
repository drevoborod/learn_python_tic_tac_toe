from enum import Enum
from random import randint, choice, shuffle
from typing import Self

from tic_tac_toe.game.interface import ask_coordinates, CoordinatesError, GameField, HEIGHT, WIDTH


# How many items should be placed in one row to win the game:
WIN_LEN = 3

# Text titles of different kinds of players:
HUMAN_PLAYER = "human"
COMPUTER_PLAYER = "computer"


class NoWinnerError(Exception): pass


class Game:

    def __init__(self, board_width: int = WIDTH, board_height: int = HEIGHT, win_len: int = WIN_LEN):
        self._gamefield: GameField = GameField(width=board_width, height=board_height)
        self._win_len: int = win_len
        self.human_role: int | None = None
        self.cpu_role: int | None = None
        self._winner: str | None = None

    def assign_player_roles(self) -> Self:
        """
        Determines which player (human/computer) will play which figure (zero/cross). Should be run firstly.

        """

        roles = [self._gamefield.cross, self._gamefield.zero]
        shuffle(roles)
        self.human_role = roles[0]
        self.cpu_role = roles[1]
        return self

    @property
    def human_moves_first(self) -> bool:
        if self.human_role == self._gamefield.cross:
            return True
        return False

    @property
    def winner(self) -> str:
        """
        Returns winner's text representation.

        :return: text representation of a player who wins ("human" or "computer" by default).

        """
        return self._winner

    def draw_field(self) -> None:
        """
        Draws the board.

        """
        self._gamefield.draw()

    def make_human_move(self) -> bool:
        """
        Makes human player's move and returns True if the human wins.

        :return: True if the human wins, False otherwise.

        """
        self._empty_cells_remain()
        while True:
            try:
                x, y = ask_coordinates()
                self._gamefield.set(x, y, self.human_role)
            except CoordinatesError as err:
                print(err)
                continue
            break
        victory = self._check_victory(self.human_role)
        if victory:
            self._winner = HUMAN_PLAYER
        return victory

    def make_cpu_move(self) -> bool:
        """
        Makes computer's move and returns True if the computer wins.

        :return: True if the computer wins, False otherwise.

        """
        empty_cells = self._empty_cells_remain()
        self._gamefield.set(*choice(empty_cells), self.cpu_role)
        victory = self._check_victory(self.cpu_role)
        if victory:
            self._winner = COMPUTER_PLAYER
        return victory

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

    def _empty_cells_remain(self) -> list[tuple[int, int]]:
        """
        Returns list with empty cells coordinates. If no empty cells left, raises NoWinnerError.

        :return: list of 2-tuples with empty cells: [(x, y), (x, y), ...]. Numbers start with 1.
        :raise: NoWinnerError if there are no empty cells left.
        """
        empty_cells = list(self._gamefield.filter_cells(self._gamefield.empty))
        if not empty_cells:
            raise NoWinnerError
        return empty_cells
