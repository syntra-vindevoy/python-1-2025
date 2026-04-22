"""
Pawn module.

The pawn is the most complex piece in terms of movement rules:
- Moves forward one square (cannot capture forward).
- Moves forward two squares from its starting row (both squares must be empty).
- Captures diagonally one square forward.
- En-passant: captures an opponent's pawn that just moved two squares forward
  and landed beside this pawn (special rule, uses board.last_move).
- Promotion is handled by Board.move_piece when the pawn reaches the last row.

Direction: white pawns move upward (row increases), black pawns move downward
(row decreases).
"""

from chess.piece import Piece
from chess.position import Position


class Pawn(Piece):
    """
    Represents a pawn chess piece.

    The pawn moves forward but captures diagonally. It is the only piece that
    moves differently when capturing vs. not capturing.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)

    def is_authorized_move(self, *, from_pos, to_pos, board):
        """
        Check whether this pawn can move from from_pos to to_pos.

        The pawn has four possible move types:
        1. One square forward to an empty square.
        2. Two squares forward from the starting row (both squares must be empty).
        3. One square diagonally forward to capture an opponent's piece.
        4. En-passant: one square diagonally forward to an empty square, capturing
           an opponent's pawn that just advanced two squares on the previous turn.

        Args:
            from_pos: Current position of the pawn.
            to_pos: Target position.
            board: The Board, used to check occupancy and last move (for en-passant).

        Returns:
            True if the move is valid for a pawn.
        """
        # Direction: +1 for white (moving up), -1 for black (moving down)
        direction = 1 if self.color == "white" else -1
        # Starting row: row 2 for white, row 7 for black
        start_row = 2 if self.color == "white" else 7

        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        target_piece = board.piece_at(position=to_pos)

        # Move one square forward: must be same column and destination must be empty
        if col_diff == 0 and row_diff == direction and target_piece is None:

            return True

        # Move two squares forward from starting position:
        # must be same column, on the start row, and both the intermediate
        # square and destination must be empty.
        if col_diff == 0 and row_diff == 2 * direction and from_pos.ver() == start_row:
            if self.path_is_clear(
                positions=self._intermediate_positions(from_pos=from_pos, to_pos=to_pos),
                board=board
            ) and target_piece is None:

                return True

        # Diagonal capture: move one column left or right, one row forward
        if abs(col_diff) == 1 and row_diff == direction:
            # Standard capture: there is an opponent's piece at the destination
            if target_piece is not None and target_piece.color != self.color:

                return True

            # En-passant: the destination square is empty, but an opponent's pawn
            # is beside us (same row) and it just advanced two squares on the
            # previous turn. The captured pawn is on our row, on the destination column.
            # Conditions:
            #   - Destination is empty
            #   - There was a previous move (board.last_move is not None)
            #   - The last moved piece was an opponent's pawn
            #   - That pawn moved exactly two squares (it was a double advance)
            #   - That pawn landed on the same column as our destination
            #     and on the same row as our current position
            if target_piece is None and board.last_move is not None:
                last_from, last_to, last_piece = board.last_move

                if isinstance(last_piece, Pawn) and last_piece.color != self.color:
                    if abs(last_to.ver() - last_from.ver()) == 2:
                        if last_to.hor() == to_pos.hor() and last_to.ver() == from_pos.ver():

                            return True

        return False

    def attacks_square(self, *, from_pos, to_pos, board):
        """
        Check whether this pawn attacks (threatens) a given square.

        A pawn attacks the two diagonal squares in front of it, regardless of
        whether those squares are occupied. This is different from is_authorized_move,
        which only allows diagonal movement when capturing an opponent's piece.

        This distinction matters for king safety: a king cannot move to a square
        that a pawn attacks, even if that square is currently empty.

        Args:
            from_pos: The Position where the pawn currently stands.
            to_pos: The target Position to check.
            board: The Board object (not used, but required by the interface).

        Returns:
            True if this pawn attacks the target square.
        """
        direction = 1 if self.color == "white" else -1

        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # A pawn attacks the two diagonal squares one row ahead
        return abs(col_diff) == 1 and row_diff == direction
