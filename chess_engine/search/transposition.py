"""
Transposition Table Implementation

This module provides an efficient transposition table with LRU eviction
for caching search results.
"""

from collections import OrderedDict
from typing import Optional, Dict, Any, Tuple
from enum import Enum

class NodeType(Enum):
    """Type of transposition table entry"""
    EXACT = 1      # Exact score
    LOWER_BOUND = 2  # Alpha cutoff (fail-high)
    UPPER_BOUND = 3  # Beta cutoff (fail-low)

class TranspositionEntry:
    """Entry in the transposition table"""
    
    def __init__(self, depth: int, score: float, node_type: NodeType, 
                 best_move=None, age: int = 0):
        self.depth = depth
        self.score = score
        self.node_type = node_type
        self.best_move = best_move
        self.age = age  # For replacement scheme

class LRUTranspositionTable:
    """
    LRU-based transposition table with size limit
    """
    
    def __init__(self, max_size: int = 1000000):
        """
        Initialize transposition table
        
        Args:
            max_size: Maximum number of entries
        """
        self.max_size = max_size
        self.table = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.collisions = 0
        self.current_age = 0
    
    def get(self, key: int) -> Optional[TranspositionEntry]:
        """
        Get entry from table
        
        Args:
            key: Position hash
            
        Returns:
            TranspositionEntry if found, None otherwise
        """
        if key in self.table:
            # Move to end (most recently used)
            entry = self.table[key]
            self.table.move_to_end(key)
            self.hits += 1
            return entry
        
        self.misses += 1
        return None
    
    def put(self, key: int, entry: TranspositionEntry):
        """
        Store entry in table
        
        Args:
            key: Position hash
            entry: TranspositionEntry to store
        """
        entry.age = self.current_age
        
        if key in self.table:
            # Update existing entry if new one is better
            existing = self.table[key]
            if self._should_replace(existing, entry):
                self.table[key] = entry
                self.table.move_to_end(key)
        else:
            # Add new entry
            if len(self.table) >= self.max_size:
                # Remove least recently used entry
                self.table.popitem(last=False)
            
            self.table[key] = entry
    
    def _should_replace(self, existing: TranspositionEntry, new: TranspositionEntry) -> bool:
        """
        Determine if existing entry should be replaced
        
        Args:
            existing: Current entry
            new: New entry
            
        Returns:
            True if should replace, False otherwise
        """
        # Replace if new entry has greater depth
        if new.depth > existing.depth:
            return True
        
        # Replace if same depth but newer age
        if new.depth == existing.depth and new.age > existing.age:
            return True
        
        # Replace if much newer (even if lower depth)
        if new.age - existing.age > 4:
            return True
        
        return False
    
    def clear(self):
        """Clear the transposition table"""
        self.table.clear()
        self.hits = 0
        self.misses = 0
        self.collisions = 0
        self.current_age = 0
    
    def new_search(self):
        """Increment age for new search"""
        self.current_age += 1
    
    def get_stats(self) -> Dict[str, Any]:
        """Get transposition table statistics"""
        total_accesses = self.hits + self.misses
        hit_rate = self.hits / total_accesses if total_accesses > 0 else 0
        
        return {
            'size': len(self.table),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate,
            'collisions': self.collisions,
            'current_age': self.current_age
        }
    
    def resize(self, new_size: int):
        """
        Resize the transposition table
        
        Args:
            new_size: New maximum size
        """
        self.max_size = new_size
        
        # Remove entries if current size exceeds new limit
        while len(self.table) > new_size:
            self.table.popitem(last=False)

class SimpleTranspositionTable:
    """
    Simple dictionary-based transposition table (for comparison)
    """
    
    def __init__(self, max_size: int = 1000000):
        self.max_size = max_size
        self.table = {}
        self.hits = 0
        self.misses = 0
    
    def get(self, key: int) -> Optional[TranspositionEntry]:
        if key in self.table:
            self.hits += 1
            return self.table[key]
        
        self.misses += 1
        return None
    
    def put(self, key: int, entry: TranspositionEntry):
        if len(self.table) >= self.max_size:
            # Simple eviction: clear half the table
            keys_to_remove = list(self.table.keys())[:len(self.table) // 2]
            for k in keys_to_remove:
                del self.table[k]
        
        self.table[key] = entry
    
    def clear(self):
        self.table.clear()
        self.hits = 0
        self.misses = 0
    
    def get_stats(self) -> Dict[str, Any]:
        total_accesses = self.hits + self.misses
        hit_rate = self.hits / total_accesses if total_accesses > 0 else 0
        
        return {
            'size': len(self.table),
            'max_size': self.max_size,
            'hits': self.hits,
            'misses': self.misses,
            'hit_rate': hit_rate
        }