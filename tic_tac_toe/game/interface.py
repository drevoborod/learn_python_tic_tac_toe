import re
from collections.abc import Iterator


# Pseudographical primitives:
VERTICAL_LINE = "︱"
HORIZONTAL_LINE = "𝄖"
ZERO = "0"
CROSS = "X"
EMPTY = " "

# Dimensions of a game field:
WIDTH = 3
HEIGHT = 3


class CoordinatesError(Exception): pass


class GameField:
    """
    Represents game's field where game progress will be drawn.
    """

    # Empty cell contents:
    empty = 0
    # Cell with "0" contents:
    zero = 1
    # Cell with "X" contents:
    cross = 2

    mapping = {
        empty: EMPTY,
        zero: ZERO,
        cross: CROSS,
    }

    def __init__(self, width: int = WIDTH, height: int = HEIGHT):
        self.width = width
        self.height = height
        self._board: dict[tuple[int, int], int] = {}

    def get(self, x: int, y: int) -> int:
        """
        Returns value of a cell by provided coordinates.

        :param x: horizontal coordinate.
        :param y: vertical coordinate.
        :return: cell value (one of empty/zero/cross).
        :raise: CoordinatesError if such cell does not exist.

        """
        if not self.cell_exists(x, y):
            raise CoordinatesError("Coordinates are out of bounds")
        if cell := self._board.get((x, y)):
            return cell
        return self.empty

    def set(self, x: int, y: int, symbol: int) -> None:
        """
        Set new value in the cell of the game field.

        :param x: horizontal coordinate (starting with 0).
        :param y: vertical coordinate (starting with 0).
        :param symbol: one of `zero` or `cross` value.
        :raise: CoordinatesError if any of the coordinates is out of bounds.

        """
        cell_data = self.get(x, y)
        if cell_data != self.empty:
            raise CoordinatesError("Attempt to write to non-empty cell")
        self._board[(x, y)] = symbol

    def filter_cells(self, cell_contents: int) -> Iterator[tuple[int, int]]:
        """
        Returns an iterator with cells coordinates for cells with corresponding contents.

        :param cell_contents: cells containing what type of data should be returned (empty, zero, cross).
        :return: iterator of cell coordinates as 2-tuples: (x, y), (x, y), ....

        """
        if cell_contents in (self.cross, self.zero):
            for key, value in self._board.items():
                if value == cell_contents:
                    yield key
        else:
            for line_num in range(self.height):
                for col_num in range(self.width):
                    if (value := (col_num, line_num)) not in self._board:
                        yield value

    def locate_cells_count_by_offset(self, x: int, y: int, x_offset: int, y_offset: int, role: int) -> int:
        """
        Returns count of cells with provided role which form solid chain in provided direction.
        Direction is formed by offsets: every next checked cell lays in (x + x_offset, y + y_offset) position.

        :param x: horizontal coordinate.
        :param y: vertical coordinate.
        :param x_offset: value by which horizontal coordinate will be increased on every search iteration.
        :param y_offset: value by which vertical coordinate will be increased on every search iteration.
        :param role: cells of which role should be located.
        :return: count of cells forming a solid line in desired direction. Count includes the cell from which counting starts.
        """
        count = 0
        while self.cell_exists(x, y):
            if self.get(x, y) == role:
                count += 1
            else:
                return count
            x += x_offset
            y += y_offset
        return count

    def cell_exists(self, x: int, y: int) -> bool:
        """
        Returns True if provided coordinates exist on the board.

        :param x: horizontal coordinate.
        :param y: vertical coordinate.
        :return: True if provided coordinates are in a correct range, False otherwise.
        """
        if x < 0 or x >= self.width:
            return False
        if y < 0 or y >= self.height:
            return False
        return True

    def draw(self) -> None:
        """
        Draw the game field in the terminal.

        """
        for line_num in range(self.height):
            print(VERTICAL_LINE.join(self.mapping[self.get(col_num, line_num)] for col_num in range(self.width)))
            if line_num < self.height - 1:
                print(f"{HORIZONTAL_LINE}{''.join(HORIZONTAL_LINE for _ in range(self.width))}")


def ask_coordinates(message: str = None) -> tuple[int, int]:
    """
    Asks the player to enter move coordinates in the console.
    Provided values are returned as 2-tuple where both values are less by 1 then provided by user.

    :param message: optional prompt text.
    :return: 2-tuple of a coordinates: (x, y).
    :raise: CoordinatesError if coordinates are entered in wrong format.
    """
    if not message:
        message = "Enter X and Y coordinates separated by space. Values should be above 0: "
    data = input(message)
    parsed = re.match(r"^(\d+)\s+(\d+)$", data.strip())
    if parsed:
        return tuple(int(x) - 1 for x in parsed.groups())
    raise CoordinatesError("Incorrect coordinates format, please try again.")
