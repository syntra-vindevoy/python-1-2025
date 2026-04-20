from chess.piece import Piece


class King(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        col_diff = abs(to_pos.hor() - from_pos.hor())
        row_diff = abs(to_pos.ver() - from_pos.ver())

        # King moves one square in any direction
        # TODO: castling
        return col_diff <= 1 and row_diff <= 1