from chess.piece import Piece


class Queen(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # Must move along a row, column, or diagonal
        if col_diff != 0 and row_diff != 0 and abs(col_diff) != abs(row_diff):
            return False

        return self.path_is_clear(self._intermediate_positions(from_pos, to_pos), board)