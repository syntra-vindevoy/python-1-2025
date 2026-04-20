from chess.piece import Piece
from chess.position import Position


class King(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)
        self.has_moved = False

    def is_authorized_move(self, from_pos, to_pos, board):
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        opponent_color = "black" if self.color == "white" else "white"

        # Castling: king moves 2 squares horizontally
        if abs(col_diff) == 2 and row_diff == 0:
            return self._can_castle(from_pos, to_pos, board, col_diff, opponent_color)

        # King moves one square in any direction
        if abs(col_diff) > 1 or abs(row_diff) > 1:
            return False

        # King cannot move to a square under attack
        return not board.is_under_attack(to_pos, opponent_color)

    def _can_castle(self, from_pos, to_pos, board, col_diff, opponent_color):
        if self.has_moved:
            return False

        # King must not be in check
        if board.is_under_attack(from_pos, opponent_color):
            return False

        row = from_pos.ver()
        letters = "ABCDEFGH"

        # Kingside castling (king moves right)
        if col_diff > 0:
            rook_pos = Position(strpos=f"H{row}")
        # Queenside castling (king moves left)
        else:
            rook_pos = Position(strpos=f"A{row}")

        rook = board.piece_at(rook_pos)
        if rook is None or not hasattr(rook, 'has_moved') or rook.has_moved:
            return False

        # Path between king and rook must be clear
        if not rook.path_is_clear(rook._intermediate_positions(from_pos, rook_pos), board):
            return False

        # King must not pass through or land on an attacked square
        step = 1 if col_diff > 0 else -1
        for c in range(from_pos.hor() + step, to_pos.hor() + step, step):
            pos = Position(strpos=f"{letters[c - 1]}{row}")
            if board.is_under_attack(pos, opponent_color):
                return False

        return True