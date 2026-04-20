"""Tests for special chess moves: en-passant, castling, pawn promotion, two-square pawn move."""

import pytest
from unittest.mock import patch
from chess.tests.helpers import empty_board, place
from chess.position import Position
from chess.rook import Rook
from chess.knight import Knight
from chess.bishop import Bishop
from chess.queen import Queen
from chess.king import King
from chess.pawn import Pawn


# ============================================================================
# EN-PASSANT
# ============================================================================

class TestEnPassant:
    def test_en_passant_white_captures_left(self):
        """White pawn on E5 can capture en-passant on D6 after black pawn D7->D5."""
        board = empty_board()
        white_pawn = Pawn(color="white")
        black_pawn = Pawn(color="black")
        place(board=board, piece=white_pawn, position_str="E5")
        place(board=board, piece=black_pawn, position_str="D5")

        # Set last_move to simulate black's D7->D5 double advance
        board.last_move = (Position(strpos="D7"), Position(strpos="D5"), black_pawn)

        result = white_pawn.is_authorized_move(
            from_pos=Position(strpos="E5"),
            to_pos=Position(strpos="D6"),
            board=board
        )

        assert result is True

    def test_en_passant_not_allowed_without_double_advance(self):
        """En-passant only works if the opponent pawn just moved 2 squares."""
        board = empty_board()
        white_pawn = Pawn(color="white")
        black_pawn = Pawn(color="black")
        place(board=board, piece=white_pawn, position_str="E5")
        place(board=board, piece=black_pawn, position_str="D5")

        # Last move was only 1 square, not a double advance
        board.last_move = (Position(strpos="D6"), Position(strpos="D5"), black_pawn)

        result = white_pawn.is_authorized_move(
            from_pos=Position(strpos="E5"),
            to_pos=Position(strpos="D6"),
            board=board
        )

        assert result is False

    def test_en_passant_removes_captured_pawn(self):
        """After en-passant, the captured pawn should be removed from the board."""
        board = empty_board()
        white_pawn = Pawn(color="white")
        black_pawn = Pawn(color="black")
        place(board=board, piece=white_pawn, position_str="E5")
        place(board=board, piece=black_pawn, position_str="D5")
        board.last_move = (Position(strpos="D7"), Position(strpos="D5"), black_pawn)

        board.move_piece(from_pos=Position(strpos="E5"), to_pos=Position(strpos="D6"))

        # The black pawn on D5 should be gone
        assert board.piece_at(position=Position(strpos="D5")) is None

        # The white pawn should be on D6
        assert isinstance(board.piece_at(position=Position(strpos="D6")), Pawn)


# ============================================================================
# CASTLING
# ============================================================================

class TestCastling:
    def test_kingside_castling_white(self):
        """White can castle kingside: E1->G1."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is True

    def test_queenside_castling_white(self):
        """White can castle queenside: E1->C1."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="A1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="C1"),
            board=board
        )

        assert result is True

    def test_castling_not_allowed_after_king_moved(self):
        """Castling is not allowed if the king has moved."""
        board = empty_board()
        king = King(color="white")
        king.has_moved = True
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is False

    def test_castling_not_allowed_after_rook_moved(self):
        """Castling is not allowed if the rook has moved."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        rook.has_moved = True
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is False

    def test_castling_not_allowed_when_in_check(self):
        """Castling is not allowed when the king is in check."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")
        place(board=board, piece=Rook(color="black"), position_str="E8")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is False

    def test_castling_not_allowed_through_attacked_square(self):
        """Castling is not allowed if the king passes through an attacked square."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")
        # Black rook attacks F1, which the king would pass through
        place(board=board, piece=Rook(color="black"), position_str="F8")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is False

    def test_castling_not_allowed_with_piece_in_between(self):
        """Castling is not allowed if there is a piece between king and rook."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")
        place(board=board, piece=Bishop(color="white"), position_str="F1")

        result = king.is_authorized_move(
            from_pos=Position(strpos="E1"),
            to_pos=Position(strpos="G1"),
            board=board
        )

        assert result is False

    def test_castling_moves_rook(self):
        """After kingside castling, rook should move from H1 to F1."""
        board = empty_board()
        king = King(color="white")
        rook = Rook(color="white")
        place(board=board, piece=king, position_str="E1")
        place(board=board, piece=rook, position_str="H1")

        board.move_piece(from_pos=Position(strpos="E1"), to_pos=Position(strpos="G1"))

        assert isinstance(board.piece_at(position=Position(strpos="G1")), King)
        assert isinstance(board.piece_at(position=Position(strpos="F1")), Rook)
        assert board.piece_at(position=Position(strpos="H1")) is None
        assert board.piece_at(position=Position(strpos="E1")) is None


# ============================================================================
# PAWN PROMOTION
# ============================================================================

class TestPawnPromotion:
    def test_promotion_to_queen(self):
        """When a pawn reaches the last row, it should be promoted."""
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="A7")

        with patch("builtins.input", return_value="Q"):
            board.move_piece(from_pos=Position(strpos="A7"), to_pos=Position(strpos="A8"))

        piece = board.piece_at(position=Position(strpos="A8"))
        assert isinstance(piece, Queen)
        assert piece.color == "white"

    def test_promotion_to_knight(self):
        board = empty_board()
        pawn = Pawn(color="white")
        place(board=board, piece=pawn, position_str="A7")

        with patch("builtins.input", return_value="K"):
            board.move_piece(from_pos=Position(strpos="A7"), to_pos=Position(strpos="A8"))

        piece = board.piece_at(position=Position(strpos="A8"))
        assert isinstance(piece, Knight)

    def test_black_promotion(self):
        """Black pawn promotes on row 1."""
        board = empty_board()
        pawn = Pawn(color="black")
        place(board=board, piece=pawn, position_str="A2")

        with patch("builtins.input", return_value="Q"):
            board.move_piece(from_pos=Position(strpos="A2"), to_pos=Position(strpos="A1"))

        piece = board.piece_at(position=Position(strpos="A1"))
        assert isinstance(piece, Queen)
        assert piece.color == "black"
