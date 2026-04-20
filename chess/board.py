"""
Board module.

Represents the chess board and all pieces on it. The board is the central data structure
of the game: it stores piece positions, executes moves (including special moves like
castling, en-passant, and promotion), and provides methods for game state detection
(check, checkmate, stalemate, insufficient material).

Pieces are stored as a list of (Position, Piece) tuples. This flat list is the single
source of truth for what is on the board.
"""

from chess.bishop import Bishop
from chess.king import King
from chess.knight import Knight
from chess.pawn import Pawn
from chess.piece import Piece
from chess.position import Position
from chess.queen import Queen
from chess.rook import Rook


class Board:
    """
    The chess board containing all pieces and game state detection logic.

    Attributes:
        pieces: List of (Position, Piece) tuples representing all pieces on the board.
        last_move: Tuple of (from_pos, to_pos, piece) for the most recent move,
                   used for en-passant detection. None if no moves have been made.
    """

    def __init__(self):
        self.pieces = []
        self.last_move = None

        self.populate()

    def _put(self, *, piece: Piece, position: str):
        """
        Place a piece on the board at the given position.

        Args:
            piece: The Piece to place.
            position: Algebraic notation string (e.g. "A1").
        """
        pos = Position(strpos=position)
        self.pieces.append((pos, piece))

    def populate(self):
        """
        Set up the board with all 32 pieces in the standard starting position.

        White pieces are on rows 1-2, black pieces on rows 7-8.
        Back rank order: Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook.
        """
        # White pieces
        self._put(piece=Rook(color="white"), position="A1")
        self._put(piece=Knight(color="white"), position="B1")
        self._put(piece=Bishop(color="white"), position="C1")
        self._put(piece=Queen(color="white"), position="D1")
        self._put(piece=King(color="white"), position="E1")
        self._put(piece=Bishop(color="white"), position="F1")
        self._put(piece=Knight(color="white"), position="G1")
        self._put(piece=Rook(color="white"), position="H1")

        for col in "ABCDEFGH":
            self._put(piece=Pawn(color="white"), position=f"{col}2")

        # Black pieces
        self._put(piece=Rook(color="black"), position="A8")
        self._put(piece=Knight(color="black"), position="B8")
        self._put(piece=Bishop(color="black"), position="C8")
        self._put(piece=Queen(color="black"), position="D8")
        self._put(piece=King(color="black"), position="E8")
        self._put(piece=Bishop(color="black"), position="F8")
        self._put(piece=Knight(color="black"), position="G8")
        self._put(piece=Rook(color="black"), position="H8")

        for col in "ABCDEFGH":
            self._put(piece=Pawn(color="black"), position=f"{col}7")

    def piece_at(self, position: Position):
        """
        Return the piece at the given position, or None if the square is empty.

        Args:
            position: The Position to look up.

        Returns:
            The Piece at that position, or None.
        """
        for pos, piece in self.pieces:
            if pos == position:
                return piece
        return None

    def move_piece(self, from_pos: Position, to_pos: Position):
        """
        Execute a move on the board, handling all special move types.

        This method performs the actual board mutation. It handles:
        1. En-passant capture: when a pawn moves diagonally to an empty square,
           the opponent's pawn on the same row is removed.
        2. Standard capture: any piece at the destination is removed.
        3. Piece movement: the piece is relocated from source to destination.
        4. Castling: when the king moves 2 squares horizontally, the corresponding
           rook is also moved to the other side of the king.
        5. Pawn promotion: when a pawn reaches the last row, the player chooses
           a new piece (Queen, Rook, Bishop, or Knight) to replace it.
        6. Move tracking: updates has_moved flags (for castling eligibility) and
           last_move (for en-passant eligibility on the next turn).

        Args:
            from_pos: The Position where the piece currently stands.
            to_pos: The Position where the piece is moving to.
        """
        piece = self.piece_at(from_pos)

        # En-passant: a pawn captures diagonally to an empty square.
        # The captured pawn is on the same row as the moving pawn, but on the
        # destination column. We remove it before the standard capture logic.
        # En-passant detection: a pawn moving diagonally (column changes) to an
        # empty square can only mean en-passant. The captured pawn sits on the
        # same row as our pawn (from_pos.ver()) but on the destination column.
        # Example: white pawn on E5 captures en-passant to D6 — the black pawn
        # on D5 (same row as E5, same column as D6) is removed.
        if isinstance(piece, Pawn) and from_pos.hor() != to_pos.hor() and self.piece_at(to_pos) is None:
            captured_pos = Position(strpos=f"{to_pos.strpos[0]}{from_pos.ver()}")
            self.pieces = [(pos, p) for pos, p in self.pieces if pos != captured_pos]

        # Remove any piece at the destination (standard capture)
        self.pieces = [(pos, p) for pos, p in self.pieces if pos != to_pos]

        # Move the piece from source to destination
        for i, (pos, p) in enumerate(self.pieces):
            if pos == from_pos:
                self.pieces[i] = (to_pos, p)
                break

        # Mark the piece as having moved (used by King and Rook for castling eligibility)
        if hasattr(piece, 'has_moved'):
            piece.has_moved = True

        # Castling: when the king moves 2 squares horizontally, the rook on that
        # side must also be moved to the square the king crossed.
        # Kingside: King E1->G1, Rook H1->F1
        # Queenside: King E1->C1, Rook A1->D1
        if isinstance(piece, King) and abs(to_pos.hor() - from_pos.hor()) == 2:
            row = from_pos.ver()
            if to_pos.hor() > from_pos.hor():
                # Kingside castling
                rook_from = Position(strpos=f"H{row}")
                rook_to = Position(strpos=f"F{row}")
            else:
                # Queenside castling
                rook_from = Position(strpos=f"A{row}")
                rook_to = Position(strpos=f"D{row}")

            for i, (pos, p) in enumerate(self.pieces):
                if pos == rook_from:
                    self.pieces[i] = (rook_to, p)
                    p.has_moved = True
                    break

        # Pawn promotion: when a pawn reaches the opponent's back rank,
        # the player must replace it with a Queen, Rook, Bishop, or Knight.
        if isinstance(piece, Pawn):
            promotion_row = 8 if piece.color == "white" else 1
            if to_pos.ver() == promotion_row:
                self._promote_pawn(to_pos, piece.color)

        # Track the last move for en-passant detection on the next turn
        self.last_move = (from_pos, to_pos, piece)

    def _promote_pawn(self, position, color):
        """
        Replace a pawn at the given position with a piece chosen by the player.

        Prompts the player to choose between Queen, Rook, Bishop, or Knight.
        Loops until a valid choice is made.

        Args:
            position: The Position of the pawn to promote.
            color: The color of the pawn ("white" or "black").
        """
        while True:
            choice = input("Promote pawn to (Q)ueen, (R)ook, (B)ishop, or (K)night: ").upper()
            if choice == "Q":
                new_piece = Queen(color=color)
            elif choice == "R":
                new_piece = Rook(color=color)
            elif choice == "B":
                new_piece = Bishop(color=color)
            elif choice == "K":
                new_piece = Knight(color=color)
            else:
                print("Invalid choice. Try again.")
                continue

            for i, (pos, piece) in enumerate(self.pieces):
                if pos == position:
                    self.pieces[i] = (pos, new_piece)
                    break
            break

    def position_key(self):
        """
        Return a hashable representation of the current board position.

        Used for threefold repetition detection. The key includes each piece's
        position, type, and color, sorted by position for consistency.

        Returns:
            A tuple of strings, each describing one piece on the board.
            Example element: "A1Rookwhite".
        """
        parts = []
        for pos, piece in sorted(self.pieces, key=lambda x: x[0].strpos):
            parts.append(f"{pos.strpos}{type(piece).__name__}{piece.color}")
        return tuple(parts)

    def pieces_of_color(self, color):
        """
        Return all pieces of the given color with their positions.

        Args:
            color: "white" or "black".

        Returns:
            A list of (Position, Piece) tuples for all pieces of that color.
        """
        return [(pos, piece) for pos, piece in self.pieces if piece.color == color]

    def find_king(self, color):
        """
        Find the position of the king of the given color.

        Args:
            color: "white" or "black".

        Returns:
            The Position of the king, or None if not found (should never happen
            in a valid game).
        """
        for pos, piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def is_under_attack(self, position, by_color):
        """
        Check whether a given square is attacked by any piece of the given color.

        Iterates through all pieces of by_color and checks if any of them can
        legally move to the target position according to their movement rules.

        Args:
            position: The Position to check.
            by_color: The color of the attacking pieces ("white" or "black").

        Returns:
            True if at least one piece of by_color can reach the position.
        """
        for pos, piece in self.pieces_of_color(by_color):
            if piece.is_authorized_move(pos, position, self):
                return True
        return False

    def has_legal_moves(self, color):
        """
        Check whether the player of the given color has at least one legal move.

        A legal move must satisfy:
        1. The piece's own movement rules allow it.
        2. The destination is not occupied by a friendly piece.
        3. After the move, the player's own king is not in check.

        This method is used to detect checkmate (in check + no legal moves)
        and stalemate (not in check + no legal moves).

        The check is done by brute force: for each piece, try all 64 destination
        squares. For each valid candidate move, simulate it temporarily on the
        board and verify that the king is not under attack. Returns True as soon
        as one legal move is found (short-circuit for performance).

        Args:
            color: The color to check ("white" or "black").

        Returns:
            True if at least one legal move exists, False otherwise.
        """
        opponent_color = "black" if color == "white" else "white"
        letters = "ABCDEFGH"

        for from_pos, piece in self.pieces_of_color(color):
            for col in letters:
                for row in range(1, 9):
                    to_pos = Position(strpos=f"{col}{row}")

                    if from_pos == to_pos:
                        continue

                    # Cannot capture own piece
                    target = self.piece_at(to_pos)
                    if target is not None and target.color == color:
                        continue

                    # Piece must allow this move
                    if not piece.is_authorized_move(from_pos, to_pos, self):
                        continue

                    # Simulate the move to verify king safety.
                    # In chess, a move is only legal if it does not leave the
                    # player's own king in check. This catches:
                    # - Moving a pinned piece (would expose king to attacker)
                    # - Failing to block or escape an existing check
                    # - King moving to an attacked square (also caught by King itself)
                    saved_pieces = self.pieces[:]

                    # Remove captured piece at destination
                    self.pieces = [(p, pc) for p, pc in self.pieces if p != to_pos]

                    # Move the piece from source to destination
                    for i, (p, pc) in enumerate(self.pieces):
                        if p == from_pos:
                            self.pieces[i] = (to_pos, pc)
                            break

                    # Check if our king is safe after the simulated move
                    king_pos = self.find_king(color)
                    in_check = self.is_under_attack(king_pos, opponent_color)

                    # Restore the board to its original state
                    self.pieces = saved_pieces

                    # If the king is not in check after this move, it's legal
                    if not in_check:
                        return True

        return False

    def is_check(self, color):
        """
        Check whether the king of the given color is currently in check.

        A king is in check when it is under attack by at least one opponent piece.

        Args:
            color: The color of the king to check ("white" or "black").

        Returns:
            True if the king is in check, False otherwise.
        """
        opponent_color = "black" if color == "white" else "white"
        king_pos = self.find_king(color)
        return self.is_under_attack(king_pos, opponent_color)

    def is_checkmate(self, color):
        """
        Check whether the player of the given color is in checkmate.

        Checkmate occurs when the king is in check AND the player has no legal
        moves to escape, block, or capture the attacker. This ends the game
        with the opponent as the winner.

        Args:
            color: The color to check ("white" or "black").

        Returns:
            True if the player is in checkmate.
        """
        return self.is_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color):
        """
        Check whether the player of the given color is in stalemate (pat).

        Stalemate occurs when the player is NOT in check but has no legal moves.
        This results in a draw. It is different from checkmate because the king
        is not under attack.

        Args:
            color: The color to check ("white" or "black").

        Returns:
            True if the player is in stalemate.
        """
        return not self.is_check(color) and not self.has_legal_moves(color)

    def is_insufficient_material(self):
        """
        Check whether neither player has enough pieces to deliver checkmate.

        The following configurations are recognized as insufficient material:
        - King vs King: no pieces can deliver checkmate.
        - King + Bishop vs King: a lone bishop cannot force checkmate.
        - King + Knight vs King: a lone knight cannot force checkmate.
        - King + Bishop vs King + Bishop (same color square): when both bishops
          move on the same color squares, checkmate is impossible.

        Returns:
            True if the game is a draw due to insufficient material.
        """
        white_pieces = self.pieces_of_color("white")
        black_pieces = self.pieces_of_color("black")

        # Separate out the kings — they always exist, so we only care about
        # the remaining "non-king" pieces to determine material sufficiency.
        white_non_king = [(pos, p) for pos, p in white_pieces if not isinstance(p, King)]
        black_non_king = [(pos, p) for pos, p in black_pieces if not isinstance(p, King)]

        # King vs King: both sides have only their king — no piece can deliver checkmate
        if len(white_non_king) == 0 and len(black_non_king) == 0:
            return True

        # King + minor piece vs King: a single bishop or knight cannot force
        # checkmate against a lone king. (Two knights can in theory, but it
        # cannot be forced, so FIDE considers it insufficient material.)
        if len(white_non_king) == 1 and len(black_non_king) == 0:
            if isinstance(white_non_king[0][1], (Bishop, Knight)):
                return True

        if len(black_non_king) == 1 and len(white_non_king) == 0:
            if isinstance(black_non_king[0][1], (Bishop, Knight)):
                return True

        # King + Bishop vs King + Bishop on the same color square:
        # Each bishop can only ever reach half the squares (light or dark).
        # The "color" of a square is determined by (column + row) % 2:
        #   even = dark square, odd = light square (or vice versa).
        # If both bishops are on the same color, they can never interact,
        # making checkmate impossible.
        if len(white_non_king) == 1 and len(black_non_king) == 1:
            if isinstance(white_non_king[0][1], Bishop) and isinstance(black_non_king[0][1], Bishop):
                w_pos = white_non_king[0][0]
                b_pos = black_non_king[0][0]
                # Same parity = same square color = insufficient material
                if (w_pos.hor() + w_pos.ver()) % 2 == (b_pos.hor() + b_pos.ver()) % 2:
                    return True

        return False
