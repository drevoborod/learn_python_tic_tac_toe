from tic_tac_toe.game.engine import Game
from tic_tac_toe.game.players import Human, Computer


def play():
    game = Game()
    game.init_players(Human, Computer)
    if game.first_players_name == Human.name:
        print("\nYou play with 'X' and you begin.")
    else:
        print("\nYou play with '0' and your opponent begins.")
    for result in game.play():
        game.draw_field()
        print("=" * 20)
        if result:
            print(result)


if __name__ == "__main__":
    play()