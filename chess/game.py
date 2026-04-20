from chess.board import Board
from chess.move import Move
from chess.player import Player


class Game:
    def __init__(self):
        self.player_white = None
        self.player_black = None
        self.board = None

        self.moves: list[Move] = []
        self.winner = None
        self.draw = False

        self.prepare()

    def prepare(self):
        self.player_white = Player(color="white")
        self.player_black = Player(color="black")
        self.board = Board()

    def start(self):
        pass

    def do_move(self):
        while True:
            user_input = input(f"Player {self.current_player.color} to make the move: ")

            try:
                move = Move(from_to=user_input, board=self.board, color=self.current_player.color)
            except ValueError as e:
                print(f"{e}. Try again.")
                continue

            self.moves.append(move)

            if move.is_quit:
                self.winner = self.other_player
            elif move.is_draw_proposal:
                self.handle_draw()
            else:
                self.board.move_piece(move.from_pos, move.to_pos)
            break

    def handle_draw(self):
        answer = input(f"Player {self.other_player.color}, do you accept the draw? (YES/NO): ").upper()
        if answer == "YES":
            self.draw = True
        else:
            print("Draw refused. Game continues.")
            self.moves.pop()

    @property
    def current_player(self):
        if len(self.moves) % 2 == 0:
            return self.player_white
        else:
            return self.player_black

    @property
    def other_player(self):
        if self.current_player == self.player_white:
            return self.player_black
        else:
            return self.player_white

    def is_over(self):
        if len(self.moves) > 0 and self.moves[-1].is_quit:
            return True
        if self.draw:
            return True
        return False

