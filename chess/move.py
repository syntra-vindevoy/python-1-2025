import re

from chess.position import Position


class Move:
    pattern = re.compile(r'^[A-H][1-8][- ][A-H][1-8]$')

    def __init__(self, from_to: str, board=None, color=None):
        assert isinstance(from_to, str), "from_to must be a string"

        self.from_to = from_to.upper()
        self.is_quit = self.from_to == "QUIT"
        self.is_draw_proposal = self.from_to == "DRAW"

        if not self.is_quit and not self.is_draw_proposal:
            if not self.is_valid_move():
                raise ValueError(f"Invalid move syntax: {from_to}. Expected format: A1-A2 (letter A-H, digit 1-8, dash or space, letter A-H, digit 1-8), QUIT or DRAW")

            self.from_pos = Position(strpos=from_to[:2])
            self.to_pos = Position(strpos=from_to[3:])
            self.board = board
            self.color = color

            if not self.is_authorized_move():
                raise ValueError(self.unauthorized_reason)

    def is_valid_move(self):
        return bool(self.pattern.match(self.from_to))

    def is_authorized_move(self):
        if self.from_pos == self.to_pos:
            self.unauthorized_reason = "From and to positions are the same"
            return False

        piece = self.board.piece_at(self.from_pos)

        if piece is None:
            self.unauthorized_reason = f"No piece at {self.from_pos.strpos}"
            return False

        if piece.color != self.color:
            self.unauthorized_reason = f"Piece at {self.from_pos.strpos} belongs to the other player"
            return False

        target_piece = self.board.piece_at(self.to_pos)

        if target_piece is not None and target_piece.color == self.color:
            self.unauthorized_reason = f"Cannot move to {self.to_pos.strpos}: occupied by your own piece"
            return False

        if not piece.is_authorized_move(self.from_pos, self.to_pos, self.board):
            self.unauthorized_reason = f"This piece cannot move from {self.from_pos.strpos} to {self.to_pos.strpos}"
            return False

        return True
