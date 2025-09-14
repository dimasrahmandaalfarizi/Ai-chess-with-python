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
        
        # Return score from perspective of the color being evaluated
        # Positive score = good for the color, negative = bad for the color
        return total_score
    
    def _evaluate_material(self, board: ChessBoard, color: Color) -> float:
        """Evaluate material balance from perspective of given color"""
        own_material = 0.0
        opponent_material = 0.0
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    piece_value = self.material_values[square.piece_type]
                    if square.color == color:
                        own_material += piece_value
                    else:
                        opponent_material += piece_value
        
        return own_material - opponent_material
    
    def _evaluate_position(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece-square table values from perspective of given color"""
        own_position_score = 0.0
        opponent_position_score = 0.0
        
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
                        own_position_score += table_value
                    else:
                        opponent_position_score += table_value
        
        return own_position_score - opponent_position_score
    
    def _evaluate_king_safety(self, board: ChessBoard, color: Color) -> float:
        """Evaluate king safety"""
        safety_score = 0.0
        
        # Find king position
        king_pos = None
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and square.piece_type == PieceType.KING and square.color == color:
                    king_pos = (file, rank)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return -1000.0  # King missing - critical error
        
        king_file, king_rank = king_pos
        
        # Evaluate pawn shield (pawns in front of king)
        pawn_shield_bonus = 0
        if color == Color.WHITE:
            # Check pawns in front of white king
            for file_offset in [-1, 0, 1]:
                shield_file = king_file + file_offset
                if 0 <= shield_file < 8:
                    for rank_check in [king_rank - 1, king_rank - 2]:
                        if 0 <= rank_check < 8:
                            square = board.get_piece((shield_file, rank_check))
                            if square and square.piece_type == PieceType.PAWN and square.color == color:
                                pawn_shield_bonus += 10
                                break
        else:
            # Check pawns in front of black king
            for file_offset in [-1, 0, 1]:
                shield_file = king_file + file_offset
                if 0 <= shield_file < 8:
                    for rank_check in [king_rank + 1, king_rank + 2]:
                        if 0 <= rank_check < 8:
                            square = board.get_piece((shield_file, rank_check))
                            if square and square.piece_type == PieceType.PAWN and square.color == color:
                                pawn_shield_bonus += 10
                                break
        
        safety_score += pawn_shield_bonus
        
        # Penalty for king in center during opening/middlegame
        if len(board.move_history) < 20:  # Opening/early middlegame
            center_penalty = 0
            if 2 <= king_file <= 5:  # King in center files
                center_penalty -= 20
            if color == Color.WHITE and king_rank > 1:  # White king moved forward
                center_penalty -= 15
            elif color == Color.BLACK and king_rank < 6:  # Black king moved forward
                center_penalty -= 15
            safety_score += center_penalty
        
        # Bonus for castling (if king is on castled position)
        castling_bonus = 0
        if color == Color.WHITE:
            if king_pos == (6, 7) or king_pos == (2, 7):  # Kingside or queenside castle
                castling_bonus += 30
        else:
            if king_pos == (6, 0) or king_pos == (2, 0):  # Kingside or queenside castle
                castling_bonus += 30
        
        safety_score += castling_bonus
        
        return safety_score
    
    def _evaluate_pawn_structure(self, board: ChessBoard, color: Color) -> float:
        """Evaluate pawn structure"""
        structure_score = 0.0
        
        # Get all pawns for both colors
        own_pawns = []
        enemy_pawns = []
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and square.piece_type == PieceType.PAWN:
                    if square.color == color:
                        own_pawns.append((file, rank))
                    else:
                        enemy_pawns.append((file, rank))
        
        # Evaluate each pawn
        for pawn_file, pawn_rank in own_pawns:
            
            # Check for doubled pawns (penalty)
            doubled_count = sum(1 for f, r in own_pawns if f == pawn_file)
            if doubled_count > 1:
                structure_score -= 10 * (doubled_count - 1)
            
            # Check for isolated pawns (penalty)
            has_adjacent_pawn = False
            for adj_file in [pawn_file - 1, pawn_file + 1]:
                if 0 <= adj_file < 8:
                    if any(f == adj_file for f, r in own_pawns):
                        has_adjacent_pawn = True
                        break
            
            if not has_adjacent_pawn:
                structure_score -= 15  # Isolated pawn penalty
            
            # Check for passed pawns (bonus)
            is_passed = True
            if color == Color.WHITE:
                # Check if any enemy pawns can stop this pawn
                for enemy_file, enemy_rank in enemy_pawns:
                    if abs(enemy_file - pawn_file) <= 1 and enemy_rank < pawn_rank:
                        is_passed = False
                        break
                if is_passed:
                    # Bonus increases as pawn advances
                    passed_bonus = 20 + (6 - pawn_rank) * 10
                    structure_score += passed_bonus
            else:
                # Black pawns
                for enemy_file, enemy_rank in enemy_pawns:
                    if abs(enemy_file - pawn_file) <= 1 and enemy_rank > pawn_rank:
                        is_passed = False
                        break
                if is_passed:
                    # Bonus increases as pawn advances
                    passed_bonus = 20 + (pawn_rank - 1) * 10
                    structure_score += passed_bonus
            
            # Pawn chains (connected pawns) bonus
            chain_bonus = 0
            if color == Color.WHITE:
                # Check for supporting pawns diagonally behind
                for support_file in [pawn_file - 1, pawn_file + 1]:
                    if 0 <= support_file < 8 and pawn_rank < 7:
                        if (support_file, pawn_rank + 1) in own_pawns:
                            chain_bonus += 5
            else:
                # Black pawns
                for support_file in [pawn_file - 1, pawn_file + 1]:
                    if 0 <= support_file < 8 and pawn_rank > 0:
                        if (support_file, pawn_rank - 1) in own_pawns:
                            chain_bonus += 5
            
            structure_score += chain_bonus
        
        return structure_score
    
    def _evaluate_mobility(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece mobility"""
        mobility_score = 0.0
        
        # Count pseudo-legal moves for each piece type
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty and square.color == color:
                    piece_mobility = 0
                    
                    if square.piece_type == PieceType.KNIGHT:
                        # Knight mobility
                        knight_moves = [
                            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
                            (1, -2), (1, 2), (2, -1), (2, 1)
                        ]
                        for df, dr in knight_moves:
                            new_file, new_rank = file + df, rank + dr
                            if 0 <= new_file < 8 and 0 <= new_rank < 8:
                                target = board.get_piece((new_file, new_rank))
                                if target.empty or target.color != color:
                                    piece_mobility += 1
                        
                        mobility_score += piece_mobility * 2  # Knight mobility weight
                    
                    elif square.piece_type == PieceType.BISHOP:
                        # Bishop mobility
                        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                        for df, dr in directions:
                            for distance in range(1, 8):
                                new_file = file + df * distance
                                new_rank = rank + dr * distance
                                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                                    break
                                target = board.get_piece((new_file, new_rank))
                                if target.empty:
                                    piece_mobility += 1
                                elif target.color != color:
                                    piece_mobility += 1
                                    break
                                else:
                                    break
                        
                        mobility_score += piece_mobility * 1.5  # Bishop mobility weight
                    
                    elif square.piece_type == PieceType.ROOK:
                        # Rook mobility
                        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        for df, dr in directions:
                            for distance in range(1, 8):
                                new_file = file + df * distance
                                new_rank = rank + dr * distance
                                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                                    break
                                target = board.get_piece((new_file, new_rank))
                                if target.empty:
                                    piece_mobility += 1
                                elif target.color != color:
                                    piece_mobility += 1
                                    break
                                else:
                                    break
                        
                        mobility_score += piece_mobility * 1.0  # Rook mobility weight
                    
                    elif square.piece_type == PieceType.QUEEN:
                        # Queen mobility (combination of rook and bishop)
                        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                                    (1, 1), (1, -1), (-1, 1), (-1, -1)]
                        for df, dr in directions:
                            for distance in range(1, 8):
                                new_file = file + df * distance
                                new_rank = rank + dr * distance
                                if not (0 <= new_file < 8 and 0 <= new_rank < 8):
                                    break
                                target = board.get_piece((new_file, new_rank))
                                if target.empty:
                                    piece_mobility += 1
                                elif target.color != color:
                                    piece_mobility += 1
                                    break
                                else:
                                    break
                        
                        mobility_score += piece_mobility * 0.5  # Queen mobility weight (lower because queen is powerful)
        
        return mobility_score
    
    def _evaluate_center_control(self, board: ChessBoard, color: Color) -> float:
        """Evaluate center control"""
        center_score = 0.0
        
        # Central squares
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]  # d4, d5, e4, e5
        extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5), (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
        
        # Check occupation of center squares
        for file, rank in center_squares:
            square = board.get_piece((file, rank))
            if square and not square.empty:
                if square.color == color:
                    center_score += 10  # Bonus for occupying center
                else:
                    center_score -= 5   # Penalty for opponent occupying center
        
        # Check control of center squares (pieces that can move to center)
        for file, rank in center_squares:
            square = board.get_piece((file, rank))
            if square.empty:  # Only count control of empty center squares
                own_attackers = 0
                opponent_attackers = 0
                
                # Count pieces that can attack this square
                for r in range(8):
                    for f in range(8):
                        piece_square = board.get_piece((f, r))
                        if piece_square and not piece_square.empty:
                            if board._can_piece_attack(piece_square.piece_type, (f, r), (file, rank)):
                                if piece_square.color == color:
                                    own_attackers += 1
                                else:
                                    opponent_attackers += 1
                
                center_score += (own_attackers - opponent_attackers) * 2
        
        return center_score
    
    def _evaluate_development(self, board: ChessBoard, color: Color) -> float:
        """Evaluate piece development"""
        development_score = 0.0
        
        # Only evaluate development in opening (first 15 moves)
        if len(board.move_history) > 30:  # 15 moves per side
            return 0.0
        
        if color == Color.WHITE:
            back_rank = 7
            # Check if pieces are still on back rank
            pieces_to_check = [
                ((1, back_rank), PieceType.KNIGHT),  # b1 knight
                ((6, back_rank), PieceType.KNIGHT),  # g1 knight
                ((2, back_rank), PieceType.BISHOP),  # c1 bishop
                ((5, back_rank), PieceType.BISHOP),  # f1 bishop
            ]
        else:
            back_rank = 0
            pieces_to_check = [
                ((1, back_rank), PieceType.KNIGHT),  # b8 knight
                ((6, back_rank), PieceType.KNIGHT),  # g8 knight
                ((2, back_rank), PieceType.BISHOP),  # c8 bishop
                ((5, back_rank), PieceType.BISHOP),  # f8 bishop
            ]
        
        # Penalty for pieces still on starting squares
        for (file, rank), expected_piece in pieces_to_check:
            square = board.get_piece((file, rank))
            if square and not square.empty and square.piece_type == expected_piece and square.color == color:
                development_score -= 5  # Penalty for undeveloped piece
        
        # Bonus for castling
        king_pos = None
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and square.piece_type == PieceType.KING and square.color == color:
                    king_pos = (file, rank)
                    break
            if king_pos:
                break
        
        if king_pos:
            if color == Color.WHITE:
                if king_pos == (6, 7) or king_pos == (2, 7):  # Castled position
                    development_score += 20
            else:
                if king_pos == (6, 0) or king_pos == (2, 0):  # Castled position
                    development_score += 20
        
        return development_score
    
    def _evaluate_tempo(self, board: ChessBoard, color: Color) -> float:
        """Evaluate tempo (initiative)"""
        tempo_score = 0.0
        
        # Small bonus for having the move (being the active player)
        if board.current_player == color:
            tempo_score += 5
        
        # Bonus for active pieces (pieces that have moved from starting squares)
        active_pieces = 0
        total_pieces = 0
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty and square.color == color:
                    total_pieces += 1
                    
                    # Check if piece is on starting square
                    is_on_starting_square = False
                    
                    if color == Color.WHITE:
                        if rank == 7:  # Back rank
                            is_on_starting_square = True
                        elif rank == 6 and square.piece_type == PieceType.PAWN:  # Pawn rank
                            is_on_starting_square = True
                    else:
                        if rank == 0:  # Back rank
                            is_on_starting_square = True
                        elif rank == 1 and square.piece_type == PieceType.PAWN:  # Pawn rank
                            is_on_starting_square = True
                    
                    if not is_on_starting_square:
                        active_pieces += 1
        
        # Bonus for piece activity
        if total_pieces > 0:
            activity_ratio = active_pieces / total_pieces
            tempo_score += activity_ratio * 10
        
        return tempo_score
    
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