"""
King module.

The king moves one square in any direction (horizontally, vertically, or
diagonally). The king has two additional constraints:
- It cannot move to a square that is under attack by an opponent's piece.
- It can perform castling (rochade) with a rook under specific conditions.

Castling is a special move where the king moves two squares toward a rook,
and the rook moves to the other side of the king. Conditions:
1. Neither the king nor the rook has moved previously.
2. The king is not currently in check.
3. All squares between king and rook are empty.
4. The king does not pass through or land on an attacked square.
"""

from chess.piece import Piece
from chess.position import Position


class King(Piece):
    """
    Represents a king chess piece.

    Attributes:
        has_moved: Tracks whether the king has moved from its original position.
                   Set to True after the first move. Used for castling eligibility.
    """

    def __init__(self, *, color: str):
        super().__init__(color=color)
        self.has_moved = False

    def is_authorized_move(self, from_pos, to_pos, board):
        """
        Check whether this king can move from from_pos to to_pos.

        Handles both normal moves (one square in any direction) and castling
        (two squares horizontally). The king can never move to a square that
        is under attack.

        Args:
            from_pos: Current position of the king.
            to_pos: Target position.
            board: The Board, used to check attacks and castling conditions.

        Returns:
            True if the move is valid for a king.
        """
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        opponent_color = "black" if self.color == "white" else "white"

        # Castling: detected when king moves exactly 2 squares horizontally
        if abs(col_diff) == 2 and row_diff == 0:
            return self._can_castle(from_pos, to_pos, board, col_diff, opponent_color)

        # Normal move: king moves one square in any direction
        if abs(col_diff) > 1 or abs(row_diff) > 1:
            return False

        # The king cannot move to a square under attack
        return not board.is_under_attack(to_pos, opponent_color)

    def _can_castle(self, from_pos, to_pos, board, col_diff, opponent_color):
        """
        Check whether castling is allowed in the given direction.

        Castling conditions (all must be true):
        1. The king has not moved previously (self.has_moved is False).
        2. The king is not currently in check.
        3. The rook on the target side exists and has not moved.
        4. All squares between king and rook are empty.
        5. The king does not pass through or land on a square under attack.

        Kingside castling: king moves from E to G, rook from H to F.
        Queenside castling: king moves from E to C, rook from A to D.

        Args:
            from_pos: The king's current position (typically E1 or E8).
            to_pos: The king's target position (G1/C1 or G8/C8).
            board: The Board, used to check piece positions and attacks.
            col_diff: Positive for kingside, negative for queenside.
            opponent_color: The color of the opponent ("white" or "black").

        Returns:
            True if castling is allowed.
        """
        if self.has_moved:
            return False

        # King must not be in check at the start
        if board.is_under_attack(from_pos, opponent_color):
            return False

        row = from_pos.ver()
        letters = "ABCDEFGH"

        # Determine which rook to castle with based on direction
        if col_diff > 0:
            # Kingside castling: rook is on the H column
            rook_pos = Position(strpos=f"H{row}")
        else:
            # Queenside castling: rook is on the A column
            rook_pos = Position(strpos=f"A{row}")

        # The rook must exist and must not have moved
        rook = board.piece_at(rook_pos)
        if rook is None or not hasattr(rook, 'has_moved') or rook.has_moved:
            return False

        # All squares between the king and rook must be empty
        if not rook.path_is_clear(rook._intermediate_positions(from_pos, rook_pos), board):
            return False

        # The king must not pass through or land on any square attacked by the opponent.
        # This checks each square the king crosses (including the destination).
        step = 1 if col_diff > 0 else -1
        for c in range(from_pos.hor() + step, to_pos.hor() + step, step):
            pos = Position(strpos=f"{letters[c - 1]}{row}")
            if board.is_under_attack(pos, opponent_color):
                return False

        return True