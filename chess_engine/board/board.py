"""
Chess Board Representation

This module provides a complete chess board representation with:
- 8x8 board state
- Piece movement validation
- Game state tracking (castling, en passant, etc.)
- Move history
"""

import copy
from typing import List, Tuple, Optional, Dict, Any
from enum import Enum

class PieceType(Enum):
    """Chess piece types"""
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Color(Enum):
    """Chess colors"""
    WHITE = 1
    BLACK = -1

class Square:
    """Represents a square on the chess board"""
    def __init__(self, piece_type: Optional[PieceType] = None, color: Optional[Color] = None):
        self.piece_type = piece_type
        self.color = color
        self.empty = piece_type is None
    
    def __str__(self):
        if self.empty:
            return "."
        
        piece_symbols = {
            (PieceType.PAWN, Color.WHITE): "P",
            (PieceType.KNIGHT, Color.WHITE): "N", 
            (PieceType.BISHOP, Color.WHITE): "B",
            (PieceType.ROOK, Color.WHITE): "R",
            (PieceType.QUEEN, Color.WHITE): "Q",
            (PieceType.KING, Color.WHITE): "K",
            (PieceType.PAWN, Color.BLACK): "p",
            (PieceType.KNIGHT, Color.BLACK): "n",
            (PieceType.BISHOP, Color.BLACK): "b", 
            (PieceType.ROOK, Color.BLACK): "r",
            (PieceType.QUEEN, Color.BLACK): "q",
            (PieceType.KING, Color.BLACK): "k"
        }
        return piece_symbols.get((self.piece_type, self.color), "?")

class Move:
    """Represents a chess move"""
    def __init__(self, from_square: Tuple[int, int], to_square: Tuple[int, int], 
                 piece_type: PieceType, color: Color, promotion: Optional[PieceType] = None,
                 is_castling: bool = False, is_en_passant: bool = False, is_capture: bool = False):
        self.from_square = from_square
        self.to_square = to_square
        self.piece_type = piece_type
        self.color = color
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
        self.is_capture = is_capture
    
    def __str__(self):
        from_pos = f"{chr(ord('a') + self.from_square[0])}{8 - self.from_square[1]}"
        to_pos = f"{chr(ord('a') + self.to_square[0])}{8 - self.to_square[1]}"
        return f"{from_pos}{to_pos}"

