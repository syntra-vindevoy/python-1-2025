"""
Test helpers for building custom board positions.
"""

from chess.board import Board
from chess.position import Position


def empty_board():
    """Create a board with no pieces."""
    board = Board.__new__(Board)
    board.pieces = []
    board.last_move = None

    return board


def place(*, board, piece, position_str):
    """Place a piece on the board at the given position string."""
    pos = Position(strpos=position_str)
    board.pieces.append((pos, piece))
