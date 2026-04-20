"""
Player module.

Represents a human player in the chess game. Each player has a color (white or black)
and a name that is entered at the start of the game.
"""

from dataclasses import dataclass


class Player:
    """
    Represents a chess player.

    Attributes:
        name: The player's name, entered via console input during creation.
    """

    def __init__(self, *, color: str):
        """
        Create a player and prompt for their name.

        Args:
            color: "white" or "black", used in the name prompt.
        """
        self.name = ""

        self.create(color=color)

    def create(self, *, color: str):
        """
        Prompt the user to enter a name for this player.

        Args:
            color: The color label shown in the prompt (e.g. "Enter name for white:").
        """
        name = input(f"Enter name for {color}: ")
        self.name = name