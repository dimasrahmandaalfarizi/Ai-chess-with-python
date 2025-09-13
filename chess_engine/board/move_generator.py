"""
Move Generator - Generate legal chess moves

This module handles:
- Legal move generation for all piece types
- Move validation
- Special moves (castling, en passant, promotion)
- Move ordering for better search performance
"""

from typing import List, Tuple, Optional
from .board import ChessBoard, Move, PieceType, Color, Square

class MoveGenerator:
    """Generates legal moves for chess positions"""
    
    def __init__(self, board: ChessBoard):
        self.board = board
    
    def generate_legal_moves(self, color: Color) -> List[Move]:
        """
        Generate all legal moves for given color
        
        Args:
            color: Color to generate moves for
            
        Returns:
            List of legal moves
        """
        moves = []
        
        # Generate moves for each piece
        for rank in range(8):
            for file in range(8):
                square = self.board.get_piece((file, rank))
                if square and not square.empty and square.color == color:
                    piece_moves = self._generate_piece_moves((file, rank), square)
                    moves.extend(piece_moves)
        
        # Filter out moves that would put own king in check
        legal_moves = []
        for move in moves:
            if self._is_legal_move(move):
                legal_moves.append(move)
        
        return legal_moves
    
    def _generate_piece_moves(self, square: Tuple[int, int], piece: Square) -> List[Move]:
        """Generate moves for a specific piece"""
        piece_type = piece.piece_type
        color = piece.color
        
        if piece_type == PieceType.PAWN:
            return self._generate_pawn_moves(square, color)
        elif piece_type == PieceType.KNIGHT:
            return self._generate_knight_moves(square, color)
        elif piece_type == PieceType.BISHOP:
            return self._generate_bishop_moves(square, color)
        elif piece_type == PieceType.ROOK:
            return self._generate_rook_moves(square, color)
        elif piece_type == PieceType.QUEEN:
            return self._generate_queen_moves(square, color)
        elif piece_type == PieceType.KING:
            return self._generate_king_moves(square, color)
        
        return []
    
    def _generate_pawn_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate pawn moves including promotion, en passant"""
        moves = []
        file, rank = square
        direction = -1 if color == Color.WHITE else 1
        start_rank = 6 if color == Color.WHITE else 1
        
        # Forward moves
        new_rank = rank + direction
        if 0 <= new_rank < 8:
            # Single square forward
            if self.board.get_piece((file, new_rank)).empty:
                moves.append(self._create_move(square, (file, new_rank), PieceType.PAWN, color))
                
                # Double square forward from starting position
                if rank == start_rank:
                    new_rank = rank + 2 * direction
                    if 0 <= new_rank < 8 and self.board.get_piece((file, new_rank)).empty:
                        moves.append(self._create_move(square, (file, new_rank), PieceType.PAWN, color))
            
            # Diagonal captures
            for file_offset in [-1, 1]:
                new_file = file + file_offset
                if 0 <= new_file < 8:
                    target_square = self.board.get_piece((new_file, new_rank))
                    if not target_square.empty and target_square.color != color:
                        moves.append(self._create_move(square, (new_file, new_rank), PieceType.PAWN, color, is_capture=True))
        
        # En passant
        if self.board.en_passant_target:
            ep_file, ep_rank = self.board.en_passant_target
            if abs(file - ep_file) == 1 and rank == ep_rank - direction:
                moves.append(self._create_move(square, (ep_file, ep_rank), PieceType.PAWN, color, is_en_passant=True))
        
        # Promotion
        promotion_rank = 0 if color == Color.WHITE else 7
        if rank + direction == promotion_rank:
            # Add promotion moves for each piece type
            for piece_type in [PieceType.QUEEN, PieceType.ROOK, PieceType.BISHOP, PieceType.KNIGHT]:
                moves.append(self._create_move(square, (file, promotion_rank), PieceType.PAWN, color, promotion=piece_type))
        
        return moves
    
    def _generate_knight_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate knight moves"""
        moves = []
        file, rank = square
        
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for file_offset, rank_offset in knight_moves:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                target_square = self.board.get_piece((new_file, new_rank))
                if target_square.empty or target_square.color != color:
                    is_capture = not target_square.empty
                    moves.append(self._create_move(square, (new_file, new_rank), PieceType.KNIGHT, color, is_capture=is_capture))
        
        return moves
    
    def _generate_bishop_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate bishop moves"""
        return self._generate_diagonal_moves(square, color, PieceType.BISHOP)
    
    def _generate_rook_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate rook moves"""
        moves = []
        file, rank = square
        
        # Horizontal and vertical directions
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for file_offset, rank_offset in directions:
            for distance in range(1, 8):
                new_file = file + file_offset * distance
                new_rank = rank + rank_offset * distance
                
                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                    break
                
                target_square = self.board.get_piece((new_file, new_rank))
                if target_square.empty:
                    moves.append(self._create_move(square, (new_file, new_rank), PieceType.ROOK, color))
                elif target_square.color != color:
                    moves.append(self._create_move(square, (new_file, new_rank), PieceType.ROOK, color, is_capture=True))
                    break
                else:
                    break
        
        return moves
    
    def _generate_queen_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate queen moves (combination of rook and bishop)"""
        moves = []
        moves.extend(self._generate_rook_moves(square, color))
        moves.extend(self._generate_diagonal_moves(square, color, PieceType.QUEEN))
        return moves
    
    def _generate_king_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate king moves including castling"""
        moves = []
        file, rank = square
        
        # Regular king moves
        king_moves = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        for file_offset, rank_offset in king_moves:
            new_file = file + file_offset
            new_rank = rank + rank_offset
            
            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                target_square = self.board.get_piece((new_file, new_rank))
                if target_square.empty or target_square.color != color:
                    is_capture = not target_square.empty
                    moves.append(self._create_move(square, (new_file, new_rank), PieceType.KING, color, is_capture=is_capture))
        
        # Castling
        moves.extend(self._generate_castling_moves(square, color))
        
        return moves
    
    def _generate_diagonal_moves(self, square: Tuple[int, int], color: Color, piece_type: PieceType) -> List[Move]:
        """Generate diagonal moves for bishop and queen"""
        moves = []
        file, rank = square
        
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for file_offset, rank_offset in directions:
            for distance in range(1, 8):
                new_file = file + file_offset * distance
                new_rank = rank + rank_offset * distance
                
                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                    break
                
                target_square = self.board.get_piece((new_file, new_rank))
                if target_square.empty:
                    moves.append(self._create_move(square, (new_file, new_rank), piece_type, color))
                elif target_square.color != color:
                    moves.append(self._create_move(square, (new_file, new_rank), piece_type, color, is_capture=True))
                    break
                else:
                    break
        
        return moves
    
    def _generate_castling_moves(self, square: Tuple[int, int], color: Color) -> List[Move]:
        """Generate castling moves"""
        moves = []
        file, rank = square
        
        # TODO: Implement castling logic
        # - Check if king and rook haven't moved
        # - Check if squares between are empty
        # - Check if king is not in check and doesn't pass through check
        
        return moves
    
    def _create_move(self, from_square: Tuple[int, int], to_square: Tuple[int, int], 
                    piece_type: PieceType, color: Color, promotion: Optional[PieceType] = None,
                    is_capture: bool = False, is_en_passant: bool = False, is_castling: bool = False) -> Move:
        """Create a move object"""
        return Move(from_square, to_square, piece_type, color, promotion, is_castling, is_en_passant, is_capture)
    
    def _is_legal_move(self, move: Move) -> bool:
        """
        Check if a move is legal (doesn't put own king in check)
        
        Args:
            move: Move to check
            
        Returns:
            True if move is legal, False otherwise
        """
        # TODO: Implement move legality check
        # - Make the move temporarily
        # - Check if own king is in check
        # - Undo the move
        # - Return result
        
        return True
    
    def order_moves(self, moves: List[Move]) -> List[Move]:
        """
        Order moves for better search performance (MVV-LVA, killer moves, etc.)
        
        Args:
            moves: List of moves to order
            
        Returns:
            Ordered list of moves
        """
        # TODO: Implement move ordering
        # - MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
        # - Killer moves
        # - History heuristic
        # - Transposition table moves
        
        return moves