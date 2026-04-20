from chess.board import Board
from chess.player import Player


class Game:
    def __init__(self):
        self.player_white = None
        self.player_black = None
        self.board = None

        self.prepare()

    def prepare(self):
        self.player_white = Player(color="white")
        self.player_black = Player(color="black")
        self.board = Board()

    def start(self):
        pass

    def do_move(self, *, move):
        pass

    def is_over(self):
        return False

