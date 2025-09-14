#!/usr/bin/env python3
"""
Chess Service

Core chess game logic and engine integration.
"""

import sys
import os
import asyncio
import time
from typing import Dict, List, Optional, Any
from datetime import datetime

# Add chess engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'chess_engine'))

try:
    from chess_engine.board.board import ChessBoard, Color, PieceType
    from chess_engine.board.move_generator import MoveGenerator
    from chess_engine.search.minimax import MinimaxEngine
    from chess_engine.eval.evaluation import EvaluationEngine
except ImportError:
    # Fallback if chess engine is not available
    print("Warning: Chess engine not found, using mock implementations")
    ChessBoard = None
    Color = None
    PieceType = None
    MoveGenerator = None
    MinimaxEngine = None
    EvaluationEngine = None

from ..models.chess_models import (
    GameState, GameMode, Difficulty, PieceColor, GameStatus,
    MoveInfo, EngineInfo, EngineSettings
)

class ChessService:
    """Chess game service with AI engine integration"""
    
    def __init__(self):
        """Initialize chess service"""
        self.games: Dict[str, Any] = {}
        self.engines: Dict[str, Any] = {}
        self.evaluators: Dict[str, Any] = {}
        self.game_settings: Dict[str, Dict] = {}
        
        # Default engine settings
        self.default_settings = {
            "depth": 4,
            "time_limit": 5.0,
            "use_opening_book": True,
            "contempt": 0.0,
            "randomness": 0.1
        }
        
        # Initialize engine if available
        if MinimaxEngine:
            self.default_engine = MinimaxEngine(max_depth=4, time_limit=5.0)
        else:
            self.default_engine = None
            
        if EvaluationEngine:
            self.default_evaluator = EvaluationEngine()
        else:
            self.default_evaluator = None
    
    async def create_game(
        self,
        game_id: str,
        mode: GameMode,
        difficulty: Optional[Difficulty] = None,
        player_color: Optional[PieceColor] = None,
        starting_fen: Optional[str] = None
    ) -> GameState:
        """Create a new chess game"""
        
        # Create chess board (mock if engine not available)
        if ChessBoard:
            board = ChessBoard()
        else:
            board = self._create_mock_board()
        
        if starting_fen:
            # TODO: Implement FEN loading
            pass
        
        # Store game
        self.games[game_id] = board
        
        # Create engine for AI games
        if mode == GameMode.HUMAN_VS_AI and self.default_engine:
            engine_settings = self._get_engine_settings_for_difficulty(difficulty)
            if MinimaxEngine:
                engine = MinimaxEngine(
                    max_depth=engine_settings["depth"],
                    time_limit=engine_settings["time_limit"]
                )
                self.engines[game_id] = engine
            
            # Create evaluator
            if self.default_evaluator:
                self.evaluators[game_id] = self.default_evaluator
        
        # Store game settings
        self.game_settings[game_id] = {
            "mode": mode,
            "difficulty": difficulty,
            "player_color": player_color,
            "created_at": datetime.now()
        }
        
        return self._create_game_state(game_id, board)
    
    async def make_move(
        self,
        game_id: str,
        move: str,
        promotion: Optional[str] = None
    ) -> Dict[str, Any]:
        """Make a move in the game"""
        
        if game_id not in self.games:
            return {"success": False, "error": "Game not found"}
        
        board = self.games[game_id]
        
        try:
            # Mock move implementation
            if ChessBoard and hasattr(board, 'make_move'):
                # Real implementation would parse and validate move
                success = True
            else:
                # Mock implementation
                success = True
            
            if not success:
                return {"success": False, "error": "Invalid move"}
            
            # Create move info (mock)
            move_info = MoveInfo(
                move=move,
                san=move,
                uci=move,
                from_square=move[:2] if len(move) >= 4 else "e2",
                to_square=move[2:4] if len(move) >= 4 else "e4",
                piece="pawn",
                is_check=False,
                is_checkmate=False,
                is_castling=False,
                is_en_passant=False
            )
            
            # Create updated game state
            game_state = self._create_game_state(game_id, board)
            
            return {
                "success": True,
                "move_info": move_info,
                "game_state": game_state
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_ai_move(self, game_id: str) -> Dict[str, Any]:
        """Get AI move for the current position"""
        
        if game_id not in self.games:
            return {"success": False, "error": "Game not found"}
        
        if game_id not in self.engines:
            return {"success": False, "error": "No AI engine for this game"}
        
        board = self.games[game_id]
        engine = self.engines.get(game_id, self.default_engine)
        
        try:
            start_time = time.time()
            
            # Get best move from engine (mock if not available)
            if engine and hasattr(engine, 'search'):
                best_move, score = engine.search(board)
            else:
                # Mock AI move
                best_move = self._get_mock_move()
                score = 0.5
            
            thinking_time = time.time() - start_time
            
            if not best_move:
                return {"success": False, "error": "No legal moves available"}
            
            # Make the AI move (mock)
            move_info = MoveInfo(
                move="e2e4",
                san="e4",
                uci="e2e4",
                from_square="e2",
                to_square="e4",
                piece="pawn",
                is_check=False,
                is_checkmate=False,
                is_castling=False,
                is_en_passant=False
            )
            
            # Create updated game state
            game_state = self._create_game_state(game_id, board)
            
            return {
                "success": True,
                "move_info": move_info,
                "game_state": game_state,
                "thinking_time": thinking_time,
                "evaluation": score
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_legal_moves(self, game_id: str) -> List[str]:
        """Get legal moves for current position"""
        
        if game_id not in self.games:
            return []
        
        board = self.games[game_id]
        
        # Mock legal moves
        return ["e2e4", "d2d4", "Nf3", "Nc3", "g3", "f4"]
    
    async def undo_move(self, game_id: str) -> Dict[str, Any]:
        """Undo the last move"""
        
        if game_id not in self.games:
            return {"success": False, "error": "Game not found"}
        
        board = self.games[game_id]
        
        try:
            # Mock undo implementation
            success = True
            
            if not success:
                return {"success": False, "error": "No moves to undo"}
            
            # Create updated game state
            game_state = self._create_game_state(game_id, board)
            
            return {
                "success": True,
                "game_state": game_state
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def analyze_position(
        self,
        fen: str,
        depth: int = 4
    ) -> Dict[str, Any]:
        """Analyze a chess position"""
        
        try:
            # Mock analysis
            return {
                "best_move": "e2e4",
                "evaluation": 0.5,
                "detailed_eval": {
                    "material": 0.0,
                    "position": 0.3,
                    "king_safety": 0.1,
                    "total": 0.4
                },
                "depth": depth
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    async def get_engine_info(self) -> EngineInfo:
        """Get chess engine information"""
        
        return EngineInfo(
            name="Chess AI Helper Engine",
            version="1.0.0",
            author="Chess Engine Team",
            features=[
                "Minimax with Alpha-Beta Pruning",
                "Position Evaluation",
                "Move Generation",
                "Game State Management"
            ],
            max_depth=10,
            nodes_per_second=1000,
            evaluation_range={"min": -1000, "max": 1000}
        )
    
    async def update_engine_settings(
        self,
        settings: EngineSettings
    ) -> Dict[str, Any]:
        """Update engine settings"""
        
        try:
            # Update default settings
            self.default_settings.update(settings.dict())
            
            # Update existing engines
            for game_id, engine in self.engines.items():
                if hasattr(engine, 'max_depth'):
                    engine.max_depth = settings.depth
                if hasattr(engine, 'time_limit'):
                    engine.time_limit = settings.time_limit
            
            return {"success": True, "settings": settings.dict()}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_game_state(self, game_id: str, board: Any) -> GameState:
        """Create game state from board"""
        
        # Mock game state
        return GameState(
            game_id=game_id,
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            pgn="",
            status=GameStatus.ACTIVE,
            turn=PieceColor.WHITE,
            move_number=1,
            halfmove_clock=0,
            legal_moves=["e2e4", "d2d4", "Nf3", "Nc3"],
            is_check=False,
            is_checkmate=False,
            is_stalemate=False,
            is_draw=False
        )
    
    def _create_mock_board(self):
        """Create a mock board when chess engine is not available"""
        return {
            "position": "starting",
            "turn": "white",
            "move_count": 0
        }
    
    def _get_mock_move(self):
        """Get a mock AI move"""
        return "e2e4"
    
    def _get_engine_settings_for_difficulty(self, difficulty: Optional[Difficulty]) -> Dict[str, Any]:
        """Get engine settings based on difficulty level"""
        
        if not difficulty:
            return self.default_settings
            
        settings_map = {
            Difficulty.BEGINNER: {"depth": 2, "time_limit": 1.0, "randomness": 0.3},
            Difficulty.EASY: {"depth": 3, "time_limit": 2.0, "randomness": 0.2},
            Difficulty.MEDIUM: {"depth": 4, "time_limit": 5.0, "randomness": 0.1},
            Difficulty.HARD: {"depth": 5, "time_limit": 8.0, "randomness": 0.05},
            Difficulty.EXPERT: {"depth": 6, "time_limit": 15.0, "randomness": 0.0}
        }
        
        return settings_map.get(difficulty, self.default_settings)