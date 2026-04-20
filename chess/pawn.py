from chess.piece import Piece
from chess.position import Position


class Pawn(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        direction = 1 if self.color == "white" else -1
        start_row = 2 if self.color == "white" else 7

        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        target_piece = board.piece_at(to_pos)

        # Move one square forward
        if col_diff == 0 and row_diff == direction and target_piece is None:
            return True

        # Move two squares forward from starting position
        if col_diff == 0 and row_diff == 2 * direction and from_pos.ver() == start_row:
            if self.path_is_clear(self._intermediate_positions(from_pos, to_pos), board) and target_piece is None:
                return True

        # Capture diagonally
        if abs(col_diff) == 1 and row_diff == direction:
            if target_piece is not None and target_piece.color != self.color:
                return True

            # En-passant: capture a pawn that just moved two squares forward
            if target_piece is None and board.last_move is not None:
                last_from, last_to, last_piece = board.last_move
                if isinstance(last_piece, Pawn) and last_piece.color != self.color:
                    if abs(last_to.ver() - last_from.ver()) == 2:
                        if last_to.hor() == to_pos.hor() and last_to.ver() == from_pos.ver():
                            return True

        return False
