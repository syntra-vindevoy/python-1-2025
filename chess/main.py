"""
Main entry point for the chess game.

This script creates a new game, initializes the players and board,
then runs the game loop until the game is over. Finally, it prints
the result (winner or draw).

Usage:
    python -m chess.main
"""

from chess.game import Game

# Create and initialize the game (prompts for player names, sets up the board)
game = Game()

# Record the initial board position for threefold repetition tracking
game.start()

# Main game loop: alternate turns until the game ends
while not game.is_over():
    game.do_move()

# Display the result
print("Game is over")
if game.draw:
    print("The game ended in a draw. No winner.")
else:
    print(f"The winner is: {game.winner.name}")