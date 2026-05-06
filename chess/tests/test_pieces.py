"""Tests for each piece's movement rules.

For each piece, _tests cover 4 scenarios:
1. Valid move (correct direction/pattern)
2. Invalid direction (piece can't move that way)
3. Destination occupied by same color (blocked)
4. Path blocked by a piece in the way (sliding pieces) or other invalid case
"""

import pytest
from chess.tests.helpers import empty_board, place
from chess.position import Position
from chess.rook import Rook
from chess.knight import Knight
from chess.bishop import Bishop
from chess.queen import Queen
from chess.king import King
from chess.pawn import Pawn


# ============================================================================
# ROOK
# ============================================================================

class TestRookValidMove:
    def test_horizontal_move(self):
        board = empty_board()
        rook = Rook(color="white")
        place(board=board, piece=rook, position_str="A1")

        result = rook.is_authorized_move(
            from_pos=Position(strpos="A1"),
            to_pos=Position(strpos="H1"),
            board=board
        )

        assert result is True

    def test_vertical_move(self):
        board = empty_board()
        rook = Rook(color="white")
        place(board=board, piece=rook, position_str="A1")

        result = rook.is_authorized_move(
            from_pos=Position(strpos="A1"),
            to_pos=Position(strpos="A8"),
            board=board
        )

        assert result is True


class TestRookInvalidDirection:
    def test_diagonal_move_not_allowed(self):
        board = empty_board()
        rook = Rook(color="white")
        place(board=board, piece=rook, position_str="A1")

        result = rook.is_authorized_move(
            from_pos=Position(strpos="A1"),
            to_pos=Position(strpos="C3"),
            board=board
        )

        assert result is False


class TestRookBlockedPath:
    def test_piece_in_the_way_horizontal(self):
        board = empty_board()
        rook = Rook(color="white")
        place(board=board, piece=rook, position_str="A1")
        place(board=board, piece=Pawn(color="white"), position_str="D1")

        result = rook.is_authorized_move(
            from_pos=Position(strpos="A1"),
            to_pos=Position(strpos="H1"),
            board=board
        )

        assert result is False

    def test_piece_in_the_way_vertical(self):
        board = empty_board()
        rook = Rook(color="white")
        place(board=board, piece=rook, position_str="A1")
        place(board=board, piece=Pawn(color="black"), position_str="A4")

        result = rook.is_authorized_move(
            from_pos=Position(strpos="A1"),
            to_pos=Position(strpos="A8"),
            board=board
        )

        assert result is False


# ============================================================================
# KNIGHT
# ============================================================================

class TestKnightValidMove:
    def test_l_shape_2_up_1_right(self):
        board = empty_board()
        knight = Knight(color="white")
        place(board=board, piece=knight, position_str="B1")

        result = knight.is_authorized_move(
            from_pos=Position(strpos="B1"),
            to_pos=Position(strpos="C3"),
            board=board
        )

        assert result is True

    def test_l_shape_1_up_2_right(self):
        board = empty_board()
        knight = Knight(color="white")
        place(board=board, piece=knight, position_str="B1")

        result = knight.is_authorized_move(
            from_pos=Position(strpos="B1"),
            to_pos=Position(strpos="D2"),
            board=board
        )

        assert result is True


class TestKnightInvalidDirection:
    def test_straight_move_not_allowed(self):
        board = empty_board()
        knight = Knight(color="white")
        place(board=board, piece=knight, position_str="B1")

        result = knight.is_authorized_move(
            from_pos=Position(strpos="B1"),
            to_pos=Position(strpos="B3"),
            board=board
        )

        assert result is False

    def test_diagonal_move_not_allowed(self):
        board = empty_board()
        knight = Knight(color="white")
        place(board=board, piece=knight, position_str="D4")

        result = knight.is_authorized_move(
            from_pos=Position(strpos="D4"),
            to_pos=Position(strpos="F6"),
            board=board
        )

        assert result is False


