from chess.bishop import Bishop
from chess.king import King
from chess.knight import Knight
from chess.pawn import Pawn
from chess.piece import Piece
from chess.position import Position
from chess.queen import Queen
from chess.rook import Rook


class Board:
    def __init__(self):
        self.pieces = []

        self.populate()

    def _put(self, *, piece: Piece, position: str):
        pos = Position(strpos=position)
        self.pieces.append((pos, piece))

    def populate(self):
        # White pieces
        self._put(piece=Rook(color="white"), position="A1")
        self._put(piece=Knight(color="white"), position="B1")
        self._put(piece=Bishop(color="white"), position="C1")
        self._put(piece=Queen(color="white"), position="D1")
        self._put(piece=King(color="white"), position="E1")
        self._put(piece=Bishop(color="white"), position="F1")
        self._put(piece=Knight(color="white"), position="G1")
        self._put(piece=Rook(color="white"), position="H1")

        for col in "ABCDEFGH":
            self._put(piece=Pawn(color="white"), position=f"{col}2")

        # Black pieces
        self._put(piece=Rook(color="black"), position="A8")
        self._put(piece=Knight(color="black"), position="B8")
        self._put(piece=Bishop(color="black"), position="C8")
        self._put(piece=Queen(color="black"), position="D8")
        self._put(piece=King(color="black"), position="E8")
        self._put(piece=Bishop(color="black"), position="F8")
        self._put(piece=Knight(color="black"), position="G8")
        self._put(piece=Rook(color="black"), position="H8")

        for col in "ABCDEFGH":
            self._put(piece=Pawn(color="black"), position=f"{col}7")

    def piece_at(self, position: Position):
        for pos, piece in self.pieces:
            if pos == position:
                return piece
        return None

    def move_piece(self, from_pos: Position, to_pos: Position):
        # Remove captured piece at destination
        self.pieces = [(pos, piece) for pos, piece in self.pieces if pos != to_pos]

        # Move the piece
        for i, (pos, piece) in enumerate(self.pieces):
            if pos == from_pos:
                self.pieces[i] = (to_pos, piece)
                break
