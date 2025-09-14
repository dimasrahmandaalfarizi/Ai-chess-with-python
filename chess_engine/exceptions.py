"""
Custom Exceptions for Chess Engine

This module defines custom exception classes for better error handling.
"""

class ChessEngineError(Exception):
    """Base exception for chess engine errors"""
    pass

class InvalidMoveError(ChessEngineError):
    """Raised when an invalid move is attempted"""
    pass

class InvalidPositionError(ChessEngineError):
    """Raised when board position is invalid"""
    pass

class SearchTimeoutError(ChessEngineError):
    """Raised when search exceeds time limit"""
    pass

class UCIProtocolError(ChessEngineError):
    """Raised when UCI protocol error occurs"""
    pass

class EvaluationError(ChessEngineError):
    """Raised when position evaluation fails"""
    pass