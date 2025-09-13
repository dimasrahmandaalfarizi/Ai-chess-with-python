"""
Quiescence Search - Handle tactical positions

This module implements:
- Quiescence search for tactical positions
- Capture-only move generation
- Static exchange evaluation (SEE)
- Tactical move ordering
"""

from typing import List, Tuple, Optional
from ..board.board import ChessBoard, Move, Color
from ..board.move_generator import MoveGenerator

class QuiescenceSearch:
    """Quiescence search for handling tactical positions"""
    
    def __init__(self, max_depth: int = 6):
        """
        Initialize quiescence search
        
        Args:
            max_depth: Maximum quiescence search depth
        """
        self.max_depth = max_depth
        self.nodes_searched = 0
        self.move_generator = None
    
    def search(self, board: ChessBoard, alpha: float, beta: float, 
              color: Color, depth: int = 0) -> float:
        """
        Perform quiescence search
        
        Args:
            board: Current position
            alpha: Alpha value
            beta: Beta value
            color: Color to move
            depth: Current depth
            
        Returns:
            Evaluation score
        """
        if depth >= self.max_depth:
            return self._static_evaluation(board, color)
        
        self.nodes_searched += 1
        
        # Get static evaluation
        static_eval = self._static_evaluation(board, color)
        
        # Stand pat if static evaluation is good enough
        if static_eval >= beta:
            return beta
        if static_eval > alpha:
            alpha = static_eval
        
        # Generate capture moves
        if not self.move_generator:
            self.move_generator = MoveGenerator(board)
        
        capture_moves = self._generate_capture_moves(board, color)
        
        # Order moves by SEE (Static Exchange Evaluation)
        capture_moves = self._order_captures_by_see(capture_moves, board)
        
        for move in capture_moves:
            # Make move
            if not board.make_move(move):
                continue
            
            # Recursive quiescence search
            score = -self.search(board, -beta, -alpha, 
                               Color.BLACK if color == Color.WHITE else Color.WHITE, 
                               depth + 1)
            
            # Undo move
            board.undo_move()
            
            # Update alpha
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha
    
    def _generate_capture_moves(self, board: ChessBoard, color: Color) -> List[Move]:
        """Generate only capture moves"""
        moves = self.move_generator.generate_legal_moves(color)
        return [move for move in moves if move.is_capture]
    
    def _order_captures_by_see(self, moves: List[Move], board: ChessBoard) -> List[Move]:
        """
        Order capture moves by Static Exchange Evaluation
        
        Args:
            moves: List of capture moves
            board: Current board position
            
        Returns:
            Moves ordered by SEE value (highest first)
        """
        def see_value(move):
            return self._static_exchange_evaluation(move, board)
        
        return sorted(moves, key=see_value, reverse=True)
    
    def _static_exchange_evaluation(self, move: Move, board: ChessBoard) -> int:
        """
        Calculate Static Exchange Evaluation for a move
        
        Args:
            move: Move to evaluate
            board: Current board position
            
        Returns:
            SEE value (positive = good for attacker)
        """
        # TODO: Implement proper SEE calculation
        # For now, use simple piece values
        
        attacker_value = self._get_piece_value(move.piece_type)
        victim_value = self._get_piece_value(move.piece_type)  # This should be the captured piece
        
        return victim_value - attacker_value
    
    def _get_piece_value(self, piece_type) -> int:
        """Get piece value for SEE calculation"""
        values = {
            'PAWN': 100,
            'KNIGHT': 320,
            'BISHOP': 330,
            'ROOK': 500,
            'QUEEN': 900,
            'KING': 20000
        }
        return values.get(piece_type.name, 0)
    
    def _static_evaluation(self, board: ChessBoard, color: Color) -> float:
        """
        Static evaluation of position (without search)
        
        Args:
            board: Current position
            color: Color to evaluate for
            
        Returns:
            Evaluation score
        """
        # TODO: Implement static evaluation
        # This should be a simple material and positional evaluation
        # without considering tactics
        
        material_score = 0.0
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    piece_value = self._get_piece_value(square.piece_type)
                    if square.color == color:
                        material_score += piece_value
                    else:
                        material_score -= piece_value
        
        return material_score
    
    def get_nodes_searched(self) -> int:
        """Get number of nodes searched in quiescence"""
        return self.nodes_searched
    
    def reset_stats(self):
        """Reset search statistics"""
        self.nodes_searched = 0