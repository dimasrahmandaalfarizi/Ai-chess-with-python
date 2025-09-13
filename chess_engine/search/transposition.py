"""
Transposition Table - Position caching for better search performance

This module implements:
- Zobrist hashing for position identification
- Transposition table with replacement strategies
- Position caching and retrieval
- Hash collision handling
"""

import random
import hashlib
from typing import Dict, Optional, Tuple, Any
from enum import Enum
from ..board.board import ChessBoard, Move, Color, PieceType

class NodeType(Enum):
    """Types of nodes in transposition table"""
    EXACT = 0
    LOWER_BOUND = 1
    UPPER_BOUND = 2

class TranspositionEntry:
    """Entry in transposition table"""
    def __init__(self, hash_key: int, move: Optional[Move], score: float, 
                 depth: int, node_type: NodeType, age: int):
        self.hash_key = hash_key
        self.move = move
        self.score = score
        self.depth = depth
        self.node_type = node_type
        self.age = age

class TranspositionTable:
    """Transposition table for chess position caching"""
    
    def __init__(self, size_mb: int = 64):
        """
        Initialize transposition table
        
        Args:
            size_mb: Size of table in megabytes
        """
        self.size = size_mb * 1024 * 1024 // 24  # Approximate entries (24 bytes per entry)
        self.table = [None] * self.size
        self.age = 0
        self.hits = 0
        self.misses = 0
        
        # Initialize Zobrist hashing
        self._init_zobrist()
    
    def _init_zobrist(self):
        """Initialize Zobrist hash tables"""
        random.seed(42)  # For reproducible hashes
        
        # Hash for piece positions
        self.piece_hashes = {}
        for piece_type in PieceType:
            for color in Color:
                self.piece_hashes[(piece_type, color)] = {}
                for rank in range(8):
                    for file in range(8):
                        self.piece_hashes[(piece_type, color)][(file, rank)] = random.randint(0, 2**64 - 1)
        
        # Hash for castling rights
        self.castling_hashes = {}
        for castling in ['K', 'Q', 'k', 'q']:
            self.castling_hashes[castling] = random.randint(0, 2**64 - 1)
        
        # Hash for en passant
        self.en_passant_hashes = {}
        for file in range(8):
            self.en_passant_hashes[file] = random.randint(0, 2**64 - 1)
        
        # Hash for side to move
        self.side_to_move_hash = random.randint(0, 2**64 - 1)
    
    def get_hash(self, board: ChessBoard) -> int:
        """
        Calculate Zobrist hash for board position
        
        Args:
            board: Chess board position
            
        Returns:
            Zobrist hash value
        """
        hash_value = 0
        
        # Hash piece positions
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty:
                    hash_value ^= self.piece_hashes[(square.piece_type, square.color)][(file, rank)]
        
        # Hash castling rights
        for castling, has_right in board.castling_rights.items():
            if has_right:
                hash_value ^= self.castling_hashes[castling]
        
        # Hash en passant target
        if board.en_passant_target:
            file, _ = board.en_passant_target
            hash_value ^= self.en_passant_hashes[file]
        
        # Hash side to move
        if board.current_player == Color.BLACK:
            hash_value ^= self.side_to_move_hash
        
        return hash_value
    
    def store(self, board: ChessBoard, move: Optional[Move], score: float, 
              depth: int, node_type: NodeType):
        """
        Store position in transposition table
        
        Args:
            board: Chess board position
            move: Best move found
            score: Evaluation score
            depth: Search depth
            node_type: Type of node (exact, lower bound, upper bound)
        """
        hash_key = self.get_hash(board)
        index = hash_key % self.size
        
        entry = TranspositionEntry(hash_key, move, score, depth, node_type, self.age)
        
        # Replacement strategy: replace if deeper or older
        if (self.table[index] is None or 
            self.table[index].depth <= depth or 
            self.table[index].age < self.age):
            self.table[index] = entry
    
    def retrieve(self, board: ChessBoard) -> Optional[TranspositionEntry]:
        """
        Retrieve position from transposition table
        
        Args:
            board: Chess board position
            
        Returns:
            Transposition entry if found, None otherwise
        """
        hash_key = self.get_hash(board)
        index = hash_key % self.size
        
        entry = self.table[index]
        if entry and entry.hash_key == hash_key:
            self.hits += 1
            return entry
        
        self.misses += 1
        return None
    
    def probe(self, board: ChessBoard, depth: int, alpha: float, beta: float) -> Tuple[Optional[float], Optional[Move]]:
        """
        Probe transposition table for position
        
        Args:
            board: Chess board position
            depth: Required search depth
            alpha: Alpha value
            beta: Beta value
            
        Returns:
            Tuple of (score, move) if found and useful, (None, None) otherwise
        """
        entry = self.retrieve(board)
        if entry is None or entry.depth < depth:
            return None, None
        
        if entry.node_type == NodeType.EXACT:
            return entry.score, entry.move
        elif entry.node_type == NodeType.LOWER_BOUND and entry.score >= beta:
            return beta, entry.move
        elif entry.node_type == NodeType.UPPER_BOUND and entry.score <= alpha:
            return alpha, entry.move
        
        return None, None
    
    def store_exact(self, board: ChessBoard, move: Optional[Move], score: float, depth: int):
        """Store exact score in transposition table"""
        self.store(board, move, score, depth, NodeType.EXACT)
    
    def store_lower_bound(self, board: ChessBoard, move: Optional[Move], score: float, depth: int):
        """Store lower bound score in transposition table"""
        self.store(board, move, score, depth, NodeType.LOWER_BOUND)
    
    def store_upper_bound(self, board: ChessBoard, move: Optional[Move], score: float, depth: int):
        """Store upper bound score in transposition table"""
        self.store(board, move, score, depth, NodeType.UPPER_BOUND)
    
    def clear(self):
        """Clear transposition table"""
        self.table = [None] * self.size
        self.age = 0
        self.hits = 0
        self.misses = 0
    
    def increment_age(self):
        """Increment age counter for replacement strategy"""
        self.age += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get transposition table statistics"""
        total_probes = self.hits + self.misses
        hit_rate = self.hits / total_probes if total_probes > 0 else 0
        
        return {
            'size': self.size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'age': self.age
        }
    
    def get_usage(self) -> float:
        """Get table usage percentage"""
        used_entries = sum(1 for entry in self.table if entry is not None)
        return (used_entries / self.size) * 100