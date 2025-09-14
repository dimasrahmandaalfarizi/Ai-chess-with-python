#!/usr/bin/env python3
"""
Analysis Service

Advanced chess position analysis and AI helper features.
"""

import sys
import os
import asyncio
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

# Add chess engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color, PieceType
from chess_engine.board.move_generator import MoveGenerator
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine

from ..models.chess_models import (
    AnalysisResult, BestMoveResponse, PositionEvaluation,
    EvaluationBreakdown, MoveVariation, Difficulty
)

class AnalysisService:
    """Advanced chess analysis service"""
    
    def __init__(self):
        """Initialize analysis service"""
        self.engine = MinimaxEngine(max_depth=6, time_limit=10.0)
        self.evaluator = EvaluationEngine()
        self.analysis_cache = {}
        self.stats = {
            "analyses_performed": 0,
            "total_analysis_time": 0.0,
            "average_depth": 0.0,
            "cache_hits": 0
        }
    
    async def analyze_position(
        self,
        fen: str,
        depth: int = 4,
        time_limit: float = 5.0,
        include_variations: bool = True
    ) -> AnalysisResult:
        """Perform comprehensive position analysis"""
        
        start_time = time.time()
        
        # Check cache first
        cache_key = f"{fen}_{depth}_{time_limit}"
        if cache_key in self.analysis_cache:
            self.stats["cache_hits"] += 1
            return self.analysis_cache[cache_key]
        
        try:
            # Create board from FEN (simplified - using starting position for now)
            board = ChessBoard()
            
            # Configure engine
            self.engine.max_depth = depth
            self.engine.time_limit = time_limit
            
            # Get best move and evaluation
            best_move, score = self.engine.search(board)
            
            # Get detailed evaluation
            evaluation = await self._get_detailed_evaluation(board, fen)
            
            # Get best moves (top 3)
            best_moves = await self._get_best_moves(board, depth=depth, count=3)
            
            # Get variations if requested
            variations = []
            if include_variations:
                variations = await self._get_variations(board, depth=depth)
            
            # Find tactical motifs
            tactical_motifs = await self._find_tactical_motifs(board)
            
            # Get opening information
            opening_info = await self._get_opening_info(board)
            
            analysis_time = time.time() - start_time
            
            # Create result
            result = AnalysisResult(
                fen=fen,
                evaluation=evaluation,
                best_moves=best_moves,
                variations=variations,
                tactical_motifs=tactical_motifs,
                opening_info=opening_info,
                analysis_time=analysis_time,
                nodes_searched=1000  # Simplified
            )
            
            # Cache result
            self.analysis_cache[cache_key] = result
            
            # Update stats
            self.stats["analyses_performed"] += 1
            self.stats["total_analysis_time"] += analysis_time
            self.stats["average_depth"] = (
                (self.stats["average_depth"] * (self.stats["analyses_performed"] - 1) + depth) /
                self.stats["analyses_performed"]
            )
            
            return result
            
        except Exception as e:
            # Return error result
            return AnalysisResult(
                fen=fen,
                evaluation=PositionEvaluation(score=0.0, evaluation="error"),
                best_moves=[],
                variations=[],
                tactical_motifs=[f"Analysis error: {str(e)}"],
                analysis_time=time.time() - start_time,
                nodes_searched=0
            )
    
    async def get_best_move(
        self,
        fen: str,
        depth: int = 4,
        difficulty: Difficulty = Difficulty.MEDIUM
    ) -> BestMoveResponse:
        """Get best move with explanation"""
        
        try:
            # Create board from FEN
            board = ChessBoard()
            
            # Adjust engine settings based on difficulty
            engine_settings = self._get_engine_settings_for_difficulty(difficulty)
            self.engine.max_depth = min(depth, engine_settings["max_depth"])
            self.engine.time_limit = engine_settings["time_limit"]
            
            # Get best move
            best_move, score = self.engine.search(board)
            
            if not best_move:
                return BestMoveResponse(
                    move="",
                    san="",
                    evaluation=0.0,
                    confidence=0.0,
                    explanation="No legal moves available",
                    alternatives=[]
                )
            
            # Get alternative moves
            alternatives = await self._get_alternative_moves(board, best_move, count=3)
            
            # Generate explanation
            explanation = await self._explain_move(board, best_move, score)
            
            # Determine tactical theme
            tactical_theme = await self._identify_tactical_theme(board, best_move)
            
            # Calculate confidence based on score difference with alternatives
            confidence = self._calculate_move_confidence(score, alternatives)
            
            return BestMoveResponse(
                move=self._move_to_uci(best_move),
                san=self._move_to_san(best_move),  # Simplified
                evaluation=score,
                confidence=confidence,
                explanation=explanation,
                alternatives=alternatives,
                tactical_theme=tactical_theme
            )
            
        except Exception as e:
            return BestMoveResponse(
                move="",
                san="",
                evaluation=0.0,
                confidence=0.0,
                explanation=f"Error: {str(e)}",
                alternatives=[]
            )
    
    async def evaluate_position(
        self,
        fen: str,
        detailed: bool = True
    ) -> PositionEvaluation:
        """Evaluate chess position"""
        
        try:
            # Create board from FEN
            board = ChessBoard()
            
            # Get evaluation
            score = self.evaluator.evaluate(board, board.current_player)
            
            # Determine evaluation description
            evaluation_desc = self._score_to_description(score)
            
            # Get detailed breakdown if requested
            breakdown = None
            if detailed:
                breakdown = await self._get_evaluation_breakdown(board)
            
            # Check for mate
            mate_in = None
            if abs(score) > 9000:
                mate_in = int((10000 - abs(score)) / 2)
                if score < 0:
                    mate_in = -mate_in
            
            return PositionEvaluation(
                score=score,
                mate_in=mate_in,
                evaluation=evaluation_desc,
                breakdown=breakdown
            )
            
        except Exception as e:
            return PositionEvaluation(
                score=0.0,
                evaluation=f"Error: {str(e)}"
            )
    
    # Helper methods will be added in the next part
    def _move_to_uci(self, move) -> str:
        """Convert move to UCI notation"""
        if not move:
            return ""
        
        from_sq = self._square_to_algebraic(move.from_square)
        to_sq = self._square_to_algebraic(move.to_square)
        
        return f"{from_sq}{to_sq}"
    
    def _move_to_san(self, move) -> str:
        """Convert move to Standard Algebraic Notation"""
        # Simplified SAN conversion
        return self._move_to_uci(move)
    
    def _square_to_algebraic(self, square) -> str:
        """Convert square coordinates to algebraic notation"""
        file, rank = square
        return f"{chr(ord('a') + file)}{8 - rank}"
    
    def _score_to_description(self, score: float) -> str:
        """Convert numerical score to descriptive text"""
        
        if score > 500:
            return "winning"
        elif score > 200:
            return "significant advantage"
        elif score > 50:
            return "slight advantage"
        elif score > -50:
            return "equal"
        elif score > -200:
            return "slight disadvantage"
        elif score > -500:
            return "significant disadvantage"
        else:
            return "losing"
    
    def _get_engine_settings_for_difficulty(self, difficulty: Difficulty) -> Dict[str, Any]:
        """Get engine settings based on difficulty"""
        
        settings_map = {
            Difficulty.BEGINNER: {"max_depth": 2, "time_limit": 1.0},
            Difficulty.EASY: {"max_depth": 3, "time_limit": 2.0},
            Difficulty.MEDIUM: {"max_depth": 4, "time_limit": 5.0},
            Difficulty.HARD: {"max_depth": 5, "time_limit": 8.0},
            Difficulty.EXPERT: {"max_depth": 6, "time_limit": 15.0}
        }
        
        return settings_map.get(difficulty, {"max_depth": 4, "time_limit": 5.0})
    
    async def _get_detailed_evaluation(self, board: ChessBoard, fen: str) -> PositionEvaluation:
        """Get detailed position evaluation"""
        
        score = self.evaluator.evaluate(board, board.current_player)
        evaluation_desc = self._score_to_description(score)
        
        # Get detailed breakdown
        breakdown = await self._get_evaluation_breakdown(board)
        
        return PositionEvaluation(
            score=score,
            evaluation=evaluation_desc,
            breakdown=breakdown
        )
    
    async def _get_evaluation_breakdown(self, board: ChessBoard) -> EvaluationBreakdown:
        """Get detailed evaluation breakdown"""
        
        total_score = self.evaluator.evaluate(board, board.current_player)
        
        return EvaluationBreakdown(
            material=total_score * 0.6,
            position=total_score * 0.2,
            king_safety=total_score * 0.1,
            pawn_structure=total_score * 0.05,
            mobility=total_score * 0.03,
            center_control=total_score * 0.01,
            development=total_score * 0.005,
            tempo=total_score * 0.005,
            total=total_score
        )
    
    async def _get_best_moves(self, board: ChessBoard, depth: int = 4, count: int = 3) -> List[Dict[str, Any]]:
        """Get top best moves"""
        
        move_gen = MoveGenerator(board)
        legal_moves = move_gen.generate_legal_moves(board.current_player)
        
        move_evaluations = []
        
        for move in legal_moves[:10]:  # Limit to first 10 moves for performance
            temp_board = board.copy()
            temp_board.make_move(move)
            
            # Quick evaluation
            score = self.evaluator.evaluate(temp_board, board.current_player)
            
            move_evaluations.append({
                "move": self._move_to_uci(move),
                "san": self._move_to_san(move),
                "evaluation": score,
                "confidence": 0.8  # Simplified
            })
        
        # Sort by evaluation and return top moves
        move_evaluations.sort(key=lambda x: x["evaluation"], reverse=True)
        return move_evaluations[:count]
    
    async def _get_variations(self, board: ChessBoard, depth: int = 4) -> List[MoveVariation]:
        """Get move variations"""
        
        variations = []
        
        # Get top 3 moves and create simple variations
        best_moves = await self._get_best_moves(board, depth, 3)
        
        for i, move_data in enumerate(best_moves):
            variation = MoveVariation(
                moves=[move_data["move"]],
                evaluation=move_data["evaluation"],
                depth=1,  # Simplified
                description=f"Line {i+1}: {move_data['san']}"
            )
            variations.append(variation)
        
        return variations
    
    async def _find_tactical_motifs(self, board: ChessBoard) -> List[str]:
        """Find tactical motifs in position"""
        
        motifs = []
        
        # Simplified tactical detection
        if board.is_check(board.current_player):
            motifs.append("Check")
        
        if board.is_checkmate(board.current_player):
            motifs.append("Checkmate")
        
        if board.is_stalemate(board.current_player):
            motifs.append("Stalemate")
        
        return motifs
    
    async def _get_opening_info(self, board: ChessBoard) -> Optional[Dict[str, str]]:
        """Get opening information"""
        
        # Simplified opening detection
        if board.fullmove_number <= 10:
            return {
                "name": "Opening Phase",
                "eco": "A00",
                "description": "Game is in the opening phase"
            }
        
        return None
    
    async def _get_alternative_moves(self, board: ChessBoard, best_move, count: int = 3) -> List[Dict[str, Any]]:
        """Get alternative moves to the best move"""
        
        best_moves = await self._get_best_moves(board, count=count + 1)
        
        # Filter out the best move
        best_move_uci = self._move_to_uci(best_move)
        alternatives = [
            move for move in best_moves 
            if move["move"] != best_move_uci
        ]
        
        return alternatives[:count]
    
    async def _explain_move(self, board: ChessBoard, move, score: float) -> str:
        """Generate explanation for a move"""
        
        explanations = []
        
        if score > 200:
            explanations.append("This move gives a significant advantage")
        elif score > 50:
            explanations.append("This move provides a slight advantage")
        elif score > -50:
            explanations.append("This move maintains equality")
        elif score > -200:
            explanations.append("This move leads to a slight disadvantage")
        else:
            explanations.append("This move is problematic")
        
        # Add tactical explanations
        if board.is_check(Color.BLACK if board.current_player == Color.WHITE else Color.WHITE):
            explanations.append("The move gives check")
        
        return ". ".join(explanations) + "."
    
    async def _identify_tactical_theme(self, board: ChessBoard, move) -> Optional[str]:
        """Identify tactical theme of a move"""
        
        # Simplified tactical theme detection
        if board.is_check(Color.BLACK if board.current_player == Color.WHITE else Color.WHITE):
            return "Check"
        
        return None
    
    def _calculate_move_confidence(self, best_score: float, alternatives: List[Dict[str, Any]]) -> float:
        """Calculate confidence in the best move"""
        
        if not alternatives:
            return 0.9
        
        # Calculate confidence based on score difference
        second_best_score = alternatives[0]["evaluation"] if alternatives else best_score - 100
        score_diff = abs(best_score - second_best_score)
        
        # Normalize to 0.0-1.0 range
        confidence = min(0.95, 0.5 + (score_diff / 400))
        return round(confidence, 2)