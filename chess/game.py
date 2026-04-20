"""
Game module.

Orchestrates a complete chess game between two players. Manages the game loop,
player turns, move input, and end-of-game detection.

The game ends when:
- A player resigns (QUIT)
- Both players agree to a draw (DRAW + YES)
- Checkmate is detected
- Stalemate (pat) is detected
- Insufficient material makes checkmate impossible
- Threefold repetition of the same board position
- 50-move rule (100 half-moves without a pawn move or capture)
"""

from chess.board import Board
from chess.move import Move
from chess.pawn import Pawn
from chess.player import Player


class Game:
    """
    Manages the state and flow of a chess game.

    Attributes:
        player_white: The Player object for white.
        player_black: The Player object for black.
        board: The Board object containing all pieces.
        moves: List of all Move objects played so far.
        winner: The winning Player, or None if the game is still ongoing or drawn.
        draw: True if the game ended in a draw.
        position_history: List of board position keys (tuples) after each move,
                          used for threefold repetition detection.
        half_move_clock: Counter of consecutive half-moves (one player's turn) without
                         a pawn move or capture. The 50-move rule triggers at 100
                         half-moves (= 50 full moves by each player).
    """

    def __init__(self):
        self.player_white = None
        self.player_black = None
        self.board = None

        self.moves: list[Move] = []
        self.winner = None
        self.draw = False
        self.position_history = []
        self.half_move_clock = 0

        self.prepare()

    def prepare(self):
        """
        Initialize the players and the board.

        Prompts each player for their name and sets up the board with all pieces
        in the standard starting position.
        """
        self.player_white = Player(color="white")
        self.player_black = Player(color="black")
        self.board = Board()

    def start(self):
        """
        Start the game by recording the initial board position.

        The initial position is added to position_history so that threefold
        repetition detection works correctly from the very beginning.
        """
        self.position_history.append(self.board.position_key())

    def do_move(self):
        """
        Execute one turn of the game: prompt the current player for a move and process it.

        The method loops until a valid move is entered. Invalid moves (syntax errors
        or unauthorized moves) display an error message and re-prompt the player.

        After a valid move is entered, the method handles three cases:
        1. QUIT: The current player resigns, the other player wins.
        2. DRAW: A draw is proposed to the other player, who can accept or refuse.
        3. Standard move: The move is executed on the board, then the game checks
           for end-of-game conditions in priority order:
           - Checkmate (opponent's king is in check with no escape)
           - Stalemate (opponent has no legal moves but is not in check)
           - Insufficient material (neither side can force checkmate)
           - Threefold repetition (same position occurred 3 times)
           - 50-move rule (100 half-moves without pawn move or capture)
           - Check (opponent's king is under attack, game continues)
        """
        while True:
            user_input = input(f"Player {self.current_player.color} to make the move: ")

            try:
                move = Move(from_to=user_input, board=self.board, color=self.current_player.color)
            except ValueError as e:
                print(f"{e}. Try again.")
                continue

            self.moves.append(move)

            if move.is_quit:
                self.winner = self.other_player
            elif move.is_draw_proposal:
                self.handle_draw()
            else:
                # Determine if this move resets the 50-move clock before executing it,
                # because move_piece will modify the board state.
                is_pawn_move = isinstance(self.board.piece_at(move.from_pos), Pawn)
                is_capture = self.board.piece_at(move.to_pos) is not None

                self.board.move_piece(move.from_pos, move.to_pos)

                # 50-move rule: the clock resets on any pawn move or capture,
                # as these are irreversible actions that change the game state.
                if is_pawn_move or is_capture:
                    self.half_move_clock = 0
                else:
                    self.half_move_clock += 1

                # Record the new position for threefold repetition detection
                self.position_history.append(self.board.position_key())

                # Check end-of-game conditions in priority order.
                # Checkmate and stalemate are checked first because they are
                # definitive outcomes. Draw conditions follow.
                opponent_color = self.other_player.color
                if self.board.is_checkmate(opponent_color):
                    self.winner = self.current_player
                    print(f"Checkmate! {self.current_player.color} wins!")
                elif self.board.is_stalemate(opponent_color):
                    self.draw = True
                    print("Stalemate! The game is a draw.")
                elif self.board.is_insufficient_material():
                    self.draw = True
                    print("Draw by insufficient material.")
                elif self.is_threefold_repetition():
                    self.draw = True
                    print("Draw by threefold repetition.")
                # 50-move rule: 100 half-moves = 50 full moves (each player moves once
                # per half-move). The clock counts half-moves without a pawn move or capture.
                elif self.half_move_clock >= 100:
                    self.draw = True
                    print("Draw by 50-move rule.")
                elif self.board.is_check(opponent_color):
                    print(f"Check!")
            break

    def handle_draw(self):
        """
        Handle a draw proposal from the current player.

        Asks the other player whether they accept the draw. If accepted, the game
        ends in a draw. If refused, the draw move is removed from the move list
        so the same player can make a regular move on the next turn.
        """
        answer = input(f"Player {self.other_player.color}, do you accept the draw? (YES/NO): ").upper()
        if answer == "YES":
            self.draw = True
        else:
            print("Draw refused. Game continues.")
            self.moves.pop()

    @property
    def current_player(self):
        """
        Return the player whose turn it is.

        White always moves first. The current player is determined by the number
        of moves played: even count means white's turn, odd means black's turn.
        """
        # In chess, white always moves first. Moves are numbered 0, 1, 2, 3...
        # Even indices (0, 2, 4...) = white's turn, odd indices (1, 3, 5...) = black's turn
        if len(self.moves) % 2 == 0:
            return self.player_white
        else:
            return self.player_black

    @property
    def other_player(self):
        """
        Return the player who is NOT currently moving.
        """
        if self.current_player == self.player_white:
            return self.player_black
        else:
            return self.player_white

    def is_threefold_repetition(self):
        """
        Check whether the current board position has occurred 3 or more times.

        Threefold repetition is a draw condition in chess. The position is compared
        using board.position_key(), which encodes the type, color, and location of
        every piece on the board.

        Returns:
            True if the current position has appeared at least 3 times in the game.
        """
        current_position = self.position_history[-1]
        return self.position_history.count(current_position) >= 3

    def is_over(self):
        """
        Check whether the game has ended.

        The game is over when:
        - A player has resigned (last move is QUIT)
        - A draw has been agreed upon or triggered by a rule
        - A winner has been determined (checkmate)

        Returns:
            True if the game is over, False if play should continue.
        """
        if len(self.moves) > 0 and self.moves[-1].is_quit:
            return True
        if self.draw:
            return True
        if self.winner is not None:
            return True
        return False

