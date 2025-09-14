"""
Zobrist Hashing for Chess Positions

This module implements Zobrist hashing for efficient position caching
in the transposition table.
"""

import random
from typing import Dict, Tuple
from ..board.board import ChessBoard, PieceType, Color

class ZobristHash:
    """Zobrist hashing implementation for chess positions"""
    
    def __init__(self):
        """Initialize Zobrist hash tables"""
        # Seed for reproducible hashes
        random.seed(12345)
        
        # Hash values for pieces on squares
        self.piece_keys = {}
        for piece_type in PieceType:
            self.piece_keys[piece_type] = {}
            for color in Color:
                self.piece_keys[piece_type][color] = {}
                for square in range(64):
                    self.piece_keys[piece_type][color][square] = random.getrandbits(64)
        
        # Hash values for castling rights
        self.castling_keys = {
            'K': random.getrandbits(64),
            'Q': random.getrandbits(64),
            'k': random.getrandbits(64),
            'q': random.getrandbits(64)
        }
        
        # Hash values for en passant files
        self.en_passant_keys = {}
        for file in range(8):
            self.en_passant_keys[file] = random.getrandbits(64)
        
        # Hash value for side to move
        self.side_to_move_key = random.getrandbits(64)
    
    def hash_position(self, board: ChessBoard) -> int:
        """
        Generate Zobrist hash for current board position
        
        Args:
            board: Chess board to hash
            
        Returns:
            64-bit hash value
        """
        hash_value = 0
        
        # Hash pieces on board
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    square_index = rank * 8 + file
                    hash_value ^= self.piece_keys[square.piece_type][square.color][square_index]
        
        # Hash castling rights
        for right, available in board.castling_rights.items():
            if available:
                hash_value ^= self.castling_keys[right]
        
        # Hash en passant target
        if board.en_passant_target:
            file, rank = board.en_passant_target
            hash_value ^= self.en_passant_keys[file]
        
        # Hash side to move
        if board.current_player == Color.BLACK:
            hash_value ^= self.side_to_move_key
        
        return hash_value
    
    def update_hash_for_move(self, current_hash: int, board: ChessBoard, move) -> int:
        """
        Incrementally update hash for a move (more efficient than full rehash)
        
        Args:
            current_hash: Current position hash
            board: Chess board
            move: Move being made
            
        Returns:
            Updated hash value
        """
        # This is a simplified version - full implementation would handle
        # all move types incrementally
        return self.hash_position(board)

# Global instance
zobrist = ZobristHash()