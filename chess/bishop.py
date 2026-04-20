"""
Bishop module.

The bishop moves any number of squares diagonally. It cannot jump over other
pieces — all intermediate squares must be empty.

Because the bishop only moves diagonally, it always stays on the same color
square it started on (light or dark). This is relevant for the insufficient
material draw rule.
"""

from chess.piece import Piece


class Bishop(Piece):
    """
    Represents a bishop chess piece.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        """
        Check whether this bishop can move from from_pos to to_pos.

        The bishop moves diagonally: the absolute column difference must equal
        the absolute row difference. All intermediate squares must be empty.

        Args:
            from_pos: Current position of the bishop.
            to_pos: Target position.
            board: The Board, used to check for pieces in the path.

        Returns:
            True if the move is a valid diagonal move with a clear path.
        """
        col_diff = to_pos.hor() - from_pos.hor()  # horizontal distance
        row_diff = to_pos.ver() - from_pos.ver()  # vertical distance

        # A diagonal move means equal horizontal and vertical distance.
        # E.g. moving from C1 to F4 is 3 columns right and 3 rows up — valid.
        # Moving from C1 to F3 is 3 columns right and 2 rows up — not diagonal.
        if abs(col_diff) != abs(row_diff):
            return False

        # All diagonal squares between source and destination must be empty
        return self.path_is_clear(self._intermediate_positions(from_pos, to_pos), board)