"""
Evaluation module - Chess position evaluation

This module handles:
- Position evaluation functions
- Tunable evaluation weights
- Material, positional, and tactical evaluation
"""

from .evaluation import EvaluationEngine

__all__ = ['EvaluationEngine']