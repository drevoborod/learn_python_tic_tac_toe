class Dimensions:
    """
    Dimensions of the game field.
    """
    WIDTH = 3
    HEIGHT = 3
    WIN_LEN = 3


class PseudoGraphics:
    """
    Pseudo graphical primitives of which the game field consists.
    All should be instances of str!
    """
    VERTICAL_LINE = "︱"
    HORIZONTAL_LINE = "𝄖"
    ZERO = "0"
    CROSS = "X"
    EMPTY = " "


class Players:
    human = "human"
    computer = "computer"
