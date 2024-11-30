import re

from .constants import Dimensions, PseudoGraphics


class CoordinatesError(Exception): pass


class GameField:
    """
    Represents game's field where game progress will be drawn.
    """

    empty = None
    zero = 0
    cross = 1

    mapping = {
        empty: PseudoGraphics.EMPTY,
        zero: PseudoGraphics.ZERO,
        cross: PseudoGraphics.CROSS,
    }

    def __init__(self):
        self._gamefield = [[self.empty for _ in range(Dimensions.WIDTH)] for _ in range(Dimensions.HEIGHT)]


    @property
    def gamefield(self):
        return self._gamefield

    def draw(self):
       """
       Draw the game field in the terminal.

       """
       for num, line in enumerate(self._gamefield):
           print(PseudoGraphics.VERTICAL_LINE.join(self.mapping[x] for x in line))
           if num < len(self._gamefield):
               print(f"{PseudoGraphics.HORIZONTAL_LINE}{''.join(PseudoGraphics.HORIZONTAL_LINE for _ in range(len(line)))}")

    def set(self, x: int, y: int, symbol: zero | cross):
        """
        Set new value in the cell of the game field.

        :param x: horizontal coordinate (starting with 1).
        :param y: vertical coordinate (starting with 1).
        :param symbol: one of `zero` or `cross` value.

        """
        if 1 > x or x > len(self._gamefield[0]):
            raise CoordinatesError("Horizontal coordinate is out of bounds")
        if 1 > y or y > len(self._gamefield):
            raise CoordinatesError("Vertical coordinate is out of bounds")
        if self._gamefield[y - 1][x - 1] is not self.empty:
            raise CoordinatesError("Attempt to write to already filled cell")
        self._gamefield[y - 1][x - 1] = symbol


def ask_coordinates(message: str = None):
    """
    Asks the player to enter move coordinates in the console.

    :param message: optional prompt text.
    :return:
    """
    if not message:
        message = "Enter X and Y coordinates separated by space: "
    data = input(message)
    parsed = re.match(r"^(\d+)\s+(\d+)", data)
    if parsed:
        return [int(x) for x in parsed.groups()]
    raise CoordinatesError("Incorrect coordinates format, please try again.")
