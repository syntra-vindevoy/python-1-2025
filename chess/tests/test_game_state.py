"""Tests for game state detection: check, checkmate, stalemate, insufficient material.

Uses Scholar's mate (herdersmat) for checkmate test:
1. e4 e5  2. Bc4 Nc6  3. Qh5 Nf6  4. Qxf7#
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
# CHECK
# ============================================================================

class TestCheck:
    def test_king_in_check_by_rook(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        assert board.is_check(color="white") is True

    def test_king_in_check_by_bishop(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Bishop(color="black"), position_str="H4")

        assert board.is_check(color="white") is True

    def test_king_in_check_by_queen(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Queen(color="black"), position_str="E8")

        assert board.is_check(color="white") is True

    def test_king_in_check_by_knight(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Knight(color="black"), position_str="D3")

        assert board.is_check(color="white") is True

    def test_king_in_check_by_pawn(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E4")
        place(board=board, piece=Pawn(color="black"), position_str="D5")

        assert board.is_check(color="white") is True

    def test_king_not_in_check(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Rook(color="black"), position_str="A8")

        assert board.is_check(color="white") is False

    def test_check_blocked_by_piece(self):
        """A piece between the attacker and king blocks the check."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Pawn(color="white"), position_str="E2")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        assert board.is_check(color="white") is False


# ============================================================================
# CHECKMATE - SCHOLAR'S MATE (HERDERSMAT)
# ============================================================================

class TestScholarsMate:
    def _setup_scholars_mate(self):
        """
        Set up the board position after Scholar's mate (herdersmat):
        1. e4 e5  2. Bc4 Nc6  3. Qh5 Nf6  4. Qxf7#

        Final position:
        - White: King E1, Queen F7, Bishop C4, pawns on standard except E4
        - Black: King E8 (in checkmate), various pieces
        """
        board = empty_board()

        # White pieces
        place(board=board, piece=Rook(color="white"), position_str="A1")
        place(board=board, piece=Knight(color="white"), position_str="B1")
        place(board=board, piece=Bishop(color="white"), position_str="C1")
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Bishop(color="white"), position_str="C4")  # Moved from F1
        place(board=board, piece=Knight(color="white"), position_str="G1")
        place(board=board, piece=Rook(color="white"), position_str="H1")

        # White pawns (E pawn moved to E4)
        for col in "ABCDFGH":
            place(board=board, piece=Pawn(color="white"), position_str=f"{col}2")

        place(board=board, piece=Pawn(color="white"), position_str="E4")

        # White queen on F7 — the checkmate move
        place(board=board, piece=Queen(color="white"), position_str="F7")

        # Black pieces
        place(board=board, piece=Rook(color="black"), position_str="A8")
        place(board=board, piece=Knight(color="black"), position_str="C6")  # Moved from B8
        place(board=board, piece=Bishop(color="black"), position_str="C8")
        place(board=board, piece=Queen(color="black"), position_str="D8")
        place(board=board, piece=King(color="black"), position_str="E8")
        place(board=board, piece=Bishop(color="black"), position_str="F8")
        place(board=board, piece=Knight(color="black"), position_str="F6")  # Moved from G8
        place(board=board, piece=Rook(color="black"), position_str="H8")

        # Black pawns (E pawn moved to E5)
        for col in "ABCDGH":
            place(board=board, piece=Pawn(color="black"), position_str=f"{col}7")

        place(board=board, piece=Pawn(color="black"), position_str="E5")
        # F7 pawn was captured by the queen

        return board

    def test_black_is_in_check(self):
        board = self._setup_scholars_mate()
        assert board.is_check(color="black") is True

    def test_black_has_no_legal_moves(self):
        board = self._setup_scholars_mate()
        assert board.has_legal_moves(color="black") is False

    def test_black_is_in_checkmate(self):
        board = self._setup_scholars_mate()
        assert board.is_checkmate(color="black") is True

    def test_white_is_not_in_checkmate(self):
        board = self._setup_scholars_mate()
        assert board.is_checkmate(color="white") is False


# ============================================================================
# SIMPLE CHECKMATE (BACK RANK)
# ============================================================================

class TestBackRankMate:
    def test_back_rank_checkmate(self):
        """
        Simple back rank mate: black king on H8 with pawns on G7 and H7,
        white rook delivers check on A8.
        """
        board = empty_board()
        place(board=board, piece=King(color="black"), position_str="H8")
        place(board=board, piece=Pawn(color="black"), position_str="G7")
        place(board=board, piece=Pawn(color="black"), position_str="H7")
        place(board=board, piece=Rook(color="white"), position_str="A8")
        place(board=board, piece=King(color="white"), position_str="A1")

        assert board.is_check(color="black") is True
        assert board.is_checkmate(color="black") is True


