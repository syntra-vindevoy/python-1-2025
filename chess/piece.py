from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, *, color: str):
        self.color = color

    @abstractmethod
    def is_authorized_move(self, from_pos, to_pos, board):
        pass
