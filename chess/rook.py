from chess.piece import Piece

# TOWER

class Rook(Piece):
    def __init__(self, *, color: str):
        super().__init__(color=color)


