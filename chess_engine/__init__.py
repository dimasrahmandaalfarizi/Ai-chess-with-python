"""
Chess Engine - A modular chess engine with training capabilities

This package contains all the core components for a chess engine:
- Board representation and move generation
- Search algorithms (minimax, alpha-beta, quiescence)
- Evaluation functions with tunable weights
- Training and tuning capabilities
- UCI interface for GUI integration
"""

__version__ = "1.0.0"
__author__ = "Chess Engine Team"

from .board.board import ChessBoard
from .search.minimax import MinimaxEngine
from .eval.evaluation import EvaluationEngine

__all__ = ['ChessBoard', 'MinimaxEngine', 'EvaluationEngine']