"""
Search module - Chess search algorithms

This module contains:
- Minimax algorithm with alpha-beta pruning
- Quiescence search for tactical positions
- Transposition table for position caching
- Iterative deepening
"""

from .minimax import MinimaxEngine
from .quiescence import QuiescenceSearch
from .transposition import LRUTranspositionTable, TranspositionEntry

__all__ = ['MinimaxEngine', 'QuiescenceSearch', 'TranspositionTable']