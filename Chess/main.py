from Chess.game import Game
from Chess.move import Move
from Chess.player import Player

game = Game(player1=Player(), player2=Player())

game.start()

while not game.is_over():
    m = Move()
    game.do_move()