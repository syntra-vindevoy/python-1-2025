from Chess.piece import Piece


class Knight(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)