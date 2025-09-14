"""
Minimax Search Algorithm with Alpha-Beta Pruning

This module implements:
- Minimax algorithm with alpha-beta pruning
- Iterative deepening
- Move ordering for better performance
- Time management
"""

import time
from typing import List, Tuple, Optional, Dict, Any
from ..board.board import ChessBoard, Move, Color
from ..board.move_generator import MoveGenerator
from ..eval.evaluation import EvaluationEngine

class MinimaxEngine:
    """Minimax chess engine with alpha-beta pruning"""
    
    def __init__(self, max_depth: int = 4, time_limit: float = 5.0):
        """
        Initialize minimax engine
        
        Args:
            max_depth: Maximum search depth
            time_limit: Time limit in seconds
        """
        self.max_depth = max_depth
        self.time_limit = time_limit
        self.nodes_searched = 0
        from .transposition import LRUTranspositionTable
        self.transposition_table = LRUTranspositionTable(max_size=1000000)
        self.killer_moves = {}  # Move ordering
        self.history_table = {}  # History heuristic
        self.evaluation_engine = EvaluationEngine()
        self.move_generator = None
        
        # Search statistics
        self.search_stats = {
            'nodes_searched': 0,
            'cutoffs': 0,
            'transposition_hits': 0,
            'quiescence_nodes': 0
        }
    
    def search(self, board: ChessBoard, depth: Optional[int] = None) -> Tuple[Move, float]:
        """
        Search for best move using minimax with alpha-beta pruning
        
        Args:
            board: Current chess position
            depth: Search depth (uses max_depth if None)
            
        Returns:
            Tuple of (best_move, evaluation_score)
        """
        if depth is None:
            depth = self.max_depth
        
        self.move_generator = MoveGenerator(board)
        self.nodes_searched = 0
        self.search_stats = {key: 0 for key in self.search_stats}
        
        start_time = time.time()
        best_move = None
        best_score = float('-inf')
        
        # Iterative deepening
        for current_depth in range(1, depth + 1):
            if time.time() - start_time > self.time_limit:
                break
                
            try:
                move, score = self._minimax(
                    board, current_depth, float('-inf'), float('inf'), 
                    board.current_player, start_time
                )
                
                if move is not None:
                    best_move = move
                    best_score = score
                    
            except TimeoutError:
                break
        
        search_time = time.time() - start_time
        print(f"Search completed: {self.nodes_searched} nodes in {search_time:.2f}s")
        print(f"Nodes/sec: {self.nodes_searched / search_time:.0f}")
        
        return best_move, best_score
    
    def _minimax(self, board: ChessBoard, depth: int, alpha: float, beta: float, 
                color: Color, start_time: float) -> Tuple[Optional[Move], float]:
        """
        Minimax algorithm with alpha-beta pruning
        
        Args:
            board: Current position
            depth: Remaining search depth
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            color: Color to move
            start_time: Search start time
            
        Returns:
            Tuple of (best_move, best_score)
        """
        # Check time limit
        if time.time() - start_time > self.time_limit:
            raise TimeoutError("Time limit exceeded")
        
        self.nodes_searched += 1
        
        # Get board hash for transposition table
        board_hash = self._get_board_hash(board)
        
        # Check for terminal positions
        if depth == 0:
            score = self._quiescence_search(board, alpha, beta, color, start_time)
            # Store in transposition table even for depth 0
            from .transposition import TranspositionEntry, NodeType
            entry = TranspositionEntry(0, score, NodeType.EXACT, None)
            self.transposition_table.put(board_hash, entry)
            return None, score
        
        # Check transposition table
        tt_entry = self.transposition_table.get(board_hash)
        if tt_entry and tt_entry.depth >= depth:
            self.search_stats['transposition_hits'] += 1
            return tt_entry.best_move, tt_entry.score
        
        # Generate legal moves
        moves = self.move_generator.generate_legal_moves(color)
        if not moves:
            # No legal moves - checkmate or stalemate
            if board.is_check(color):
                return None, float('-inf') if color == board.current_player else float('inf')
            else:
                return None, 0.0  # Stalemate
        
        # Order moves for better pruning
        moves = self._order_moves(moves, board)
        
        best_move = None
        best_score = float('-inf') if color == board.current_player else float('inf')
        
        for move in moves:
            # Make move
            if not board.make_move(move):
                continue
            
            # Recursive search
            _, score = self._minimax(
                board, depth - 1, alpha, beta, 
                Color.BLACK if color == Color.WHITE else Color.WHITE, start_time
            )
            
            # Undo move
            board.undo_move()
            
            # Update best move and score
            if color == board.current_player:
                if score > best_score:
                    best_score = score
                    best_move = move
                    alpha = max(alpha, score)
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
                    beta = min(beta, score)
            
            # Alpha-beta pruning
            if beta <= alpha:
                self.search_stats['cutoffs'] += 1
                break
        
        # Store in transposition table
        from .transposition import TranspositionEntry, NodeType
        node_type = NodeType.EXACT  # Simplified - should determine based on alpha/beta bounds
        entry = TranspositionEntry(depth, best_score, node_type, best_move)
        self.transposition_table.put(board_hash, entry)
        
        return best_move, best_score
    
    def _quiescence_search(self, board: ChessBoard, alpha: float, beta: float, 
                          color: Color, start_time: float) -> float:
        """
        Quiescence search to handle tactical positions
        
        Args:
            board: Current position
            alpha: Alpha value
            beta: Beta value
            color: Color to move
            start_time: Search start time
            
        Returns:
            Evaluation score
        """
        self.search_stats['quiescence_nodes'] += 1
        
        # Check time limit
        if time.time() - start_time > self.time_limit:
            raise TimeoutError("Time limit exceeded")
        
        # Get static evaluation
        static_eval = self.evaluation_engine.evaluate(board, color)
        
        # Stand pat if static evaluation is good enough
        if static_eval >= beta:
            return beta
        if static_eval > alpha:
            alpha = static_eval
        
        # Generate only capture moves
        moves = self._generate_capture_moves(board, color)
        
        for move in moves:
            if not board.make_move(move):
                continue
            
            score = -self._quiescence_search(board, -beta, -alpha, 
                                           Color.BLACK if color == Color.WHITE else Color.WHITE, start_time)
            
            board.undo_move()
            
            if score >= beta:
                return beta
            if score > alpha:
                alpha = score
        
        return alpha
    
    def _generate_capture_moves(self, board: ChessBoard, color: Color) -> List[Move]:
        """Generate only capture moves for quiescence search"""
        moves = self.move_generator.generate_legal_moves(color)
        return [move for move in moves if move.is_capture]
    
    def _order_moves(self, moves: List[Move], board: ChessBoard) -> List[Move]:
        """
        Order moves for better alpha-beta pruning
        
        Args:
            moves: List of moves to order
            board: Current board position
            
        Returns:
            Ordered list of moves
        """
        def move_priority(move):
            priority = 0
            
            # MVV-LVA (Most Valuable Victim - Least Valuable Attacker)
            if move.is_capture:
                victim_value = self._get_piece_value(move.piece_type)
                attacker_value = self._get_piece_value(move.piece_type)
                priority += 1000 + victim_value - attacker_value
            
            # Killer moves
            if move in self.killer_moves.get(board.current_player, []):
                priority += 100
            
            # History heuristic
            history_key = (move.from_square, move.to_square)
            priority += self.history_table.get(history_key, 0)
            
            # Promotion
            if move.promotion:
                priority += 500
            
            return priority
        
        return sorted(moves, key=move_priority, reverse=True)
    
    def _get_piece_value(self, piece_type) -> int:
        """Get piece value for MVV-LVA"""
        values = {
            'PAWN': 100,
            'KNIGHT': 320,
            'BISHOP': 330,
            'ROOK': 500,
            'QUEEN': 900,
            'KING': 20000
        }
        return values.get(piece_type.name, 0)
    
    def _get_board_hash(self, board: ChessBoard) -> int:
        """Get board hash for transposition table"""
        from .zobrist import zobrist
        return zobrist.hash_position(board)
    
    def update_killer_moves(self, move: Move, color: Color):
        """Update killer moves for move ordering"""
        if color not in self.killer_moves:
            self.killer_moves[color] = []
        
        if move not in self.killer_moves[color]:
            self.killer_moves[color].insert(0, move)
            if len(self.killer_moves[color]) > 2:
                self.killer_moves[color].pop()
    
    def update_history(self, move: Move, depth: int):
        """Update history table for move ordering"""
        history_key = (move.from_square, move.to_square)
        self.history_table[history_key] = self.history_table.get(history_key, 0) + depth * depth
    
    def clear_tables(self):
        """Clear transposition and history tables"""
        self.transposition_table.clear()
        self.killer_moves.clear()
        self.history_table.clear()
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        return {
            'nodes_searched': self.nodes_searched,
            'cutoffs': self.search_stats['cutoffs'],
            'transposition_hits': self.search_stats['transposition_hits'],
            'quiescence_nodes': self.search_stats['quiescence_nodes'],
            'transposition_size': self.transposition_table.get_stats()['size']
        }