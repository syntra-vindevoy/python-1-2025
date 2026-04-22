"""
Move module.

Represents a player's move input. A move can be:
- A standard move in algebraic notation (e.g. "A2-A4", "e2 e4")
- A special command: "QUIT" (resign) or "DRAW" (propose a draw)

The Move class handles three levels of validation:
1. Syntax validation: Does the input match the expected format?
2. Authorization: Is the move legal according to chess rules?
3. King safety: Does the move leave the player's own king in check?

If any validation fails, a ValueError is raised with a descriptive message.
"""

import re

from chess.position import Position


class Move:
    """
    Represents a single move in the chess game.

    Attributes:
        pattern: Compiled regex for valid move syntax (e.g. "A1-A2" or "A1 A2").
        from_to: The raw input string, uppercased.
        is_quit: True if the player chose to resign.
        is_draw_proposal: True if the player proposed a draw.
        from_pos: Position object for the source square (only set for standard moves).
        to_pos: Position object for the destination square (only set for standard moves).
        board: Reference to the Board (only set for standard moves).
        color: The color of the player making the move (only set for standard moves).
        unauthorized_reason: Descriptive message when a move is rejected (set during validation).
    """

    pattern = re.compile(r'^[A-H][1-8][- ][A-H][1-8]$')

    def __init__(self, *, from_to: str, board=None, color=None):
        """
        Create and validate a move from user input.

        The constructor performs all validation immediately. If the move is invalid,
        a ValueError is raised — the caller never receives an invalid Move object.

        For special commands (QUIT, DRAW), no board or color is needed.
        For standard moves, both board and color must be provided.

        Args:
            from_to: The user's input string (e.g. "A2-A4", "quit", "draw").
            board: The Board object, needed to validate standard moves.
            color: The color of the current player ("white" or "black").

        Raises:
            AssertionError: If from_to is not a string.
            ValueError: If the move syntax is invalid or the move is not authorized.
        """
        assert isinstance(from_to, str), "from_to must be a string"

        self.from_to = from_to.upper()
        self.is_quit = self.from_to == "QUIT"
        self.is_draw_proposal = self.from_to == "DRAW"

        if not self.is_quit and not self.is_draw_proposal:
            if not self.is_valid_move():
                raise ValueError(f"Invalid move syntax: {from_to}. Expected format: A1-A2 (letter A-H, digit 1-8, dash or space, letter A-H, digit 1-8), QUIT or DRAW")

            self.from_pos = Position(strpos=from_to[:2])
            self.to_pos = Position(strpos=from_to[3:])
            self.board = board
            self.color = color

            if not self.is_authorized_move():
                raise ValueError(self.unauthorized_reason)

    def is_valid_move(self):
        """
        Check whether the input matches the expected move syntax.

        Valid format: a letter A-H, a digit 1-8, a separator (dash or space),
        a letter A-H, a digit 1-8. Example: "A2-A4" or "E7 E5".

        Returns:
            True if the syntax is valid, False otherwise.
        """

        return bool(self.pattern.match(self.from_to))

    def is_authorized_move(self):
        """
        Check whether the move is legal according to all chess rules.

        This method performs a chain of validations, in order:
        1. Source and destination must be different squares.
        2. There must be a piece at the source position.
        3. The piece must belong to the current player.
        4. The destination must not be occupied by a friendly piece.
        5. The piece's own movement rules must allow the move
           (delegates to Piece.is_authorized_move).
        6. The move must not leave the player's own king in check
           (simulates the move temporarily to verify king safety).

        If any check fails, self.unauthorized_reason is set with a descriptive
        message explaining why the move was rejected.

        Returns:
            True if the move passes all checks, False otherwise.
        """
        # Check 1: source and destination must differ
        if self.from_pos == self.to_pos:
            self.unauthorized_reason = "From and to positions are the same"

            return False

        # Check 2: there must be a piece at the source
        piece = self.board.piece_at(position=self.from_pos)

        if piece is None:
            self.unauthorized_reason = f"No piece at {self.from_pos.strpos}"

            return False

        # Check 3: the piece must belong to the current player
        if piece.color != self.color:
            self.unauthorized_reason = f"Piece at {self.from_pos.strpos} belongs to the other player"

            return False

        # Check 4: cannot capture your own piece
        target_piece = self.board.piece_at(position=self.to_pos)

        if target_piece is not None and target_piece.color == self.color:
            self.unauthorized_reason = f"Cannot move to {self.to_pos.strpos}: occupied by your own piece"

            return False

        # Check 5: the piece's own movement rules must allow it
        if not piece.is_authorized_move(from_pos=self.from_pos, to_pos=self.to_pos, board=self.board):
            self.unauthorized_reason = f"This piece cannot move from {self.from_pos.strpos} to {self.to_pos.strpos}"

            return False

        # Check 6: simulate the move and verify the king is not left in check.
        # We temporarily modify the board's piece list, check king safety,
        # then restore the original state. This is necessary because a move
        # that is otherwise valid may expose the king to an attack (e.g.
        # moving a pinned piece, or not blocking/escaping a check).
        opponent_color = "black" if self.color == "white" else "white"

        # Save the current board state so we can restore it after the simulation
        saved_pieces = self.board.pieces[:]

        # Simulate: remove any captured piece at the destination
        self.board.pieces = [(p, pc) for p, pc in self.board.pieces if p != self.to_pos]

        # Simulate: move our piece from source to destination
        for i, (p, pc) in enumerate(self.board.pieces):
            if p == self.from_pos:
                self.board.pieces[i] = (self.to_pos, pc)
                break

        # After the simulated move, find our king and check if it's under attack.
        # A pinned piece (one that shields the king from an attacker) would fail here
        # because moving it would expose the king.
        king_pos = self.board.find_king(color=self.color)
        in_check = self.board.is_under_attack(position=king_pos, by_color=opponent_color)

        # Restore the board to its original state — the simulation is done
        self.board.pieces = saved_pieces

        if in_check:
            self.unauthorized_reason = "This move would leave your king in check"

            return False

        return True
