from chess.bishop import Bishop
from chess.king import King
from chess.knight import Knight
from chess.pawn import Pawn
from chess.piece import Piece
from chess.position import Position
from chess.queen import Queen
from chess.rook import Rook


class Board:
    def __init__(self):
        self.pieces = []
        self.last_move = None

        self.populate()

    def _put(self, *, piece: Piece, position: str):
        pos = Position(strpos=position)
        self.pieces.append((pos, piece))

    def populate(self):
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
        for pos, piece in self.pieces:
            if pos == position:
                return piece
        return None

    def move_piece(self, from_pos: Position, to_pos: Position):
        piece = self.piece_at(from_pos)

        # Handle en-passant: pawn captures diagonally to empty square
        if isinstance(piece, Pawn) and from_pos.hor() != to_pos.hor() and self.piece_at(to_pos) is None:
            captured_pos = Position(strpos=f"{to_pos.strpos[0]}{from_pos.ver()}")
            self.pieces = [(pos, p) for pos, p in self.pieces if pos != captured_pos]

        # Remove captured piece at destination
        self.pieces = [(pos, p) for pos, p in self.pieces if pos != to_pos]

        # Move the piece
        for i, (pos, p) in enumerate(self.pieces):
            if pos == from_pos:
                self.pieces[i] = (to_pos, p)
                break

        # Track has_moved for king and rook (for castling)
        if hasattr(piece, 'has_moved'):
            piece.has_moved = True

        # Handle castling: if king moved 2 squares, also move the rook
        if isinstance(piece, King) and abs(to_pos.hor() - from_pos.hor()) == 2:
            row = from_pos.ver()
            if to_pos.hor() > from_pos.hor():
                # Kingside
                rook_from = Position(strpos=f"H{row}")
                rook_to = Position(strpos=f"F{row}")
            else:
                # Queenside
                rook_from = Position(strpos=f"A{row}")
                rook_to = Position(strpos=f"D{row}")

            for i, (pos, p) in enumerate(self.pieces):
                if pos == rook_from:
                    self.pieces[i] = (rook_to, p)
                    p.has_moved = True
                    break

        # Handle pawn promotion
        if isinstance(piece, Pawn):
            promotion_row = 8 if piece.color == "white" else 1
            if to_pos.ver() == promotion_row:
                self._promote_pawn(to_pos, piece.color)

        # Track last move for en-passant
        self.last_move = (from_pos, to_pos, piece)

    def _promote_pawn(self, position, color):
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

    def pieces_of_color(self, color):
        return [(pos, piece) for pos, piece in self.pieces if piece.color == color]

    def find_king(self, color):
        for pos, piece in self.pieces:
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def is_under_attack(self, position, by_color):
        for pos, piece in self.pieces_of_color(by_color):
            if piece.is_authorized_move(pos, position, self):
                return True
        return False

    def has_legal_moves(self, color):
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

                    # Simulate the move and check if own king is still safe
                    saved_pieces = self.pieces[:]
                    self.pieces = [(p, pc) for p, pc in self.pieces if p != to_pos]
                    for i, (p, pc) in enumerate(self.pieces):
                        if p == from_pos:
                            self.pieces[i] = (to_pos, pc)
                            break

                    king_pos = self.find_king(color)
                    in_check = self.is_under_attack(king_pos, opponent_color)

                    self.pieces = saved_pieces

                    if not in_check:
                        return True

        return False

    def is_check(self, color):
        opponent_color = "black" if color == "white" else "white"
        king_pos = self.find_king(color)
        return self.is_under_attack(king_pos, opponent_color)

    def is_checkmate(self, color):
        return self.is_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color):
        return not self.is_check(color) and not self.has_legal_moves(color)

    def is_insufficient_material(self):
        white_pieces = self.pieces_of_color("white")
        black_pieces = self.pieces_of_color("black")

        white_non_king = [(pos, p) for pos, p in white_pieces if not isinstance(p, King)]
        black_non_king = [(pos, p) for pos, p in black_pieces if not isinstance(p, King)]

        # King vs King
        if len(white_non_king) == 0 and len(black_non_king) == 0:
            return True

        # King + Bishop vs King or King + Knight vs King
        if len(white_non_king) == 1 and len(black_non_king) == 0:
            if isinstance(white_non_king[0][1], (Bishop, Knight)):
                return True

        if len(black_non_king) == 1 and len(white_non_king) == 0:
            if isinstance(black_non_king[0][1], (Bishop, Knight)):
                return True

        # King + Bishop vs King + Bishop (same color square)
        if len(white_non_king) == 1 and len(black_non_king) == 1:
            if isinstance(white_non_king[0][1], Bishop) and isinstance(black_non_king[0][1], Bishop):
                w_pos = white_non_king[0][0]
                b_pos = black_non_king[0][0]
                if (w_pos.hor() + w_pos.ver()) % 2 == (b_pos.hor() + b_pos.ver()) % 2:
                    return True

        return False
