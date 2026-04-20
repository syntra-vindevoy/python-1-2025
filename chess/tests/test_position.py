"""Tests for Position class."""

import pytest
from chess.position import Position


class TestPositionCreation:
    def test_uppercase_storage(self):
        pos = Position(strpos="a1")
        assert pos.strpos == "A1"

    def test_already_uppercase(self):
        pos = Position(strpos="E4")
        assert pos.strpos == "E4"


class TestPositionHor:
    def test_column_a(self):
        assert Position(strpos="A1").hor() == 1

    def test_column_h(self):
        assert Position(strpos="H8").hor() == 8

    def test_column_d(self):
        assert Position(strpos="D5").hor() == 4


class TestPositionVer:
    def test_row_1(self):
        assert Position(strpos="A1").ver() == 1

    def test_row_8(self):
        assert Position(strpos="H8").ver() == 8

    def test_row_5(self):
        assert Position(strpos="D5").ver() == 5


class TestPositionPos:
    def test_a1(self):
        assert Position(strpos="A1").pos() == (1, 1)

    def test_h8(self):
        assert Position(strpos="H8").pos() == (8, 8)

    def test_c3(self):
        assert Position(strpos="C3").pos() == (3, 3)


class TestPositionEquality:
    def test_same_position_equal(self):
        assert Position(strpos="A1") == Position(strpos="A1")

    def test_different_position_not_equal(self):
        assert not (Position(strpos="A1") == Position(strpos="A2"))

    def test_case_insensitive_equal(self):
        assert Position(strpos="a1") == Position(strpos="A1")

    def test_not_equal_to_string(self):
        assert not (Position(strpos="A1") == "A1")

    def test_not_equal_to_none(self):
        assert not (Position(strpos="A1") == None)