# ============================================================================
# NOT CHECKMATE (CAN ESCAPE)
# ============================================================================

class TestNotCheckmate:
    def test_can_block_check(self):
        """King is in check but a piece can block."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Rook(color="white"), position_str="A2")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        assert board.is_check(color="white") is True
        assert board.is_checkmate(color="white") is False  # Rook can block on E2

    def test_can_capture_attacker(self):
        """King is in check but the attacker can be captured."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Queen(color="white"), position_str="A4")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        assert board.is_check(color="white") is True
        assert board.is_checkmate(color="white") is False  # Queen can capture on E8

    def test_king_can_escape(self):
        """King is in check but can move to a safe square."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        assert board.is_check(color="white") is True
        assert board.is_checkmate(color="white") is False  # King can move to D1, F1, etc.


# ============================================================================
# STALEMATE
# ============================================================================

class TestStalemate:
    def test_stalemate_king_only(self):
        """
        Black king on A8, white queen on B6, white king on C8.
        Black is not in check but has no legal moves = stalemate.
        """
        board = empty_board()
        place(board=board, piece=King(color="black"), position_str="A8")
        place(board=board, piece=Queen(color="white"), position_str="B6")
        place(board=board, piece=King(color="white"), position_str="C1")

        assert board.is_check(color="black") is False
        assert board.has_legal_moves(color="black") is False
        assert board.is_stalemate(color="black") is True

    def test_not_stalemate_when_in_check(self):
        """If the king is in check, it's not stalemate even if no legal moves (it's checkmate)."""
        board = empty_board()
        place(board=board, piece=King(color="black"), position_str="H8")
        place(board=board, piece=Pawn(color="black"), position_str="G7")
        place(board=board, piece=Pawn(color="black"), position_str="H7")
        place(board=board, piece=Rook(color="white"), position_str="A8")
        place(board=board, piece=King(color="white"), position_str="A1")

        assert board.is_stalemate(color="black") is False  # It's checkmate, not stalemate


# ============================================================================
# INSUFFICIENT MATERIAL
# ============================================================================

class TestInsufficientMaterial:
    def test_king_vs_king(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is True

    def test_king_and_bishop_vs_king(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Bishop(color="white"), position_str="C1")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is True

    def test_king_and_knight_vs_king(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Knight(color="white"), position_str="B1")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is True

    def test_king_bishop_vs_king_bishop_same_color_square(self):
        """Both bishops on same color square = insufficient material."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        # C1: hor=3, ver=1, sum=4 (even) = dark square
        place(board=board, piece=Bishop(color="white"), position_str="C1")
        place(board=board, piece=King(color="black"), position_str="E8")
        # F8: hor=6, ver=8, sum=14 (even) = dark square
        place(board=board, piece=Bishop(color="black"), position_str="F8")

        assert board.is_insufficient_material() is True

    def test_king_bishop_vs_king_bishop_different_color_square(self):
        """Bishops on different color squares = sufficient material."""
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        # C1: hor=3, ver=1, sum=4 (even)
        place(board=board, piece=Bishop(color="white"), position_str="C1")
        place(board=board, piece=King(color="black"), position_str="E8")
        # C8: hor=3, ver=8, sum=11 (odd)
        place(board=board, piece=Bishop(color="black"), position_str="C8")

        assert board.is_insufficient_material() is False

    def test_king_and_rook_vs_king_is_sufficient(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Rook(color="white"), position_str="A1")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is False

    def test_king_and_queen_vs_king_is_sufficient(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Queen(color="white"), position_str="D1")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is False

    def test_king_and_pawn_vs_king_is_sufficient(self):
        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Pawn(color="white"), position_str="E2")
        place(board=board, piece=King(color="black"), position_str="E8")

        assert board.is_insufficient_material() is False


# ============================================================================
# MOVE LEAVES KING IN CHECK
# ============================================================================

class TestMoveKingSafety:
    def test_pinned_piece_cannot_move(self):
        """A piece that is pinned (shields king from attacker) cannot move away."""
        from chess.move import Move

        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        # Bishop on E2 is pinned by the black rook on E8
        place(board=board, piece=Bishop(color="white"), position_str="E2")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        with pytest.raises(ValueError, match="leave your king in check"):
            Move(from_to="E2-D3", board=board, color="white")

    def test_must_escape_check(self):
        """When in check, you must make a move that gets out of check."""
        from chess.move import Move

        board = empty_board()
        place(board=board, piece=King(color="white"), position_str="E1")
        place(board=board, piece=Pawn(color="white"), position_str="A2")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        # Moving the pawn doesn't resolve the check
        with pytest.raises(ValueError, match="leave your king in check"):
            Move(from_to="A2-A3", board=board, color="white")
