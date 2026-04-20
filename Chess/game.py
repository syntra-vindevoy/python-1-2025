from Chess.board import Board
from Chess.player import Player

class Game:
    def __init__(self):
        self.player_white = None
        self.player_black = None

    def prepare(self):
        self.player_white = Player(color="white")
        self.player_black = Player(color="black")
        self.board = Board()

    def start(self): # player1: Player, player2: Player
        pass

    def do_move(self, *, move):
        pass

    def is_over(self):  #King falls, king can't move without getting caught, both players agree to a draw
        pass

