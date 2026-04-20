from abc import ABC, abstractmethod

from chess.position import Position


class Piece(ABC):
    def __init__(self, *, color: str):
        self.color = color

    @abstractmethod
    def is_authorized_move(self, from_pos, to_pos, board):
        pass

    def _intermediate_positions(self, from_pos, to_pos):
        col_diff = to_pos.hor() - from_pos.hor()
        row_diff = to_pos.ver() - from_pos.ver()

        step_col = (1 if col_diff > 0 else -1) if col_diff != 0 else 0
        step_row = (1 if row_diff > 0 else -1) if row_diff != 0 else 0
        letters = "ABCDEFGH"

        positions = []
        col = from_pos.hor() + step_col
        row = from_pos.ver() + step_row

        while col != to_pos.hor() or row != to_pos.ver():
            positions.append(Position(strpos=f"{letters[col - 1]}{row}"))
            col += step_col
            row += step_row

        return positions

    def path_is_clear(self, positions, board):
        for pos in positions:
            if board.piece_at(pos) is not None:
                return False
        return True
