"""
Position module.

Represents a single square on the chess board using algebraic notation (e.g. "A1", "E4").
The position is stored as a two-character string where the first character is a column
letter (A-H) and the second is a row number (1-8).

Columns (A-H) map to horizontal positions 1-8 from left to right.
Rows (1-8) map to vertical positions where 1 is white's back rank and 8 is black's back rank.
"""


class Position:
    """
    Represents a square on the chess board.

    Attributes:
        strpos: The algebraic notation of the position (e.g. "A1", "E4").
                Always stored in uppercase.
    """

    def __init__(self, *, strpos: str):
        """
        Create a position from algebraic notation.

        Args:
            strpos: A two-character string like "A1" or "e4".
                    The first character is a column letter (A-H),
                    the second is a row number (1-8).
                    Automatically converted to uppercase.
        """
        self.strpos = strpos.upper()

    def hor(self):
        """
        Return the horizontal (column) index as an integer.

        Mapping: A=1, B=2, C=3, D=4, E=5, F=6, G=7, H=8.
        """
        letters = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}

        return letters[self.strpos[0]]

    def ver(self):
        """
        Return the vertical (row) index as an integer (1-8).

        Row 1 is white's back rank, row 8 is black's back rank.
        """
        return int(self.strpos[1])

    def pos(self):
        """
        Return the position as a (column, row) integer tuple.

        Example: Position("C3").pos() returns (3, 3).
        """
        return (self.hor(), self.ver())

    def __eq__(self, other):
        """
        Two positions are equal if they refer to the same square.

        This is necessary because Position objects are created independently
        (not reused), so identity comparison (is) would always return False
        for positions referring to the same square.
        """
        return isinstance(other, Position) and self.strpos == other.strpos