class TestKnightJumpsOverPieces:
    def test_can_jump_over_pieces(self):
        """Knight should be able to jump over other pieces."""
        board = empty_board()
        knight = Knight(color="white")
        place(board=board, piece=knight, position_str="B1")
        place(board=board, piece=Pawn(color="white"), position_str="B2")
        place(board=board, piece=Pawn(color="white"), position_str="C2")

        result = knight.is_authorized_move(
            from_pos=Position(strpos="B1"),
            to_pos=Position(strpos="C3"),
            board=board
        )

        assert result is True


# ============================================================================
# BISHOP
# ============================================================================

class TestBishopValidMove:
    def test_diagonal_move(self):
        board = empty_board()
        bishop = Bishop(color="white")
        place(board=board, piece=bishop, position_str="C1")

        result = bishop.is_authorized_move(
            from_pos=Position(strpos="C1"),
            to_pos=Position(strpos="F4"),
            board=board
        )

        assert result is True

    def test_diagonal_move_other_direction(self):
        board = empty_board()
        bishop = Bishop(color="white")
        place(board=board, piece=bishop, position_str="F4")

        result = bishop.is_authorized_move(
            from_pos=Position(strpos="F4"),
            to_pos=Position(strpos="C1"),
            board=board
        )

        assert result is True


class TestBishopInvalidDirection:
    def test_horizontal_move_not_allowed(self):
        board = empty_board()
        bishop = Bishop(color="white")
        place(board=board, piece=bishop, position_str="C1")

        result = bishop.is_authorized_move(
            from_pos=Position(strpos="C1"),
            to_pos=Position(strpos="F1"),
            board=board
        )

        assert result is False

    def test_vertical_move_not_allowed(self):
        board = empty_board()
        bishop = Bishop(color="white")
        place(board=board, piece=bishop, position_str="C1")

        result = bishop.is_authorized_move(
            from_pos=Position(strpos="C1"),
            to_pos=Position(strpos="C5"),
            board=board
        )

        assert result is False


class TestBishopBlockedPath:
    def test_piece_in_the_way(self):
        board = empty_board()
        bishop = Bishop(color="white")
        place(board=board, piece=bishop, position_str="C1")
        place(board=board, piece=Pawn(color="white"), position_str="D2")

        result = bishop.is_authorized_move(
            from_pos=Position(strpos="C1"),
            to_pos=Position(strpos="F4"),
            board=board
        )

        assert result is False


# ============================================================================
# QUEEN
# ============================================================================

class TestQueenValidMove:
    def test_horizontal_move(self):
        board = empty_board()
        queen = Queen(color="white")
        place(board=board, piece=queen, position_str="D1")

        result = queen.is_authorized_move(
            from_pos=Position(strpos="D1"),
            to_pos=Position(strpos="H1"),
            board=board
        )

        assert result is True

    def test_vertical_move(self):
        board = empty_board()
        queen = Queen(color="white")
        place(board=board, piece=queen, position_str="D1")

        result = queen.is_authorized_move(
            from_pos=Position(strpos="D1"),
            to_pos=Position(strpos="D8"),
            board=board
        )

        assert result is True

    def test_diagonal_move(self):
        board = empty_board()
        queen = Queen(color="white")
        place(board=board, piece=queen, position_str="D1")

        result = queen.is_authorized_move(
            from_pos=Position(strpos="D1"),
            to_pos=Position(strpos="H5"),
            board=board
        )

        assert result is True


class TestQueenInvalidDirection:
    def test_l_shape_not_allowed(self):
        board = empty_board()
        queen = Queen(color="white")
        place(board=board, piece=queen, position_str="D1")

        result = queen.is_authorized_move(
            from_pos=Position(strpos="D1"),
            to_pos=Position(strpos="E3"),
            board=board
        )

        assert result is False


class TestQueenBlockedPath:
    def test_piece_in_the_way(self):
        board = empty_board()
        queen = Queen(color="white")
        place(board=board, piece=queen, position_str="D1")
        place(board=board, piece=Pawn(color="white"), position_str="D4")

        result = queen.is_authorized_move(
            from_pos=Position(strpos="D1"),
            to_pos=Position(strpos="D8"),
            board=board
        )

        assert result is False


# ============================================================================
# KING
# ============================================================================

