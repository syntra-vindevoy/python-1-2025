"""
Rook (Tower) module.

The rook moves any number of squares along a row or column (horizontally or
vertically). It cannot jump over other pieces — all intermediate squares must
be empty.

The rook also participates in castling (rochade) with the king. The has_moved
attribute tracks whether the rook has moved, which is required to determine
castling eligibility. The actual castling logic is in King._can_castle and
Board.move_piece.
"""

from chess.piece import Piece


class Rook(Piece):
    """
    Represents a rook (tower) chess piece.

    Attributes:
        has_moved: Tracks whether this rook has moved from its original position.
                   Set to True after the first move. Used for castling eligibility.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)
        self.has_moved = False

    def is_authorized_move(self, *, from_pos, to_pos, board):
        """
        Check whether this rook can move from from_pos to to_pos.

        The rook moves in straight lines: either the column changes (horizontal)
        or the row changes (vertical), but not both. All squares between the
        source and destination must be empty.

        Args:
            from_pos: Current position of the rook.
            to_pos: Target position.
            board: The Board, used to check for pieces in the path.

        Returns:
            True if the move is a valid straight-line move with a clear path.
        """
        col_diff = to_pos.hor() - from_pos.hor()  # horizontal distance (+ = right, - = left)
        row_diff = to_pos.ver() - from_pos.ver()  # vertical distance (+ = up, - = down)

        # Rook can only move in straight lines: either horizontally (row stays the same,
        # column changes) or vertically (column stays the same, row changes).
        # If both change, it's a diagonal move — not allowed for a rook.
        if col_diff != 0 and row_diff != 0:

            return False

        # All squares between source and destination must be empty

        return self.path_is_clear(
            positions=self._intermediate_positions(from_pos=from_pos, to_pos=to_pos),
            board=board
        )
