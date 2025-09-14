#!/usr/bin/env python3
"""
Learning Service

Educational features and learning assistance for chess improvement.
"""

import sys
import os
import random
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add chess engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color, PieceType
from chess_engine.board.move_generator import MoveGenerator
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine

from ..models.chess_models import HintResponse, PuzzleData

class LearningService:
    """Educational chess service for learning and improvement"""
    
    def __init__(self):
        """Initialize learning service"""
        self.engine = MinimaxEngine(max_depth=4, time_limit=3.0)
        self.evaluator = EvaluationEngine()
        
        # Sample puzzle database (in a real app, this would be from a database)
        self.puzzle_database = self._initialize_puzzle_database()
        
        # Learning statistics
        self.stats = {
            "hints_given": 0,
            "puzzles_solved": 0,
            "explanations_provided": 0
        }
    
    async def get_move_hint(self, fen: str) -> HintResponse:
        """Provide a helpful hint without giving away the exact move"""
        
        try:
            board = ChessBoard()
            
            # Get best move for analysis
            best_move, score = self.engine.search(board)
            
            if not best_move:
                return HintResponse(
                    hint_type="general",
                    message="Look for any legal moves available",
                    highlighted_squares=[],
                    suggested_moves=[],
                    explanation="No specific hints available for this position"
                )
            
            # Analyze position for hint type
            hint_type, message, highlighted_squares = await self._analyze_position_for_hints(board, best_move)
            
            # Get suggested move categories without revealing exact moves
            suggested_moves = await self._get_move_categories(board)
            
            # Generate explanation
            explanation = await self._generate_hint_explanation(board, best_move, score)
            
            self.stats["hints_given"] += 1
            
            return HintResponse(
                hint_type=hint_type,
                message=message,
                highlighted_squares=highlighted_squares,
                suggested_moves=suggested_moves,
                explanation=explanation
            )
            
        except Exception as e:
            return HintResponse(
                hint_type="error",
                message="Unable to provide hint at this time",
                highlighted_squares=[],
                suggested_moves=[],
                explanation=f"Error: {str(e)}"
            )
    
    async def explain_position(self, fen: str) -> Dict[str, Any]:
        """Provide educational explanation of the position"""
        
        try:
            board = ChessBoard()
            
            # Analyze position
            evaluation = self.evaluator.evaluate(board, board.current_player)
            
            explanation = {
                "overview": await self._get_position_overview(board, evaluation),
                "key_features": await self._identify_key_features(board),
                "strategic_concepts": await self._identify_strategic_concepts(board),
                "tactical_opportunities": await self._identify_tactical_opportunities(board),
                "learning_points": await self._generate_learning_points(board, evaluation)
            }
            
            self.stats["explanations_provided"] += 1
            
            return explanation
            
        except Exception as e:
            return {"error": f"Unable to explain position: {str(e)}"}
    
    async def get_puzzles(
        self,
        difficulty: str = "medium",
        theme: str = "all",
        count: int = 10
    ) -> List[PuzzleData]:
        """Get chess puzzles for training"""
        
        try:
            # Filter puzzles by criteria
            filtered_puzzles = []
            
            for puzzle in self.puzzle_database:
                # Filter by difficulty
                if difficulty != "all" and puzzle.rating != self._difficulty_to_rating(difficulty):
                    continue
                
                # Filter by theme
                if theme != "all" and theme not in puzzle.themes:
                    continue
                
                filtered_puzzles.append(puzzle)
            
            # Randomly select puzzles
            selected_puzzles = random.sample(
                filtered_puzzles, 
                min(count, len(filtered_puzzles))
            )
            
            return selected_puzzles
            
        except Exception as e:
            return []
    
    async def check_puzzle_solution(
        self,
        puzzle_id: str,
        moves: List[str]
    ) -> Dict[str, Any]:
        """Check if puzzle solution is correct"""
        
        try:
            # Find puzzle
            puzzle = None
            for p in self.puzzle_database:
                if p.puzzle_id == puzzle_id:
                    puzzle = p
                    break
            
            if not puzzle:
                return {"success": False, "error": "Puzzle not found"}
            
            # Check solution
            is_correct = moves == puzzle.moves
            
            result = {
                "success": True,
                "correct": is_correct,
                "solution": puzzle.moves,
                "explanation": puzzle.solution_explanation
            }
            
            if is_correct:
                result["message"] = "Correct! Well done!"
                self.stats["puzzles_solved"] += 1
            else:
                result["message"] = "Not quite right. Try again!"
                result["hint"] = await self._get_puzzle_hint(puzzle)
            
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Helper methods
    
    async def _analyze_position_for_hints(
        self,
        board: ChessBoard,
        best_move
    ) -> tuple[str, str, List[str]]:
        """Analyze position to determine hint type and content"""
        
        # Check for tactical opportunities
        if board.is_check(board.current_player):
            return (
                "tactical",
                "You're in check! Look for ways to get out of check.",
                [self._square_to_algebraic(square) for square in self._get_king_squares(board)]
            )
        
        # Check if best move gives check
        temp_board = board.copy()
        temp_board.make_move(best_move)
        opponent_color = Color.BLACK if board.current_player == Color.WHITE else Color.WHITE
        
        if temp_board.is_check(opponent_color):
            return (
                "tactical",
                "Look for a move that puts pressure on the opponent's king.",
                [self._square_to_algebraic(best_move.to_square)]
            )
        
        # Check for material gain
        captured_piece = board.get_piece(best_move.to_square)
        if captured_piece and not captured_piece.empty:
            return (
                "tactical",
                "Look for opportunities to win material.",
                [self._square_to_algebraic(best_move.to_square)]
            )
        
        # Default positional hint
        return (
            "positional",
            "Consider improving your piece activity and position.",
            []
        )
    
    async def _get_move_categories(self, board: ChessBoard) -> List[str]:
        """Get general move categories without revealing specific moves"""
        
        categories = []
        
        move_gen = MoveGenerator(board)
        legal_moves = move_gen.generate_legal_moves(board.current_player)
        
        # Analyze move types
        has_captures = any(
            not board.get_piece(move.to_square).empty 
            for move in legal_moves
        )
        
        has_checks = any(
            self._move_gives_check(board, move)
            for move in legal_moves
        )
        
        if has_captures:
            categories.append("captures")
        
        if has_checks:
            categories.append("checks")
        
        categories.extend(["development", "positional"])
        
        return categories
    
    async def _generate_hint_explanation(
        self,
        board: ChessBoard,
        best_move,
        score: float
    ) -> str:
        """Generate explanation for the hint"""
        
        explanations = []
        
        if score > 200:
            explanations.append("This position offers significant tactical opportunities")
        elif score > 50:
            explanations.append("Look for moves that improve your position")
        else:
            explanations.append("Focus on solid, developing moves")
        
        # Add specific guidance based on position
        if board.fullmove_number <= 10:
            explanations.append("In the opening, prioritize piece development and king safety")
        elif board.fullmove_number <= 25:
            explanations.append("In the middlegame, look for tactical opportunities and improve piece coordination")
        else:
            explanations.append("In the endgame, focus on king activity and pawn promotion")
        
        return ". ".join(explanations) + "."
    
    async def _get_position_overview(self, board: ChessBoard, evaluation: float) -> str:
        """Get general overview of the position"""
        
        overview_parts = []
        
        # Material assessment
        if evaluation > 200:
            overview_parts.append("White has a significant material advantage")
        elif evaluation > 50:
            overview_parts.append("White has a slight advantage")
        elif evaluation > -50:
            overview_parts.append("The position is roughly equal")
        elif evaluation > -200:
            overview_parts.append("Black has a slight advantage")
        else:
            overview_parts.append("Black has a significant advantage")
        
        # Game phase
        if board.fullmove_number <= 10:
            overview_parts.append("The game is in the opening phase")
        elif board.fullmove_number <= 25:
            overview_parts.append("The game is in the middlegame")
        else:
            overview_parts.append("The game is in the endgame")
        
        return ". ".join(overview_parts) + "."
    
    async def _identify_key_features(self, board: ChessBoard) -> List[str]:
        """Identify key features of the position"""
        
        features = []
        
        # Check for special conditions
        if board.is_check(board.current_player):
            features.append("King in check")
        
        if board.is_checkmate(board.current_player):
            features.append("Checkmate")
        
        if board.is_stalemate(board.current_player):
            features.append("Stalemate")
        
        # Add more sophisticated feature detection here
        features.extend([
            "Active piece play",
            "Central control",
            "King safety considerations"
        ])
        
        return features
    
    async def _identify_strategic_concepts(self, board: ChessBoard) -> List[str]:
        """Identify strategic concepts relevant to the position"""
        
        concepts = []
        
        # Game phase concepts
        if board.fullmove_number <= 10:
            concepts.extend([
                "Piece development",
                "Center control",
                "King safety"
            ])
        elif board.fullmove_number <= 25:
            concepts.extend([
                "Piece coordination",
                "Tactical awareness",
                "Pawn structure"
            ])
        else:
            concepts.extend([
                "King activity",
                "Pawn promotion",
                "Endgame technique"
            ])
        
        return concepts
    
    async def _identify_tactical_opportunities(self, board: ChessBoard) -> List[str]:
        """Identify tactical opportunities in the position"""
        
        opportunities = []
        
        # Simplified tactical detection
        if board.is_check(board.current_player):
            opportunities.append("Escape from check")
        
        # Check for captures
        move_gen = MoveGenerator(board)
        legal_moves = move_gen.generate_legal_moves(board.current_player)
        
        has_captures = any(
            not board.get_piece(move.to_square).empty 
            for move in legal_moves
        )
        
        if has_captures:
            opportunities.append("Material gain through captures")
        
        # Add more tactical pattern detection
        opportunities.extend([
            "Piece development",
            "Positional improvement"
        ])
        
        return opportunities
    
    async def _generate_learning_points(self, board: ChessBoard, evaluation: float) -> List[str]:
        """Generate educational learning points"""
        
        learning_points = []
        
        # General principles based on game phase
        if board.fullmove_number <= 10:
            learning_points.extend([
                "Develop pieces toward the center",
                "Castle early for king safety",
                "Don't move the same piece twice in the opening"
            ])
        elif board.fullmove_number <= 25:
            learning_points.extend([
                "Look for tactical combinations",
                "Improve piece coordination",
                "Consider pawn breaks to open lines"
            ])
        else:
            learning_points.extend([
                "Activate your king in the endgame",
                "Push passed pawns",
                "Centralize your king"
            ])
        
        return learning_points
    
    def _initialize_puzzle_database(self) -> List[PuzzleData]:
        """Initialize sample puzzle database"""
        
        puzzles = [
            PuzzleData(
                puzzle_id="puzzle_001",
                fen="r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4",
                moves=["Nf3-g5", "d7-d6", "Ng5xf7"],
                rating=1200,
                themes=["fork", "knight"],
                description="Knight fork winning the queen",
                solution_explanation="The knight on g5 can fork the king and queen by moving to f7"
            ),
            PuzzleData(
                puzzle_id="puzzle_002",
                fen="rnbqkb1r/pppp1ppp/5n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R b KQkq - 0 4",
                moves=["Nf6-g4", "Bf1-e2", "Ng4-e3"],
                rating=1400,
                themes=["fork", "knight", "tactics"],
                description="Knight fork attacking king and queen",
                solution_explanation="The knight can create a powerful fork by jumping to e3"
            ),
            PuzzleData(
                puzzle_id="puzzle_003",
                fen="r1bqk2r/pppp1ppp/2n2n2/2b1p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 0 6",
                moves=["Bc4xf7+", "Ke8-f8", "Nf3-g5"],
                rating=1600,
                themes=["sacrifice", "attack", "bishop"],
                description="Bishop sacrifice leading to mate",
                solution_explanation="Sacrificing the bishop on f7 opens up the black king for a mating attack"
            )
        ]
        
        return puzzles
    
    def _difficulty_to_rating(self, difficulty: str) -> int:
        """Convert difficulty string to rating range"""
        
        difficulty_map = {
            "beginner": 1000,
            "easy": 1200,
            "medium": 1400,
            "hard": 1600,
            "expert": 1800
        }
        
        return difficulty_map.get(difficulty, 1400)
    
    async def _get_puzzle_hint(self, puzzle: PuzzleData) -> str:
        """Get hint for a puzzle"""
        
        hints = {
            "fork": "Look for a move that attacks two pieces at once",
            "pin": "Look for a move that pins an opponent's piece",
            "skewer": "Look for a move that forces a valuable piece to move",
            "sacrifice": "Consider sacrificing material for a greater advantage",
            "attack": "Look for aggressive moves against the opponent's king"
        }
        
        # Return hint based on puzzle themes
        for theme in puzzle.themes:
            if theme in hints:
                return hints[theme]
        
        return "Look for the most forcing move in the position"
    
    def _move_gives_check(self, board: ChessBoard, move) -> bool:
        """Check if a move gives check"""
        
        temp_board = board.copy()
        temp_board.make_move(move)
        opponent_color = Color.BLACK if board.current_player == Color.WHITE else Color.WHITE
        
        return temp_board.is_check(opponent_color)
    
    def _get_king_squares(self, board: ChessBoard) -> List[tuple]:
        """Get squares where kings are located"""
        
        king_squares = []
        
        # Find kings on the board
        for rank in range(8):
            for file in range(8):
                piece = board.get_piece((file, rank))
                if piece and piece.piece_type == PieceType.KING:
                    king_squares.append((file, rank))
        
        return king_squares
    
    def _square_to_algebraic(self, square) -> str:
        """Convert square coordinates to algebraic notation"""
        file, rank = square
        return f"{chr(ord('a') + file)}{8 - rank}"