from Chess.piece import Piece


class Rook(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)