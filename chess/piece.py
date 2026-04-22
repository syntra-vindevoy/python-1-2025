"""
Piece module.

Defines the abstract base class for all chess pieces. Every concrete piece
(Rook, Knight, Bishop, Queen, King, Pawn) must inherit from Piece and implement
the is_authorized_move method.

This class also provides shared utility methods for path calculation and
path clearance checking, used by sliding pieces (Rook, Bishop, Queen) and Pawn.
"""

from abc import ABC, abstractmethod

from chess.position import Position


class Piece(ABC):
    """
    Abstract base class for all chess pieces.

    Attributes:
        color: The color of the piece ("white" or "black").
    """

    def __init__(self, *, color: str):
        """
        Initialize a piece with a color.

        Args:
            color: "white" or "black".
        """
        self.color = color

    @abstractmethod
    def is_authorized_move(self, *, from_pos, to_pos, board):
        """
        Check whether this piece can move from from_pos to to_pos on the given board.

        This method only validates the piece-specific movement rules (e.g. a rook moves
        in straight lines, a knight moves in an L-shape). It does NOT check:
        - Whether the source has a piece of the correct color (checked in Move)
        - Whether the destination has a friendly piece (checked in Move)
        - Whether the move leaves the own king in check (checked in Move)

        Args:
            from_pos: The Position where the piece currently stands.
            to_pos: The Position where the piece wants to move.
            board: The Board object, used to check for pieces along the path.

        Returns:
            True if the piece's movement rules allow this move, False otherwise.
        """
        pass

    def attacks_square(self, *, from_pos, to_pos, board):
        """
        Check whether this piece attacks (threatens) a given square.

        For most pieces, attacking a square is the same as being able to move there.
        The pawn is the exception: it attacks diagonally regardless of whether the
        target square is occupied, but it moves forward only to empty squares.

        This method is used by is_under_attack to determine if a square is threatened,
        which matters for king movement and castling safety checks.

        Args:
            from_pos: The Position where the piece currently stands.
            to_pos: The target Position to check.
            board: The Board object.

        Returns:
            True if this piece attacks the target square.
        """

        return self.is_authorized_move(from_pos=from_pos, to_pos=to_pos, board=board)

    def _intermediate_positions(self, *, from_pos, to_pos):
        """
        Calculate all positions between from_pos and to_pos (exclusive of both endpoints).

        Works for horizontal, vertical, and diagonal lines. The method determines the
        direction of movement by computing the sign of the column and row differences,
        then walks step by step from from_pos toward to_pos, collecting each intermediate
        position.

        Example: from A1 to A4 returns [A2, A3] (the squares the piece passes through).
        Example: from A1 to D4 returns [B2, C3] (diagonal intermediate squares).

        Args:
            from_pos: The starting Position (not included in the result).
            to_pos: The ending Position (not included in the result).

        Returns:
            A list of Position objects representing the squares between from and to.
        """
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        # Determine step direction: -1, 0, or +1 for each axis
        step_col = (1 if col_diff > 0 else -1) if col_diff != 0 else 0
        step_row = (1 if row_diff > 0 else -1) if row_diff != 0 else 0
        letters = "ABCDEFGH"

        positions = []
        col = from_pos.hor() + step_col
        row = from_pos.ver() + step_row

        # Walk from from_pos toward to_pos, collecting intermediate squares
        while col != to_pos.hor() or row != to_pos.ver():
            positions.append(Position(strpos=f"{letters[col - 1]}{row}"))
            col += step_col
            row += step_row

        return positions

    def path_is_clear(self, *, positions, board):
        """
        Check whether all given positions are empty (no piece occupying them).

        Used by sliding pieces (Rook, Bishop, Queen) and Pawn (two-square move)
        to verify that no piece blocks the path between the start and destination.

        Args:
            positions: A list of Position objects to check (typically from _intermediate_positions).
            board: The Board object to check piece occupancy.

        Returns:
            True if all positions are empty, False if any position is occupied.
        """
        for pos in positions:
            if board.piece_at(position=pos) is not None:

                return False

        return True
