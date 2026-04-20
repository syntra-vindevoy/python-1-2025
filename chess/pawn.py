from chess.piece import Piece


class Pawn(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)
        