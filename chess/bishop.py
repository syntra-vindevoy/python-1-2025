from chess.piece import Piece
from chess.position import Position


class Bishop(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # Must move diagonally
        if abs(col_diff) != abs(row_diff):
            return False

        # Check that the path is clear
        step_col = 1 if col_diff > 0 else -1
        step_row = 1 if row_diff > 0 else -1
        letters = "ABCDEFGH"

        col = from_pos.hor() + step_col
        row = from_pos.ver() + step_row

        while col != to_pos.hor() or row != to_pos.ver():
            middle_pos = Position(strpos=f"{letters[col - 1]}{row}")
            if board.piece_at(middle_pos) is not None:
                return False
            col += step_col
            row += step_row

        return True