class TestKingValidMove:
    def test_one_square_horizontal(self):
        board = empty_board()
        king = King(color="white")
        place(board=board, piece=king, position_str="E1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="F1"),
            board=board
        )

        assert result is True

    def test_one_square_diagonal(self):
        board = empty_board()
        king = King(color="white")
        place(board=board, piece=king, position_str="E1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="F2"),
            board=board
        )

        assert result is True


class TestKingInvalidDirection:
    def test_two_squares_not_allowed(self):
        """King cannot move 2 squares (unless castling)."""
        board = empty_board()
        king = King(color="white")
        king.has_moved = True  # Prevent castling interpretation
        place(board=board, piece=king, position_str="E4")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E4"),
            to_pos=Position(strpos="E6"),
            board=board
        )

        assert result is False


class TestKingCannotMoveIntoCheck:
    def test_cannot_move_to_square_attacked_by_rook(self):
        board = empty_board()
        king = King(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=Rook(color="black"), position_str="F8")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="F1"),
            board=board
        )

        assert result is False

    def test_cannot_move_to_square_attacked_by_pawn(self):
        """King must not move to a square attacked by an opponent pawn,
        even though the target square is empty (pawn attacks diagonally)."""
        board = empty_board()
        king = King(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=Pawn(color="black"), position_str="E3")

        # D2 is diagonally attacked by the black pawn on E3
        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="D2"),
            board=board
        )

        assert result is False

    def test_can_move_to_square_not_attacked_by_pawn(self):
        """King can move to a square that is NOT attacked by a pawn
        (pawn attacks diagonally, not forward)."""
        board = empty_board()
        king = King(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=Pawn(color="black"), position_str="D4")

        # E2 is NOT attacked by the black pawn on D4 (pawn attacks C3 and E3, not E2)
        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="E2"),
            board=board
        )

        assert result is True


# ============================================================================
# PAWN
# ============================================================================

class TestPawnValidMove:
    def test_one_square_forward_white(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E2")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E2"),
            to_pos=Position(strpos="E3"),
            board=board
        )

        assert result is True

    def test_two_squares_forward_from_start_white(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E2")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E2"),
            to_pos=Position(strpos="E4"),
            board=board
        )

        assert result is True

    def test_one_square_forward_black(self):
        board = empty_board()
        pawn = Pawn(color="black")
        place(board=board, piece=pawn, position_str="E7")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E7"),
            to_pos=Position(strpos="E6"),
            board=board
        )

        assert result is True

    def test_diagonal_capture(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E4")
        place(board=board, piece=Pawn(color="black"), position_str="D5")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E4"),
            to_pos=Position(strpos="D5"),
            board=board
        )

        assert result is True


class TestPawnInvalidDirection:
    def test_backward_move_not_allowed_white(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E4")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E4"),
            to_pos=Position(strpos="E3"),
            board=board
        )

        assert result is False

    def test_sideways_move_not_allowed(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E4")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E4"),
            to_pos=Position(strpos="D4"),
            board=board
        )

        assert result is False

    def test_diagonal_without_capture_not_allowed(self):
        """Pawn cannot move diagonally to an empty square."""
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E4")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E4"),
            to_pos=Position(strpos="D5"),
            board=board
        )

        assert result is False


class TestPawnBlockedPath:
    def test_forward_blocked_by_piece(self):
        """Pawn cannot move forward if a piece is in the way."""
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E2")
        place(board=board, piece=Pawn(color="black"), position_str="E3")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E2"),
            to_pos=Position(strpos="E3"),
            board=board
        )

        assert result is False

    def test_two_squares_blocked_by_piece_on_middle(self):
        """Pawn cannot move 2 squares if the middle square is occupied."""
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E2")
        place(board=board, piece=Pawn(color="black"), position_str="E3")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E2"),
            to_pos=Position(strpos="E4"),
            board=board
        )

        assert result is False

    def test_two_squares_not_from_start(self):
        """Pawn cannot move 2 squares if not on starting row."""
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="E3")

        result = pawn.is_authorized_move(
            from_pos=Position(strpos="E3"),
            to_pos=Position(strpos="E5"),
            board=board
        )

        assert result is False
