from chess.piece import Piece
from chess.position import Position
from chess.rook import Rook


class Board:
    def __init__(self):
        self.pieces = []

        self.populate()

    def _put(self, *, piece: Piece, position: str):
        pos = Position(strpos=position)
        self.pieces.append((pos, piece))

    def populate(self):
        self._put(piece=Rook(color="white"), position="A1")
        self._put(piece=Rook(color="white"), position="A8")
        self._put(piece=Rook(color="black"), position="H1")
        self._put(piece=Rook(color="black"), position="H8")
