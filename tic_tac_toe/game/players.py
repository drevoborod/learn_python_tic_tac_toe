from random import choice
from typing import Protocol

from tic_tac_toe.game.interface import ask_coordinates, GameField, CoordinatesError


class Player(Protocol):
    name: str

    @staticmethod
    def next_move(gamefield: GameField) -> tuple[int, int]:
        """Return player's next move coordinates."""


class Computer(Player):
    name = "computer"

    @staticmethod
    def next_move(gamefield: GameField) -> tuple[int, int]:
        empty_cells = list(gamefield.filter_cells(gamefield.empty))
        return choice(empty_cells)


class Human(Player):
    name = "human"

    @staticmethod
    def next_move(gamefield: GameField) -> tuple[int, int]:
        while True:
            try:
                x, y = ask_coordinates()
            except CoordinatesError as err:
                print(err)
            else:
                if not gamefield.cell_exists(x, y):
                    print("Coordinates are out of bounds!")
                    continue
                if gamefield.is_cell_accessible(x, y):
                    return x, y
                print("Cell is occupied!")

