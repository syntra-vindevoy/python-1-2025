from Chess.bishop import Bishop
from Chess.king import King
from Chess.knight import Knight
from Chess.pawn import Pawn
from Chess.piece import Piece
from Chess.position import Position
from Chess.queen import Queen
from Chess.rook import Rook


class Board:
    def __init__(self):
        self.pieces = []

        self.populate()

    def _put(self, *, piece: Piece, position: str):
        pos = Position(strpos=position)

    def populate(self):
        # White pieces
        self._put(piece = Rook(color="white"), position = "A1")
        self._put(piece = Knight(color="white"), position = "B1")
        self._put(piece = Bishop(color="white"), position = "C1")
        self._put(piece = Queen(color="white"), position = "D1")
        self._put(piece = King(color="white"), position = "E1")
        self._put(piece = Bishop(color="white"), position = "F1")
        self._put(piece = Knight(color="white"), position = "G1")
        self._put(piece = Rook(color="white"), position = "H1")
        # White pawns
        #for pos in "ABCDEFGH":
        #    self._put(piece = Pawn(color="Black"), position = f{pos}2)
        for pos in ["A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2"]:
            self._put(piece = Pawn(color="Black"), position = pos)

        # Black pieces
        self._put(piece = Rook(color="black"), position = "A8")
        self._put(piece = Knight(color="black"), position = "B8")
        self._put(piece = Bishop(color="black"), position = "C8")
        self._put(piece = King(color="black"), position = "D8")
        self._put(piece = Queen(color="black"), position = "E8")
        self._put(piece = Bishop(color="black"), position = "F8")
        self._put(piece = Knight(color="black"), position = "G8")
        self._put(piece = Rook(color="black"), position = "H8")
        # Black pawns   -> adjust positions
        for pos in ["A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7"]:
            self._put(piece = Pawn(color="Black"), position = pos)
