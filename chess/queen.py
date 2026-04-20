"""
Queen module.

The queen is the most powerful piece. It combines the movement of the rook
and bishop: it can move any number of squares along a row, column, or diagonal.
It cannot jump over other pieces — all intermediate squares must be empty.
"""

from chess.piece import Piece


class Queen(Piece):
    """
    Represents a queen chess piece.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, from_pos, to_pos, board):
        """
        Check whether this queen can move from from_pos to to_pos.

        The queen combines rook and bishop movement: it can move along a row
        (col changes, row stays), a column (row changes, col stays), or a
        diagonal (equal change in both). All intermediate squares must be empty.

        Args:
            from_pos: Current position of the queen.
            to_pos: Target position.
            board: The Board, used to check for pieces in the path.

        Returns:
            True if the move is along a valid line with a clear path.
        """
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # Must move along a row, column, or diagonal.
        # Row: row_diff == 0, col_diff != 0
        # Column: col_diff == 0, row_diff != 0
        # Diagonal: abs(col_diff) == abs(row_diff)
        # Anything else is invalid.
        if col_diff != 0 and row_diff != 0 and abs(col_diff) != abs(row_diff):
            return False

        return self.path_is_clear(self._intermediate_positions(from_pos, to_pos), board)