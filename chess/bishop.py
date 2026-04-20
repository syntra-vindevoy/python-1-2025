from chess.piece import Piece


class Bishop(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # Must move diagonally
        if abs(col_diff) != abs(row_diff):
            return False

        return self.path_is_clear(self._intermediate_positions(from_pos, to_pos), board)