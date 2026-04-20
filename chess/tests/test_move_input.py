"""Tests for Move input validation."""

import pytest
from chess.move import Move
from chess.board import Board
from chess.tests.helpers import empty_board, place
from chess.pawn import Pawn
from chess.rook import Rook


class TestMoveValidSyntax:
    def test_dash_separator(self):
        """A2-A4 is valid syntax."""
        board = empty_board()
        place(board=board, piece=Pawn(color="white"), position_str="A2")
        move = Move(from_to="A2-A4", board=board, color="white")
        assert move.from_to == "A2-A4"

    def test_space_separator(self):
        """A2 A4 is valid syntax."""
        board = empty_board()
        place(board=board, piece=Pawn(color="white"), position_str="A2")
        move = Move(from_to="A2 A4", board=board, color="white")
        assert move.from_to == "A2 A4"

    def test_lowercase_input(self):
        """Lowercase input should be accepted and uppercased."""
        board = empty_board()
        place(board=board, piece=Pawn(color="white"), position_str="A2")
        move = Move(from_to="a2-a4", board=board, color="white")
        assert move.from_to == "A2-A4"


class TestMoveInvalidSyntax:
    def test_too_short(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="A2", board=empty_board(), color="white")

    def test_too_long(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="A2-A4-A6", board=empty_board(), color="white")

    def test_invalid_column(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="Z2-A4", board=empty_board(), color="white")

    def test_invalid_row(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="A0-A4", board=empty_board(), color="white")

    def test_no_separator(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="A2A4", board=empty_board(), color="white")

    def test_random_text(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="hello", board=empty_board(), color="white")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="Invalid move syntax"):
            Move(from_to="", board=empty_board(), color="white")


class TestMoveSpecialCommands:
    def test_quit(self):
        move = Move(from_to="QUIT")
        assert move.is_quit is True
        assert move.is_draw_proposal is False

    def test_quit_lowercase(self):
        move = Move(from_to="quit")
        assert move.is_quit is True

    def test_draw(self):
        move = Move(from_to="DRAW")
        assert move.is_draw_proposal is True
        assert move.is_quit is False

    def test_draw_lowercase(self):
        move = Move(from_to="draw")
        assert move.is_draw_proposal is True


class TestMoveAssertions:
    def test_non_string_raises_assertion(self):
        with pytest.raises(AssertionError, match="from_to must be a string"):
            Move(from_to=123)

    def test_none_raises_assertion(self):
        with pytest.raises(AssertionError, match="from_to must be a string"):
            Move(from_to=None)


class TestMoveAuthorization:
    def test_no_piece_at_source(self):
        board = empty_board()
        with pytest.raises(ValueError, match="No piece at"):
            Move(from_to="A2-A4", board=board, color="white")

    def test_wrong_color_piece(self):
        board = empty_board()
        place(board=board, piece=Pawn(color="black"), position_str="A2")
        with pytest.raises(ValueError, match="belongs to the other player"):
            Move(from_to="A2-A4", board=board, color="white")

    def test_same_source_and_destination(self):
        board = empty_board()
        place(board=board, piece=Rook(color="white"), position_str="A1")
        with pytest.raises(ValueError, match="From and to positions are the same"):
            Move(from_to="A1-A1", board=board, color="white")

    def test_capture_own_piece(self):
        board = empty_board()
        place(board=board, piece=Rook(color="white"), position_str="A1")
        place(board=board, piece=Rook(color="white"), position_str="A8")
        with pytest.raises(ValueError, match="occupied by your own piece"):
            Move(from_to="A1-A8", board=board, color="white")
