"""
Training module - Chess engine training and tuning

This module contains:
- Genetic algorithm for weight tuning
- PGN dataset loading and parsing
- Neural network training for evaluation
- Self-play capabilities
"""

from .tuner import WeightTuner
from .dataset import ChessDataset
from .trainer import NeuralTrainer

__all__ = ['WeightTuner', 'ChessDataset', 'NeuralTrainer']