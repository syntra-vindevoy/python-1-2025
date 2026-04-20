from Chess.board import Board
from Chess.player import Player

class Game:
    def __init__(self):
        self.player_white = None
        self.player_black = None

        #self.moves: list[Moves] = []

        self.prepare()

    def prepare(self):
        self.player_white = Player(color="white")
        self.player_black = Player(color="black")
        self.board = Board()

    def start(self): # player1: Player, player2: Player
        pass

    def do_move(self, *, move):
        i = input(f"Player {self.player_white.color} to make the move: ")

    def current_player(self):
        # if len(self.moves) % 2 == 0:
        #     return self.player_white
        # else:
        #     return self.player_black
        return self.player_white if len(self.moves) % 2 == 0 else self.player_black

    def is_over(self):  #King falls, king can't move without getting caught, both players agree to a draw
        pass

