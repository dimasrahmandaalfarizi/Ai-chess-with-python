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
        try:
            # Validate move
            if not self._is_valid_square(move.from_square) or not self._is_valid_square(move.to_square):
                return False
            
            from_file, from_rank = move.from_square
            to_file, to_rank = move.to_square
            
            # Get piece at source
            piece = self.board[from_rank][from_file]
            if piece.empty or piece.color != self.current_player:
                return False
            
            # Store current state for undo
            board_state = {
                'board': copy.deepcopy(self.board),
                'castling_rights': self.castling_rights.copy(),
                'en_passant_target': self.en_passant_target,
                'halfmove_clock': self.halfmove_clock,
                'fullmove_number': self.fullmove_number,
                'current_player': self.current_player
            }
            self.position_history.append(board_state)
            
            # Handle special moves
            captured_piece = None
            
            # En passant capture
            if move.is_en_passant:
                # Remove the captured pawn
                if self.current_player == Color.WHITE:
                    captured_piece = self.board[to_rank + 1][to_file]
                    self.board[to_rank + 1][to_file] = Square()
                else:
                    captured_piece = self.board[to_rank - 1][to_file]
                    self.board[to_rank - 1][to_file] = Square()
            
            # Regular capture
            elif move.is_capture:
                captured_piece = self.board[to_rank][to_file]
            
            # Castling
            if move.is_castling:
                # Move the rook
                if to_file > from_file:  # Kingside
                    rook = self.board[from_rank][7]
                    self.board[from_rank][5] = rook
                    self.board[from_rank][7] = Square()
                else:  # Queenside
                    rook = self.board[from_rank][0]
                    self.board[from_rank][3] = rook
                    self.board[from_rank][0] = Square()
            
            # Make the move
            self.board[to_rank][to_file] = piece
            self.board[from_rank][from_file] = Square()
            
            # Handle promotion
            if move.promotion:
                self.board[to_rank][to_file] = Square(move.promotion, piece.color)
            
            # Update castling rights
            self._update_castling_rights(move)
            
            # Update en passant target
            self._update_en_passant_target(move)
            
            # Update halfmove clock
            if piece.piece_type == PieceType.PAWN or captured_piece:
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1
            
            # Update fullmove number
            if self.current_player == Color.BLACK:
                self.fullmove_number += 1
            
            # Add to move history
            self.move_history.append(move)
            
            # Switch players
            self.current_player = Color.BLACK if self.current_player == Color.WHITE else Color.WHITE
            
            # Check if move puts own king in check (illegal move)
            if self.is_check(Color.BLACK if self.current_player == Color.WHITE else Color.WHITE):
                # Undo the move
                self.undo_move()
                return False
            
            return True
            
        except Exception as e:
            # If any error occurs, don't make the move
            return False
    
    def undo_move(self) -> bool:
        """
        Undo the last move
        
        Returns:
            True if move was undone, False if no moves to undo
        """
        if not self.move_history or not self.position_history:
            return False
        
        try:
            # Remove last move
            self.move_history.pop()
            
            # Restore previous state
            previous_state = self.position_history.pop()
            
            self.board = previous_state['board']
            self.castling_rights = previous_state['castling_rights']
            self.en_passant_target = previous_state['en_passant_target']
            self.halfmove_clock = previous_state['halfmove_clock']
            self.fullmove_number = previous_state['fullmove_number']
            self.current_player = previous_state['current_player']
            
            return True
            
        except Exception:
            return False
    
    def is_check(self, color: Color) -> bool:
        """
        Check if given color is in check
        
        Args:
            color: Color to check
            
        Returns:
            True if in check, False otherwise
        """
        # Find king position
        king_pos = None
        for rank in range(8):
            for file in range(8):
                square = self.board[rank][file]
                if not square.empty and square.piece_type == PieceType.KING and square.color == color:
                    king_pos = (file, rank)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False  # No king found
        
        # Check if any opponent piece can attack the king
        opponent_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        for rank in range(8):
            for file in range(8):
                square = self.board[rank][file]
                if not square.empty and square.color == opponent_color:
                    if self._can_piece_attack(square.piece_type, (file, rank), king_pos):
                        return True
        
        return False
    
    def is_checkmate(self, color: Color) -> bool:
        """
        Check if given color is in checkmate
        
        Args:
            color: Color to check
            
        Returns:
            True if in checkmate, False otherwise
        """
        # Must be in check to be checkmate
        if not self.is_check(color):
            return False
        
        # Check if any legal moves exist by generating pseudo-legal moves
        # and checking if any are actually legal
        has_legal_move = False
        
        for rank in range(8):
            for file in range(8):
                square = self.get_piece((file, rank))
                if square and not square.empty and square.color == color:
                    # Generate pseudo-legal moves for this piece
                    pseudo_moves = self._generate_pseudo_legal_moves_for_piece((file, rank), square)
                    
                    # Test if any move is legal
                    for move in pseudo_moves:
                        board_copy = self.copy()
                        # Temporarily set the current player to the color we're testing
                        original_player = board_copy.current_player
                        board_copy.current_player = color
                        
                        if board_copy.make_move(move):
                            if not board_copy.is_check(color):
                                has_legal_move = True
                                break
                        
                        # Restore original player (though we're using a copy)
                        board_copy.current_player = original_player
                    
                    if has_legal_move:
                        break
            
            if has_legal_move:
                break
        
        return not has_legal_move
    
    def is_stalemate(self, color: Color) -> bool:
        """
        Check if given color is in stalemate
        
        Args:
            color: Color to check
            
        Returns:
            True if in stalemate, False otherwise
        """
        # Must NOT be in check to be stalemate
        if self.is_check(color):
            return False
        
        # Check if no legal moves exist by generating pseudo-legal moves
        # and checking if any are actually legal
        has_legal_move = False
        
        for rank in range(8):
            for file in range(8):
                square = self.get_piece((file, rank))
                if square and not square.empty and square.color == color:
                    # Generate pseudo-legal moves for this piece
                    pseudo_moves = self._generate_pseudo_legal_moves_for_piece((file, rank), square)
                    
                    # Test if any move is legal
                    for move in pseudo_moves:
                        board_copy = self.copy()
                        # Temporarily set the current player to the color we're testing
                        original_player = board_copy.current_player
                        board_copy.current_player = color
                        
                        if board_copy.make_move(move):
                            if not board_copy.is_check(color):
                                has_legal_move = True
                                break
                        
                        # Restore original player (though we're using a copy)
                        board_copy.current_player = original_player
                    
                    if has_legal_move:
                        break
            
            if has_legal_move:
                break
        
        return not has_legal_move
    
    def _get_fen(self) -> str:
        """Generate FEN string from current board state"""
        fen_parts = []
        
        # 1. Piece placement
        for rank in range(8):
            rank_str = ""
            empty_count = 0
            
            for file in range(8):
                square = self.board[rank][file]
                if square.empty:
                    empty_count += 1
                else:
                    if empty_count > 0:
                        rank_str += str(empty_count)
                        empty_count = 0
                    rank_str += str(square)
            
            if empty_count > 0:
                rank_str += str(empty_count)
            
            fen_parts.append(rank_str)
        
        board_fen = "/".join(fen_parts)
        
        # 2. Active color
        active_color = "w" if self.current_player == Color.WHITE else "b"
        
        # 3. Castling availability
        castling = ""
        if self.castling_rights["K"]:
            castling += "K"
        if self.castling_rights["Q"]:
            castling += "Q"
        if self.castling_rights["k"]:
            castling += "k"
        if self.castling_rights["q"]:
            castling += "q"
        if not castling:
            castling = "-"
        
        # 4. En passant target square
        en_passant = "-"
        if self.en_passant_target:
            file, rank = self.en_passant_target
            en_passant = f"{chr(ord('a') + file)}{8 - rank}"
        
        # 5. Halfmove clock
        halfmove = str(self.halfmove_clock)
        
        # 6. Fullmove number
        fullmove = str(self.fullmove_number)
        
        return f"{board_fen} {active_color} {castling} {en_passant} {halfmove} {fullmove}"
    
    def __str__(self):
        """String representation of the board"""
        result = []
        for rank in range(8):
            row = []
            for file in range(8):
                row.append(str(self.board[rank][file]))
            result.append(" ".join(row))
        return "\n".join(result)
    
    def _can_piece_attack(self, piece_type: PieceType, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Check if a piece can attack a target square"""
        from_file, from_rank = from_pos
        to_file, to_rank = to_pos
        
        if piece_type == PieceType.PAWN:
            # Pawn attacks diagonally
            piece = self.board[from_rank][from_file]
            if piece.color == Color.WHITE:
                return (from_rank - 1 == to_rank and abs(from_file - to_file) == 1)
            else:
                return (from_rank + 1 == to_rank and abs(from_file - to_file) == 1)
        
        elif piece_type == PieceType.KNIGHT:
            df, dr = abs(from_file - to_file), abs(from_rank - to_rank)
            return (df == 2 and dr == 1) or (df == 1 and dr == 2)
        
        elif piece_type == PieceType.BISHOP:
            return self._is_diagonal_clear(from_pos, to_pos)
        
        elif piece_type == PieceType.ROOK:
            return self._is_straight_clear(from_pos, to_pos)
        
        elif piece_type == PieceType.QUEEN:
            return self._is_diagonal_clear(from_pos, to_pos) or self._is_straight_clear(from_pos, to_pos)
        
        elif piece_type == PieceType.KING:
            df, dr = abs(from_file - to_file), abs(from_rank - to_rank)
            return df <= 1 and dr <= 1 and (df != 0 or dr != 0)
        
        return False
    
    def _is_diagonal_clear(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Check if diagonal path is clear"""
        from_file, from_rank = from_pos
        to_file, to_rank = to_pos
        
        df = abs(to_file - from_file)
        dr = abs(to_rank - from_rank)
        
        if df != dr:
            return False  # Not diagonal
        
        file_step = 1 if to_file > from_file else -1
        rank_step = 1 if to_rank > from_rank else -1
        
        current_file = from_file + file_step
        current_rank = from_rank + rank_step
        
        while current_file != to_file:
            if not self.board[current_rank][current_file].empty:
                return False
            current_file += file_step
            current_rank += rank_step
        
        return True
    
    def _is_straight_clear(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Check if straight path is clear"""
        from_file, from_rank = from_pos
        to_file, to_rank = to_pos
        
        if from_file != to_file and from_rank != to_rank:
            return False  # Not straight
        
        if from_file == to_file:
            # Vertical movement
            start_rank = min(from_rank, to_rank) + 1
            end_rank = max(from_rank, to_rank)
            for rank in range(start_rank, end_rank):
                if not self.board[rank][from_file].empty:
                    return False
        else:
            # Horizontal movement
            start_file = min(from_file, to_file) + 1
            end_file = max(from_file, to_file)
            for file in range(start_file, end_file):
                if not self.board[from_rank][file].empty:
                    return False
        
        return True
    
    def _update_castling_rights(self, move: Move):
        """Update castling rights after a move"""
        from_file, from_rank = move.from_square
        to_file, to_rank = move.to_square
        
        # King moves
        if move.piece_type == PieceType.KING:
            if move.color == Color.WHITE:
                self.castling_rights["K"] = False
                self.castling_rights["Q"] = False
            else:
                self.castling_rights["k"] = False
                self.castling_rights["q"] = False
        
        # Rook moves
        elif move.piece_type == PieceType.ROOK:
            if move.color == Color.WHITE:
                if from_file == 0 and from_rank == 7:  # Queenside rook
                    self.castling_rights["Q"] = False
                elif from_file == 7 and from_rank == 7:  # Kingside rook
                    self.castling_rights["K"] = False
            else:
                if from_file == 0 and from_rank == 0:  # Queenside rook
                    self.castling_rights["q"] = False
                elif from_file == 7 and from_rank == 0:  # Kingside rook
                    self.castling_rights["k"] = False
        
        # Rook captured
        if move.is_capture:
            if to_file == 0 and to_rank == 0:  # Black queenside rook
                self.castling_rights["q"] = False
            elif to_file == 7 and to_rank == 0:  # Black kingside rook
                self.castling_rights["k"] = False
            elif to_file == 0 and to_rank == 7:  # White queenside rook
                self.castling_rights["Q"] = False
            elif to_file == 7 and to_rank == 7:  # White kingside rook
                self.castling_rights["K"] = False
    
    def _update_en_passant_target(self, move: Move):
        """Update en passant target after a move"""
        self.en_passant_target = None
        
        # Check for pawn double move
        if move.piece_type == PieceType.PAWN:
            from_file, from_rank = move.from_square
            to_file, to_rank = move.to_square
            
            if abs(to_rank - from_rank) == 2:
                # Pawn moved two squares, set en passant target
                if move.color == Color.WHITE:
                    self.en_passant_target = (to_file, to_rank + 1)
                else:
                    self.en_passant_target = (to_file, to_rank - 1)
    
    def _generate_pseudo_legal_moves_for_piece(self, square: Tuple[int, int], piece: Square) -> List[Move]:
        """Generate pseudo-legal moves for a specific piece (without checking for check)"""
        moves = []
        file, rank = square
        piece_type = piece.piece_type
        color = piece.color
        
        if piece_type == PieceType.PAWN:
            moves.extend(self._generate_pawn_pseudo_moves(square, color))
        elif piece_type == PieceType.KNIGHT:
            moves.extend(self._generate_knight_pseudo_moves(square, color))
        elif piece_type == PieceType.BISHOP:
            moves.extend(self._generate_bishop_pseudo_moves(square, color))
        elif piece_type == PieceType.ROOK:
            moves.extend(self._generate_rook_pseudo_moves(square, color))
        elif piece_type == PieceType.QUEEN:
            moves.extend(self._generate_queen_pseudo_moves(square, color))
        elif piece_type == PieceType.KING:
            moves.extend(self._generate_king_pseudo_moves(square, color))
        
        return moves
    
    def _generate_pawn_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal pawn moves"""
        moves = []
        file, rank = square
        direction = -1 if color == Color.WHITE else 1
        start_rank = 6 if color == Color.WHITE else 1
        
        # Forward moves
        new_rank = rank + direction
        if 0 <= new_rank < 8:
            if self.get_piece((file, new_rank)).empty:
                moves.append(Move((file, rank), (file, new_rank), PieceType.PAWN, color))
                
                # Double move from starting position
                if rank == start_rank:
                    new_rank = rank + 2 * direction
                    if 0 <= new_rank < 8 and self.get_piece((file, new_rank)).empty:
                        moves.append(Move((file, rank), (file, new_rank), PieceType.PAWN, color))
            
            # Diagonal captures
            for file_offset in [-1, 1]:
                new_file = file + file_offset
                if 0 <= new_file < 8:
                    target_square = self.get_piece((new_file, new_rank))
                    if not target_square.empty and target_square.color != color:
                        moves.append(Move((file, rank), (new_file, new_rank), PieceType.PAWN, color, is_capture=True))
        
        return moves
    
    def _generate_knight_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal knight moves"""
        moves = []
        file, rank = square
        
        knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        
        for file_offset, rank_offset in knight_moves:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                target_square = self.get_piece((new_file, new_rank))
                if target_square.empty or target_square.color != color:
                    is_capture = not target_square.empty
                    moves.append(Move((file, rank), (new_file, new_rank), PieceType.KNIGHT, color, is_capture=is_capture))
        
        return moves
    
    def _generate_bishop_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal bishop moves"""
        return self._generate_sliding_moves(square, color, PieceType.BISHOP, [(1, 1), (1, -1), (-1, 1), (-1, -1)])
    
    def _generate_rook_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal rook moves"""
        return self._generate_sliding_moves(square, color, PieceType.ROOK, [(0, 1), (0, -1), (1, 0), (-1, 0)])
    
    def _generate_queen_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal queen moves"""
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        return self._generate_sliding_moves(square, color, PieceType.QUEEN, directions)
    
    def _generate_king_pseudo_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pseudo-legal king moves"""
        moves = []
        file, rank = square
        
        king_moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
        for file_offset, rank_offset in king_moves:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                target_square = self.get_piece((new_file, new_rank))
                if target_square.empty or target_square.color != color:
                    is_capture = not target_square.empty
                    moves.append(Move((file, rank), (new_file, new_rank), PieceType.KING, color, is_capture=is_capture))
        
        return moves
    
    def _generate_sliding_moves(self, square: Tuple[int, int], color: Color, piece_type: PieceType, directions: List[Tuple[int, int]]) -> List[Move]:
        """Generate sliding piece moves (rook, bishop, queen)"""
        moves = []
        file, rank = square
        
        for file_offset, rank_offset in directions:
            for distance in range(1, 8):
                new_file = file + file_offset * distance
                new_rank = rank + rank_offset * distance
                
                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                    break
                
                target_square = self.get_piece((new_file, new_rank))
                if target_square.empty:
                    moves.append(Move((file, rank), (new_file, new_rank), piece_type, color))
                elif target_square.color != color:
                    moves.append(Move((file, rank), (new_file, new_rank), piece_type, color, is_capture=True))
                    break
                else:
                    break
        
        return moves
    
    def copy(self):
        """Create a deep copy of the board"""
        return copy.deepcopy(self)