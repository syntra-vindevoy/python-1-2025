from chess.game import Game
from chess.move import Move

game = Game()

game.start()

while not game.is_over():
    m = Move()
    game.do_move(move=m)

print("Game is over")
if game.draw:
    print("The game ended in a draw. No winner.")
else:
    print(f"The winner is: {game.winner.name}")