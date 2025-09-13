"""
Board module - Chess board representation and move generation

This module handles:
- Chess board representation
- Legal move generation
- Move validation
- Game state management
"""

from .board import ChessBoard
from .move_generator import MoveGenerator

__all__ = ['ChessBoard', 'MoveGenerator']