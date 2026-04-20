class Position:
    def __init__(self, *, strpos: str):
        self.strpos = strpos.upper()

    def hor(self):
        letters = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8}

        return letters[self.strpos[0]]

    def ver(self):
        return int(self.strpos[1])

    def pos(self):
        return (self.hor(), self.ver())

    def __eq__(self, other):
        return isinstance(other, Position) and self.strpos == other.strpos