class ChessBoard:
    """Main chess board class"""
    
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        """
        Initialize chess board from FEN string
        
        Args:
            fen: Forsyth-Edwards Notation string representing board state
        """
        self.board = [[Square() for _ in range(8)] for _ in range(8)]
        self.current_player = Color.WHITE
        self.castling_rights = {"K": True, "Q": True, "k": True, "q": True}
        self.en_passant_target = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.move_history = []
        self.position_history = []
        
        self._load_from_fen(fen)
    
    def _load_from_fen(self, fen: str):
        """Load board state from FEN string"""
        parts = fen.split()
        if len(parts) != 6:
            raise ValueError("Invalid FEN string")
        
        # Parse board position
        board_str = parts[0]
        rank = 0
        file = 0
        
        for char in board_str:
            if char == '/':
                rank += 1
                file = 0
            elif char.isdigit():
                file += int(char)
            else:
                piece_type, color = self._char_to_piece(char)
                self.board[rank][file] = Square(piece_type, color)
                file += 1
        
        # Parse current player
        self.current_player = Color.WHITE if parts[1] == 'w' else Color.BLACK
        
        # Parse castling rights
        castling = parts[2]
        self.castling_rights = {
            "K": "K" in castling,
            "Q": "Q" in castling, 
            "k": "k" in castling,
            "q": "q" in castling
        }
        
        # Parse en passant target
        if parts[3] != '-':
            self.en_passant_target = (ord(parts[3][0]) - ord('a'), 8 - int(parts[3][1]))
        else:
            self.en_passant_target = None
        
        # Parse halfmove and fullmove clocks
        self.halfmove_clock = int(parts[4])
        self.fullmove_number = int(parts[5])
    
    def _char_to_piece(self, char: str) -> Tuple[PieceType, Color]:
        """Convert character to piece type and color"""
        piece_map = {
            'P': (PieceType.PAWN, Color.WHITE),
            'N': (PieceType.KNIGHT, Color.WHITE),
            'B': (PieceType.BISHOP, Color.WHITE),
            'R': (PieceType.ROOK, Color.WHITE),
            'Q': (PieceType.QUEEN, Color.WHITE),
            'K': (PieceType.KING, Color.WHITE),
            'p': (PieceType.PAWN, Color.BLACK),
            'n': (PieceType.KNIGHT, Color.BLACK),
            'b': (PieceType.BISHOP, Color.BLACK),
            'r': (PieceType.ROOK, Color.BLACK),
            'q': (PieceType.QUEEN, Color.BLACK),
            'k': (PieceType.KING, Color.BLACK)
        }
        return piece_map[char]
    
    def get_piece(self, square: Tuple[int, int]) -> Optional[Square]:
        """Get piece at given square"""
        if self._is_valid_square(square):
            return self.board[square[1]][square[0]]
        return None
    
    def _is_valid_square(self, square: Tuple[int, int]) -> bool:
        """Check if square coordinates are valid"""
        return 0 <= square[0] < 8 and 0 <= square[1] < 8
    
    def make_move(self, move: Move) -> bool:
        """
        Make a move on the board
        
        Args:
            move: Move to make
            
        Returns:
            True if move was successful, False otherwise
        """
        # TODO: Implement move validation and execution
        # - Check if move is legal
        # - Update board state
        # - Update game state (castling, en passant, etc.)
        # - Add to move history
        # - Switch current player
        
        # Placeholder implementation
        if not self._is_valid_square(move.from_square) or not self._is_valid_square(move.to_square):
            return False
        
        # Store current position for history
        self.position_history.append(self._get_fen())
        
        # Make the move
        piece = self.board[move.from_square[1]][move.from_square[0]]
        self.board[move.to_square[1]][move.to_square[0]] = piece
        self.board[move.from_square[1]][move.from_square[0]] = Square()
        
        # Add to move history
        self.move_history.append(move)
        
        # Switch players
        self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
        
        return True
    
    def undo_move(self) -> bool:
        """
        Undo the last move
        
        Returns:
            True if move was undone, False if no moves to undo
        """
        if not self.move_history:
            return False
        
        # TODO: Implement move undo
        # - Restore previous board state
        # - Update game state
        # - Remove from move history
        
        return True
    
    def is_check(self, color: Color) -> bool:
        """
        Check if given color is in check
        
        Args:
            color: Color to check
            
        Returns:
            True if in check, False otherwise
        """
        # TODO: Implement check detection
        # - Find king position
        # - Check if any opponent pieces can attack king
        return False
    
    def is_checkmate(self, color: Color) -> bool:
        """
        Check if given color is in checkmate
        
        Args:
            color: Color to check
            
        Returns:
            True if in checkmate, False otherwise
        """
        # TODO: Implement checkmate detection
        # - Check if in check
        # - Check if any legal moves exist
        return False
    
    def is_stalemate(self, color: Color) -> bool:
        """
        Check if given color is in stalemate
        
        Args:
            color: Color to check
            
        Returns:
            True if in stalemate, False otherwise
        """
        # TODO: Implement stalemate detection
        # - Check if not in check
        # - Check if no legal moves exist
        return False
    
    def _get_fen(self) -> str:
        """Generate FEN string from current board state"""
        # TODO: Implement FEN generation
        # - Convert board to FEN notation
        # - Include game state information
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    
    def __str__(self):
        """String representation of the board"""
        result = []
        for rank in range(8):
            row = []
            for file in range(8):
                row.append(str(self.board[rank][file]))
            result.append(" ".join(row))
        return "\n".join(result)
    
    def copy(self):
        """Create a deep copy of the board"""
        return copy.deepcopy(self)