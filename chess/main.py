from chess.game import Game
from chess.move import Move

game = Game()

game.start()

while not game.is_over():
    m = Move()
    game.do_move(move=m)

print("Game is over")
print("The winner is:")