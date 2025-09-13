"""
Evaluation Engine - Modular chess position evaluation

This module implements:
- Material evaluation
- Piece-square tables
- King safety evaluation
- Pawn structure evaluation
- Mobility evaluation
- Tunable evaluation weights
"""

import json
import os
from typing import Dict, List, Tuple, Any
from ..board.board import ChessBoard, Color, PieceType

class EvaluationEngine:
    """Modular chess position evaluation engine"""
    
    def __init__(self, weights_file: str = "weights.json"):
        """
        Initialize evaluation engine
        
        Args:
            weights_file: Path to weights configuration file
        """
        self.weights_file = weights_file
        self.weights = self._load_weights()
        
        # Piece-square tables for positional evaluation
        self.piece_square_tables = self._init_piece_square_tables()
        
        # Material values
        self.material_values = {
            PieceType.PAWN: 100,
            PieceType.KNIGHT: 320,
            PieceType.BISHOP: 330,
            PieceType.ROOK: 500,
            PieceType.QUEEN: 900,
            PieceType.KING: 20000
        }
    
    def _load_weights(self) -> Dict[str, float]:
        """Load evaluation weights from file"""
        default_weights = {
            "material": 1.0,
            "position": 1.0,
            "king_safety": 1.0,
            "pawn_structure": 1.0,
            "mobility": 1.0,
            "center_control": 1.0,
            "development": 1.0,
            "tempo": 1.0
        }
        
        if os.path.exists(self.weights_file):
            try:
                with open(self.weights_file, 'r') as f:
                    weights = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_weights.items():
                    if key not in weights:
                        weights[key] = value
                return weights
            except (json.JSONDecodeError, IOError):
                print(f"Warning: Could not load weights from {self.weights_file}, using defaults")
                return default_weights
        else:
            # Create default weights file
            self._save_weights(default_weights)
            return default_weights
    
    def _save_weights(self, weights: Dict[str, float]):
        """Save weights to file"""
        try:
            with open(self.weights_file, 'w') as f:
                json.dump(weights, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save weights to {self.weights_file}: {e}")
    
    def _init_piece_square_tables(self) -> Dict[PieceType, List[List[int]]]:
        """Initialize piece-square tables for positional evaluation"""
        tables = {}
        
        # Pawn table (encourages central pawns and passed pawns)
        tables[PieceType.PAWN] = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5,  5, 10, 25, 25, 10,  5,  5],
            [0,  0,  0, 20, 20,  0,  0,  0],
            [5, -5,-10,  0,  0,-10, -5,  5],
            [5, 10, 10,-20,-20, 10, 10,  5],
            [0,  0,  0,  0,  0,  0,  0,  0]
        ]
        
        # Knight table (encourages central knights)
        tables[PieceType.KNIGHT] = [
            [-50,-40,-30,-30,-30,-30,-40,-50],
            [-40,-20,  0,  0,  0,  0,-20,-40],
            [-30,  0, 10, 15, 15, 10,  0,-30],
            [-30,  5, 15, 20, 20, 15,  5,-30],
            [-30,  0, 15, 20, 20, 15,  0,-30],
            [-30,  5, 10, 15, 15, 10,  5,-30],
            [-40,-20,  0,  5,  5,  0,-20,-40],
            [-50,-40,-30,-30,-30,-30,-40,-50]
        ]
        
        # Bishop table (encourages central bishops)
        tables[PieceType.BISHOP] = [
            [-20,-10,-10,-10,-10,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5, 10, 10,  5,  0,-10],
            [-10,  5,  5, 10, 10,  5,  5,-10],
            [-10,  0, 10, 10, 10, 10,  0,-10],
            [-10, 10, 10, 10, 10, 10, 10,-10],
            [-10,  5,  0,  0,  0,  0,  5,-10],
            [-20,-10,-10,-10,-10,-10,-10,-20]
        ]
        
        # Rook table (encourages rooks on open files)
        tables[PieceType.ROOK] = [
            [0,  0,  0,  0,  0,  0,  0,  0],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0,  0,  0,  5,  5,  0,  0,  0]
        ]
        
        # Queen table (encourages central queen)
        tables[PieceType.QUEEN] = [
            [-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-5,  0,  5,  5,  5,  5,  0, -5],
            [0,  0,  5,  5,  5,  5,  0, -5],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]
        ]
        
        # King table (encourages king safety in endgame)
        tables[PieceType.KING] = [
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-30,-40,-40,-50,-50,-40,-40,-30],
            [-20,-30,-30,-40,-40,-30,-30,-20],
            [-10,-20,-20,-20,-20,-20,-20,-10],
            [20, 20,  0,  0,  0,  0, 20, 20],
            [20, 30, 10,  0,  0, 10, 30, 20]
        ]
        
        return tables
    
    def evaluate(self, board: ChessBoard, color: Color) -> float:
        """
        Evaluate chess position
        
        Args:
            board: Chess board position
            color: Color to evaluate for
            
        Returns:
            Evaluation score (positive = good for color)
        """
        if board.is_checkmate(color):
            return float('-inf')
        if board.is_checkmate(Color.BLACK if color == Color.WHITE else Color.WHITE):
            return float('inf')
        if board.is_stalemate(color):
            return 0.0
        
        # Calculate different evaluation components
        material_score = self._evaluate_material(board, color)
        position_score = self._evaluate_position(board, color)
        king_safety_score = self._evaluate_king_safety(board, color)
        pawn_structure_score = self._evaluate_pawn_structure(board, color)
        mobility_score = self._evaluate_mobility(board, color)
        center_control_score = self._evaluate_center_control(board, color)
        development_score = self._evaluate_development(board, color)
        tempo_score = self._evaluate_tempo(board, color)
        
        # Combine scores with weights
        total_score = (
            material_score * self.weights["material"] +
            position_score * self.weights["position"] +
            king_safety_score * self.weights["king_safety"] +
            pawn_structure_score * self.weights["pawn_structure"] +
            mobility_score * self.weights["mobility"] +
            center_control_score * self.weights["center_control"] +
            development_score * self.weights["development"] +
            tempo_score * self.weights["tempo"]
        )
        
        return total_score
    
    def _evaluate_material(self, board: ChessBoard, color: Color) -> float:
        """Evaluate material balance"""
        material_score = 0.0
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    piece_value = self.material_values[square.piece_type]
                    if square.color == color:
                        material_score += piece_value
                    else:
                        material_score -= piece_value
        
        return material_score
    
    def _evaluate_position(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece-square table values"""
        position_score = 0.0
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    piece_table = self.piece_square_tables[square.piece_type]
                    
                    # Adjust table for color (flip for black)
                    if square.color == Color.WHITE:
                        table_value = piece_table[rank][file]
                    else:
                        table_value = piece_table[7 - rank][file]
                    
                    if square.color == color:
                        position_score += table_value
                    else:
                        position_score -= table_value
        
        return position_score
    
    def _evaluate_king_safety(self, board: ChessBoard, color: Color) -> float:
        """Evaluate king safety"""
        # TODO: Implement king safety evaluation
        # - King shelter
        # - Pawn shield
        # - Attacking pieces near king
        # - King mobility
        
        return 0.0
    
    def _evaluate_pawn_structure(self, board: ChessBoard, color: Color) -> float:
        """Evaluate pawn structure"""
        # TODO: Implement pawn structure evaluation
        # - Passed pawns
        # - Isolated pawns
        # - Doubled pawns
        # - Pawn chains
        # - Pawn storms
        
        return 0.0
    
    def _evaluate_mobility(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece mobility"""
        # TODO: Implement mobility evaluation
        # - Number of legal moves
        # - Control of important squares
        # - Piece activity
        
        return 0.0
    
    def _evaluate_center_control(self, board: ChessBoard, color: Color) -> float:
        """Evaluate center control"""
        # TODO: Implement center control evaluation
        # - Control of central squares (d4, d5, e4, e5)
        # - Piece pressure on center
        
        return 0.0
    
    def _evaluate_development(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece development"""
        # TODO: Implement development evaluation
        # - Number of pieces developed
        # - Castling status
        # - Piece coordination
        
        return 0.0
    
    def _evaluate_tempo(self, board: ChessBoard, color: Color) -> float:
        """Evaluate tempo (initiative)"""
        # TODO: Implement tempo evaluation
        # - Move order advantage
        # - Initiative in position
        
        return 0.0
    
    def update_weights(self, new_weights: Dict[str, float]):
        """Update evaluation weights"""
        self.weights.update(new_weights)
        self._save_weights(self.weights)
    
    def get_weights(self) -> Dict[str, float]:
        """Get current evaluation weights"""
        return self.weights.copy()
    
    def reset_weights(self):
        """Reset weights to default values"""
        default_weights = {
            "material": 1.0,
            "position": 1.0,
            "king_safety": 1.0,
            "pawn_structure": 1.0,
            "mobility": 1.0,
            "center_control": 1.0,
            "development": 1.0,
            "tempo": 1.0
        }
        self.weights = default_weights
        self._save_weights(self.weights)
    
    def get_evaluation_breakdown(self, board: ChessBoard, color: Color) -> Dict[str, float]:
        """Get detailed evaluation breakdown"""
        return {
            "material": self._evaluate_material(board, color),
            "position": self._evaluate_position(board, color),
            "king_safety": self._evaluate_king_safety(board, color),
            "pawn_structure": self._evaluate_pawn_structure(board, color),
            "mobility": self._evaluate_mobility(board, color),
            "center_control": self._evaluate_center_control(board, color),
            "development": self._evaluate_development(board, color),
            "tempo": self._evaluate_tempo(board, color)
        }