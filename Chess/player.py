# from dataclasses import dataclass
#
# @dataclass(frozen=True)
# class Player:
#     name: str

class Player:
    def __init__(self, *, color: str):
        self.name = ""

        self.create()

    def create(self):
        self.name