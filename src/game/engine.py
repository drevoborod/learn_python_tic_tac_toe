from random import randint, choice

from .interface import ask_coordinates, CoordinatesError, GameField
from .constants import Dimensions, Players


class NoWinnerError(Exception): pass


class Game:

    def __init__(self):
        self._gamefield = GameField()
        self._human_role = None
        self._cpu_role = None
        self._winner = None

    def init_game(self):
        """
        Prepares the game. Should be run firstly.

        """

        roles = (self._gamefield.cross, self._gamefield.zero)
        selection = randint(0, 1)
        self._human_role = roles[selection]
        self._cpu_role = roles[not selection]
        return self

    @property
    def human_role(self):
        if self._human_role is None:
            self.init_game()
        return self._human_role

    @property
    def cpu_role(self):
        if self._cpu_role is None:
            self.init_game()
        return self._cpu_role

    @property
    def human_moves_first(self) -> bool:
        """
        Checks whether the human player should move first or not.

        :return: True if human player's move should be done first, False otherwise.
        """
        if self.human_role == self._gamefield.cross:
            return True
        return False

    @property
    def winner(self) -> str:
        return self._winner

    def draw_field(self):
        self._gamefield.draw()

    def make_human_move(self) -> bool:
        """
        Makes human player's move and returns True if the human wins.

        :return: True if the human wins, False otherwise.
        """
        self._empty_cells()
        while True:
            try:
                x, y = ask_coordinates()
                self._gamefield.set(x, y, self._human_role)
            except CoordinatesError as err:
                print(err)
                continue
            break
        victory = self._check_victory(self.human_role)
        if victory:
            self._winner = Players.human
        return victory

    def make_cpu_move(self) -> bool:
        """
        Makes computer's move and returns True if the computer wins.

        :return: True if the computer wins, False otherwise.
        """
        empty_cells = self._empty_cells()
        self._gamefield.set(*choice(empty_cells), self.cpu_role)
        victory = self._check_victory(self.cpu_role)
        if victory:
            self._winner = Players.computer
        return victory

    def _check_victory(self, role: int) -> bool:
        """
        Returns True if provided role wins the game.

        :param role: player to check.
        :return: True if player wins, False otherwise.
        """
        def _locate_chain(x: int, y: int, x_step: int, y_step: int) -> bool:
            count = 1
            while True:
                x += x_step
                y += y_step
                if (not (0 <= x < len(self._gamefield.gamefield[0]))) or (not (0 <= y < len(self._gamefield.gamefield))):
                    return False
                if self._gamefield.gamefield[y][x] == role:
                    count += 1
                else:
                    return False
                if count == Dimensions.WIN_LEN:
                    return True

        for line_num, line in enumerate(self._gamefield.gamefield):
            for col_num, cell in enumerate(line):
                if cell == role:
                    # Check if there are winning chains in four dimensions from located cell:
                    # eastwards, south-east, southwards, south-west.
                    for steps in ((1, 0), (1, 1), (0, 1), (-1, 1)):
                        if _locate_chain(col_num, line_num, *steps):
                            return True
        return False

    def _empty_cells(self) -> list[tuple[int, int]]:
        """
        Returns list with empty cells coordinates (x, y). If no empty cells left, raises NoWinnerError.

        :return:
        """
        empty_cells = []
        for line_num, line in enumerate(self._gamefield.gamefield, start=1):
            for col_num, column in enumerate(line, start=1):
                if column is self._gamefield.empty:
                    empty_cells.append((col_num, line_num))
        if not empty_cells:
            raise NoWinnerError
        return empty_cells

