"""
Chess GUI module using pygame.

Provides a graphical interface for the chess game. The board is rendered with
alternating light/dark squares, and pieces are drawn using Unicode chess symbols.

Players interact by clicking: first click selects a piece, second click moves it.
Legal moves are highlighted with green dots. The status bar shows the current player,
check/checkmate/draw messages, and provides QUIT and DRAW buttons.

Usage:
    python3 -m chess.gui
"""

import sys
from unittest.mock import patch

import pygame

from chess.board import Board
from chess.king import King
from chess.knight import Knight
from chess.bishop import Bishop
from chess.queen import Queen
from chess.rook import Rook
from chess.pawn import Pawn
from chess.move import Move
from chess.player import Player
from chess.position import Position


# ============================================================================
# CONSTANTS
# ============================================================================

SQUARE_SIZE = 80
BOARD_SIZE = SQUARE_SIZE * 8
STATUS_HEIGHT = 80
WINDOW_WIDTH = BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE + STATUS_HEIGHT

# Colors
COLOR_LIGHT_SQUARE = (240, 217, 181)
COLOR_DARK_SQUARE = (181, 136, 99)
COLOR_SELECTED = (255, 255, 100, 150)
COLOR_LEGAL_MOVE = (100, 200, 100, 180)
COLOR_LAST_MOVE = (170, 210, 255, 120)
COLOR_CHECK = (255, 80, 80, 150)
COLOR_STATUS_BG = (50, 50, 50)
COLOR_STATUS_TEXT = (220, 220, 220)
COLOR_BUTTON = (80, 80, 80)
COLOR_BUTTON_HOVER = (110, 110, 110)
COLOR_BUTTON_TEXT = (220, 220, 220)
COLOR_PROMO_BG = (60, 60, 60, 230)
COLOR_PROMO_HOVER = (100, 100, 100)

