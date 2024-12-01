from typing import Callable

from tic_tac_toe.game.engine import Game, NoWinnerError


def play(game: Game):
    """
    Main game loop. Continues until victory.

    """

    def _make_move(func: Callable):
        try:
            result = func()
        except NoWinnerError:
            print("No winner in this game!\n")
            return True
        finally:
            game.draw_field()
        if game.winner:
            print(f"{game.winner.title()} wins!\n")
        return result

    functions = (game.make_cpu_move, game.make_human_move)
    human_first = game.human_moves_first
    if human_first:
        print("\nYou play with 'X' and you begin.")
    else:
        print("\nYou play with '0' and your opponent begins.")
    first_mover, second_mover = functions[human_first], functions[not human_first]
    while True:
        if _make_move(first_mover):
            break
        print("=" * 20)
        if _make_move(second_mover):
            break
        print("=" * 20)


if __name__ == "__main__":
    play(Game().init_game())