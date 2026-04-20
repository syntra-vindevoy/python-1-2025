from dataclasses import dataclass



class Player:
    def __init__(self, *, color: str):
        self.name = ""

        self.create(color=color)

    def create(self, *, color: str):
        name = input(f"Enter name for {color}: ")
        self.name = name