# Unicode chess piece symbols
PIECE_SYMBOLS = {
    ("King", "white"): "\u2654",
    ("Queen", "white"): "\u2655",
    ("Rook", "white"): "\u2656",
    ("Bishop", "white"): "\u2657",
    ("Knight", "white"): "\u2658",
    ("Pawn", "white"): "\u2659",
    ("King", "black"): "\u265A",
    ("Queen", "black"): "\u265B",
    ("Rook", "black"): "\u265C",
    ("Bishop", "black"): "\u265D",
    ("Knight", "black"): "\u265E",
    ("Pawn", "black"): "\u265F",
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def pixel_to_board(*, x, y):
    """
    Convert pixel coordinates to board column and row.

    The board is drawn with A1 at the bottom-left.
    Column: 0-7 maps to A-H (left to right).
    Row: 0-7 maps to 8-1 (top to bottom), so row 0 = rank 8, row 7 = rank 1.

    Returns:
        (col, row) where col is 1-8 (A-H) and row is 1-8 (ranks).
    """
    col = x // SQUARE_SIZE + 1
    row = 8 - y // SQUARE_SIZE

    return col, row


def board_to_pixel(*, col, row):
    """
    Convert board column and row to pixel coordinates (top-left of square).

    Args:
        col: 1-8 (A-H).
        row: 1-8 (ranks).

    Returns:
        (px, py) pixel coordinates.
    """
    px = (col - 1) * SQUARE_SIZE
    py = (8 - row) * SQUARE_SIZE

    return px, py


def col_row_to_strpos(*, col, row):
    """Convert column (1-8) and row (1-8) to algebraic notation string."""
    letters = "ABCDEFGH"

    return f"{letters[col - 1]}{row}"


def get_piece_symbol(*, piece):
    """Get the Unicode symbol for a piece."""
    piece_type = type(piece).__name__

    return PIECE_SYMBOLS.get((piece_type, piece.color), "?")


def get_legal_moves(*, board, from_pos, color):
    """
    Get all legal destination positions for a piece at from_pos.

    Tests every square on the board and returns those where a valid Move
    can be constructed without raising ValueError.
    """
    legal = []
    letters = "ABCDEFGH"

    for col in range(1, 9):
        for row in range(1, 9):
            to_str = col_row_to_strpos(col=col, row=row)
            from_str = from_pos.strpos
            move_str = f"{from_str}-{to_str}"

            try:
                Move(from_to=move_str, board=board, color=color)
                legal.append(Position(strpos=to_str))
            except ValueError:
                pass

    return legal


# ============================================================================
# CHESS GUI CLASS
# ============================================================================

class ChessGUI:
    """
    Pygame-based graphical interface for the chess game.

    Attributes:
        screen: The pygame display surface.
        board: The Board object.
        moves: List of Move objects played.
        winner: The winning player color string, or None.
        draw: True if the game ended in a draw.
        current_color: "white" or "black" — whose turn it is.
        selected_pos: The Position of the currently selected piece, or None.
        legal_moves: List of legal destination Positions for the selected piece.
        last_move_from: Position of the last move's source, or None.
        last_move_to: Position of the last move's destination, or None.
        status_message: Text shown in the status bar.
        game_over: True if the game has ended.
        position_history: List of position keys for threefold repetition.
        half_move_clock: Counter for 50-move rule.
        promoting: True if a promotion dialog is currently shown.
        promotion_pos: The Position where the pawn needs to be promoted.
        promotion_color: The color of the pawn being promoted.
    """

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Chess")

        self.piece_font = pygame.font.SysFont("segoeuisymbol,dejavusans,noto,arial", 56)
        self.status_font = pygame.font.SysFont("arial", 20)
        self.button_font = pygame.font.SysFont("arial", 16, bold=True)
        self.label_font = pygame.font.SysFont("arial", 14)
        self.promo_font = pygame.font.SysFont("segoeuisymbol,dejavusans,noto,arial", 48)

        self.board = Board()
        self.moves = []
        self.winner = None
        self.draw = False
        self.current_color = "white"
        self.selected_pos = None
        self.legal_moves = []
        self.last_move_from = None
        self.last_move_to = None
        self.status_message = "White's turn"
        self.game_over = False
        self.position_history = [self.board.position_key()]
        self.half_move_clock = 0

        # Promotion state
        self.promoting = False
        self.promotion_pos = None
        self.promotion_color = None

        # Button rectangles (set during drawing)
        self.quit_button_rect = None
        self.draw_button_rect = None

    # ========================================================================
    # DRAWING
    # ========================================================================

    def draw_board(self):
        """Draw the chess board squares with highlights."""
        for col in range(8):
            for row in range(8):
                x = col * SQUARE_SIZE
                y = row * SQUARE_SIZE

                # Alternating colors
                if (col + row) % 2 == 0:
                    color = COLOR_LIGHT_SQUARE
                else:
                    color = COLOR_DARK_SQUARE

                pygame.draw.rect(self.screen, color, (x, y, SQUARE_SIZE, SQUARE_SIZE))

        # Highlight last move
        if self.last_move_from is not None:
            self._highlight_square(pos=self.last_move_from, color=COLOR_LAST_MOVE)

        if self.last_move_to is not None:
            self._highlight_square(pos=self.last_move_to, color=COLOR_LAST_MOVE)

        # Highlight king in check
        if not self.game_over:
            king_pos = self.board.find_king(color=self.current_color)

            if king_pos is not None and self.board.is_check(color=self.current_color):
                self._highlight_square(pos=king_pos, color=COLOR_CHECK)

        # Highlight selected square
        if self.selected_pos is not None:
            self._highlight_square(pos=self.selected_pos, color=COLOR_SELECTED)

        # Draw legal move indicators
        for move_pos in self.legal_moves:
            px, py = board_to_pixel(col=move_pos.hor(), row=move_pos.ver())
            center = (px + SQUARE_SIZE // 2, py + SQUARE_SIZE // 2)

            # If there's a piece to capture, draw a ring; otherwise a dot
            if self.board.piece_at(position=move_pos) is not None:
                pygame.draw.circle(self.screen, (100, 200, 100), center, SQUARE_SIZE // 2 - 4, 4)
            else:
                pygame.draw.circle(self.screen, (100, 200, 100, 180), center, 12)

    def _highlight_square(self, *, pos, color):
        """Draw a semi-transparent overlay on a square."""
        px, py = board_to_pixel(col=pos.hor(), row=pos.ver())
        surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        surface.fill(color)
        self.screen.blit(surface, (px, py))

    def draw_pieces(self):
        """Draw all pieces on the board using Unicode symbols."""
        for pos, piece in self.board.pieces:
            px, py = board_to_pixel(col=pos.hor(), row=pos.ver())
            symbol = get_piece_symbol(piece=piece)
            text = self.piece_font.render(symbol, True, (0, 0, 0))
            text_rect = text.get_rect(center=(px + SQUARE_SIZE // 2, py + SQUARE_SIZE // 2))
            self.screen.blit(text, text_rect)

    def draw_coordinates(self):
        """Draw file letters (A-H) and rank numbers (1-8) on the board edges."""
        letters = "abcdefgh"

        for i in range(8):
            # File letters at the bottom
            label = self.label_font.render(letters[i], True,
                COLOR_DARK_SQUARE if i % 2 == 0 else COLOR_LIGHT_SQUARE)
            self.screen.blit(label, (i * SQUARE_SIZE + SQUARE_SIZE - 14, BOARD_SIZE - 16))

            # Rank numbers on the left
            label = self.label_font.render(str(8 - i), True,
                COLOR_LIGHT_SQUARE if i % 2 == 0 else COLOR_DARK_SQUARE)
            self.screen.blit(label, (3, i * SQUARE_SIZE + 3))

    def draw_status_bar(self):
        """Draw the status bar at the bottom with message and buttons."""
        bar_y = BOARD_SIZE

        # Background
        pygame.draw.rect(self.screen, COLOR_STATUS_BG, (0, bar_y, WINDOW_WIDTH, STATUS_HEIGHT))

        # Status message
        text = self.status_font.render(self.status_message, True, COLOR_STATUS_TEXT)
        self.screen.blit(text, (15, bar_y + 10))

        mouse_pos = pygame.mouse.get_pos()

        if not self.game_over:
            # QUIT button
            self.quit_button_rect = pygame.Rect(WINDOW_WIDTH - 180, bar_y + 45, 75, 28)
            quit_color = COLOR_BUTTON_HOVER if self.quit_button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
            pygame.draw.rect(self.screen, quit_color, self.quit_button_rect, border_radius=4)
            quit_text = self.button_font.render("RESIGN", True, COLOR_BUTTON_TEXT)
            quit_text_rect = quit_text.get_rect(center=self.quit_button_rect.center)
            self.screen.blit(quit_text, quit_text_rect)

            # DRAW button
            self.draw_button_rect = pygame.Rect(WINDOW_WIDTH - 90, bar_y + 45, 75, 28)
            draw_color = COLOR_BUTTON_HOVER if self.draw_button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
            pygame.draw.rect(self.screen, draw_color, self.draw_button_rect, border_radius=4)
            draw_text = self.button_font.render("DRAW", True, COLOR_BUTTON_TEXT)
            draw_text_rect = draw_text.get_rect(center=self.draw_button_rect.center)
            self.screen.blit(draw_text, draw_text_rect)

        else:
            # RESTART button
            self.restart_button_rect = pygame.Rect(WINDOW_WIDTH - 120, bar_y + 45, 100, 28)
            restart_color = COLOR_BUTTON_HOVER if self.restart_button_rect.collidepoint(mouse_pos) else COLOR_BUTTON
            pygame.draw.rect(self.screen, restart_color, self.restart_button_rect, border_radius=4)
            restart_text = self.button_font.render("NEW GAME", True, COLOR_BUTTON_TEXT)
            restart_text_rect = restart_text.get_rect(center=self.restart_button_rect.center)
            self.screen.blit(restart_text, restart_text_rect)

    def draw_promotion_dialog(self):
        """Draw the promotion choice dialog over the board."""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # Dialog box
        dialog_w, dialog_h = 360, 120
        dialog_x = (WINDOW_WIDTH - dialog_w) // 2
        dialog_y = (BOARD_SIZE - dialog_h) // 2

        pygame.draw.rect(self.screen, (60, 60, 60), (dialog_x, dialog_y, dialog_w, dialog_h), border_radius=8)
        pygame.draw.rect(self.screen, (120, 120, 120), (dialog_x, dialog_y, dialog_w, dialog_h), 2, border_radius=8)

        # Title
        title = self.status_font.render("Promote pawn to:", True, COLOR_STATUS_TEXT)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, dialog_y + 20))
        self.screen.blit(title, title_rect)

        # Four piece choices
        color = self.promotion_color
        pieces = [
            (Queen(color=color), "Q"),
            (Rook(color=color), "R"),
            (Bishop(color=color), "B"),
            (Knight(color=color), "K"),
        ]

        mouse_pos = pygame.mouse.get_pos()
        self._promo_rects = []

        for i, (piece, label) in enumerate(pieces):
            rect_x = dialog_x + 20 + i * 85
            rect_y = dialog_y + 45
            rect = pygame.Rect(rect_x, rect_y, 70, 60)
            self._promo_rects.append((rect, label))

            # Hover effect
            bg_color = COLOR_PROMO_HOVER if rect.collidepoint(mouse_pos) else (80, 80, 80)
            pygame.draw.rect(self.screen, bg_color, rect, border_radius=6)

            # Piece symbol
            symbol = get_piece_symbol(piece=piece)
            text = self.promo_font.render(symbol, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    # ========================================================================
    # GAME LOGIC
    # ========================================================================

    def handle_square_click(self, *, col, row):
        """Handle a click on a board square."""
        if self.game_over or self.promoting:

            return

        clicked_pos = Position(strpos=col_row_to_strpos(col=col, row=row))

        # If no piece is selected yet
        if self.selected_pos is None:
            piece = self.board.piece_at(position=clicked_pos)

            if piece is not None and piece.color == self.current_color:
                self.selected_pos = clicked_pos
                self.legal_moves = get_legal_moves(
                    board=self.board, from_pos=clicked_pos, color=self.current_color
                )

            return

        # A piece is already selected — try to move
        # Check if clicking the same square (deselect)
        if clicked_pos == self.selected_pos:
            self.selected_pos = None
            self.legal_moves = []

            return

        # Check if clicking another own piece (switch selection)
        piece = self.board.piece_at(position=clicked_pos)

        if piece is not None and piece.color == self.current_color:
            self.selected_pos = clicked_pos
            self.legal_moves = get_legal_moves(
                board=self.board, from_pos=clicked_pos, color=self.current_color
            )

            return

        # Try to execute the move
        from_str = self.selected_pos.strpos
        to_str = clicked_pos.strpos
        move_str = f"{from_str}-{to_str}"

        try:
            move = Move(from_to=move_str, board=self.board, color=self.current_color)
        except ValueError:
            # Invalid move — deselect
            self.selected_pos = None
            self.legal_moves = []

            return

        self._execute_move(move=move)

    def _execute_move(self, *, move):
        """Execute a validated move and update game state."""
        self.moves.append(move)

        # Track 50-move rule before executing
        moving_piece = self.board.piece_at(position=move.from_pos)
        is_pawn_move = isinstance(moving_piece, Pawn)
        is_capture = self.board.piece_at(position=move.to_pos) is not None

        # Check if this is a pawn promotion
        if isinstance(moving_piece, Pawn):
            promotion_row = 8 if moving_piece.color == "white" else 1

            if move.to_pos.ver() == promotion_row:
                # Start promotion dialog — don't execute the move yet
                self.promoting = True
                self.promotion_pos = move.to_pos
                self.promotion_color = moving_piece.color
                self._pending_move = move
                self._pending_is_pawn_move = is_pawn_move
                self._pending_is_capture = is_capture
                self.selected_pos = None
                self.legal_moves = []

                return

        # Execute the move on the board
        self.board.move_piece(from_pos=move.from_pos, to_pos=move.to_pos)

        self._after_move(
            move=move, is_pawn_move=is_pawn_move, is_capture=is_capture
        )

    def _complete_promotion(self, *, choice):
        """Complete a pending pawn promotion move."""
        move = self._pending_move

        # Execute the move with the promotion choice patched
        with patch("builtins.input", return_value=choice):
            self.board.move_piece(from_pos=move.from_pos, to_pos=move.to_pos)

        self.promoting = False
        self.promotion_pos = None
        self.promotion_color = None

        self._after_move(
            move=move,
            is_pawn_move=self._pending_is_pawn_move,
            is_capture=self._pending_is_capture
        )

    def _after_move(self, *, move, is_pawn_move, is_capture):
        """Post-move processing: update clocks, check game state, switch turns."""
        # Update 50-move clock
        if is_pawn_move or is_capture:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1

        # Track position for threefold repetition
        self.position_history.append(self.board.position_key())

        # Track last move for highlighting
        self.last_move_from = move.from_pos
        self.last_move_to = move.to_pos

        # Clear selection
        self.selected_pos = None
        self.legal_moves = []

        # Switch turns
        self.current_color = "black" if self.current_color == "white" else "white"
        opponent = "white" if self.current_color == "white" else "black"

        # Check game state
        if self.board.is_checkmate(color=self.current_color):
            self.game_over = True
            self.winner = opponent
            self.status_message = f"Checkmate! {opponent.capitalize()} wins!"

        elif self.board.is_stalemate(color=self.current_color):
            self.game_over = True
            self.draw = True
            self.status_message = "Stalemate! The game is a draw."

        elif self.board.is_insufficient_material():
            self.game_over = True
            self.draw = True
            self.status_message = "Draw by insufficient material."

        elif self._is_threefold_repetition():
            self.game_over = True
            self.draw = True
            self.status_message = "Draw by threefold repetition."

        elif self.half_move_clock >= 100:
            self.game_over = True
            self.draw = True
            self.status_message = "Draw by 50-move rule."

        elif self.board.is_check(color=self.current_color):
            self.status_message = f"{self.current_color.capitalize()}'s turn (CHECK!)"

        else:
            self.status_message = f"{self.current_color.capitalize()}'s turn"

    def _is_threefold_repetition(self):
        """Check for threefold repetition."""
        current = self.position_history[-1]

        return self.position_history.count(current) >= 3

    def handle_resign(self):
        """Handle the resign button click."""
        if self.game_over:

            return

        opponent = "black" if self.current_color == "white" else "white"
        self.winner = opponent
        self.game_over = True
        self.status_message = f"{self.current_color.capitalize()} resigns. {opponent.capitalize()} wins!"

    def handle_draw_offer(self):
        """Handle the draw button click — auto-accept for simplicity."""
        if self.game_over:

            return

        self.draw = True
        self.game_over = True
        self.status_message = "Game ended in a draw by agreement."

    def restart(self):
        """Reset all game state and start a new game."""
        self.board = Board()
        self.moves = []
        self.winner = None
        self.draw = False
        self.current_color = "white"
        self.selected_pos = None
        self.legal_moves = []
        self.last_move_from = None
        self.last_move_to = None
        self.status_message = "White's turn"
        self.game_over = False
        self.position_history = [self.board.position_key()]
        self.half_move_clock = 0
        self.promoting = False
        self.promotion_pos = None
        self.promotion_color = None
        self.restart_button_rect = None

    # ========================================================================
    # MAIN LOOP
    # ========================================================================

    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos

                    # Check promotion dialog clicks
                    if self.promoting and hasattr(self, '_promo_rects'):
                        for rect, label in self._promo_rects:
                            if rect.collidepoint(x, y):
                                self._complete_promotion(choice=label)
                                break

                        continue

                    # Check button clicks
                    if self.restart_button_rect and self.restart_button_rect.collidepoint(x, y):
                        self.restart()
                        continue

                    if self.quit_button_rect and self.quit_button_rect.collidepoint(x, y):
                        self.handle_resign()
                        continue

                    if self.draw_button_rect and self.draw_button_rect.collidepoint(x, y):
                        self.handle_draw_offer()
                        continue

                    # Check board clicks
                    if y < BOARD_SIZE:
                        col, row = pixel_to_board(x=x, y=y)

                        if 1 <= col <= 8 and 1 <= row <= 8:
                            self.handle_square_click(col=col, row=row)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # Draw everything
            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_pieces()
            self.draw_coordinates()
            self.draw_status_bar()

            if self.promoting:
                self.draw_promotion_dialog()

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    gui = ChessGUI()
    gui.run()
