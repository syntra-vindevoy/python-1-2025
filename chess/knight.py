"""
Knight module.

The knight moves in an L-shape: two squares in one direction and one square
perpendicular (or vice versa). The knight is the only piece that can jump
over other pieces — intermediate squares are irrelevant.

Possible moves from any position form up to 8 destinations:
(+2,+1), (+2,-1), (-2,+1), (-2,-1), (+1,+2), (+1,-2), (-1,+2), (-1,-2).
"""

from chess.piece import Piece


class Knight(Piece):
    """
    Represents a knight chess piece.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, *, from_pos, to_pos, board):
        """
        Check whether this knight can move from from_pos to to_pos.

        The knight moves in an L-shape: the absolute column difference and row
        difference must be (2,1) or (1,2). The knight jumps over pieces, so
        no path clearance check is needed.

        Args:
            from_pos: Current position of the knight.
            to_pos: Target position.
            board: The Board (not used for knights, but required by the interface).

        Returns:
            True if the move forms a valid L-shape.
        """
        col_diff = abs(to_pos.hor() - from_pos.hor())  # absolute horizontal distance
        row_diff = abs(to_pos.ver() - from_pos.ver())  # absolute vertical distance

        # The knight moves in an L-shape: 2 squares in one direction and 1 in the other.
        # E.g. from B1 to C3 (1 right, 2 up) or from B1 to A3 (1 left, 2 up).
        # The knight is the only piece that jumps over other pieces — no path check needed.

        return (col_diff == 2 and row_diff == 1) or (col_diff == 1 and row_diff == 2)
