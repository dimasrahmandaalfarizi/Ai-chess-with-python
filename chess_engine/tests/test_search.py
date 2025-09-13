"""
Unit tests for search module
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.search.transposition import TranspositionTable, NodeType
from chess_engine.search.quiescence import QuiescenceSearch

class TestMinimaxEngine(unittest.TestCase):
    """Test cases for MinimaxEngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
        self.engine = MinimaxEngine(max_depth=2, time_limit=1.0)
    
    def test_engine_initialization(self):
        """Test engine initialization"""
        self.assertEqual(self.engine.max_depth, 2)
        self.assertEqual(self.engine.time_limit, 1.0)
        self.assertEqual(self.engine.nodes_searched, 0)
    
    def test_search_basic(self):
        """Test basic search functionality"""
        # Test search on initial position
        best_move, score = self.engine.search(self.board)
        
        # Should return a move and score
        self.assertIsNotNone(best_move)
        self.assertIsInstance(score, float)
        
        # Score should be finite
        self.assertTrue(abs(score) < float('inf'))
    
    def test_search_stats(self):
        """Test search statistics"""
        self.engine.search(self.board)
        stats = self.engine.get_search_stats()
        
        self.assertIn('nodes_searched', stats)
        self.assertIn('cutoffs', stats)
        self.assertIn('transposition_hits', stats)
        self.assertIn('quiescence_nodes', stats)
        
        self.assertGreater(stats['nodes_searched'], 0)

class TestTranspositionTable(unittest.TestCase):
    """Test cases for TranspositionTable class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.table = TranspositionTable(size_mb=1)  # Small size for testing
        self.board = ChessBoard()
    
    def test_table_initialization(self):
        """Test table initialization"""
        self.assertGreater(self.table.size, 0)
        self.assertEqual(self.table.age, 0)
        self.assertEqual(self.table.hits, 0)
        self.assertEqual(self.table.misses, 0)
    
    def test_hash_generation(self):
        """Test hash generation"""
        hash1 = self.table.get_hash(self.board)
        hash2 = self.table.get_hash(self.board)
        
        # Same position should generate same hash
        self.assertEqual(hash1, hash2)
        
        # Hash should be an integer
        self.assertIsInstance(hash1, int)
    
    def test_store_and_retrieve(self):
        """Test storing and retrieving entries"""
        from chess_engine.board.move_generator import MoveGenerator
        from chess_engine.board.board import Move, PieceType
        
        # Create a test move
        move = Move((1, 6), (1, 4), PieceType.PAWN, Color.WHITE)
        
        # Store entry
        self.table.store_exact(self.board, move, 0.5, 3)
        
        # Retrieve entry
        entry = self.table.retrieve(self.board)
        self.assertIsNotNone(entry)
        self.assertEqual(entry.move, move)
        self.assertEqual(entry.score, 0.5)
        self.assertEqual(entry.depth, 3)
        self.assertEqual(entry.node_type, NodeType.EXACT)
    
    def test_probe_functionality(self):
        """Test probe functionality"""
        from chess_engine.board.move_generator import MoveGenerator
        from chess_engine.board.board import Move, PieceType
        
        # Create a test move
        move = Move((1, 6), (1, 4), PieceType.PAWN, Color.WHITE)
        
        # Store entry
        self.table.store_exact(self.board, move, 0.5, 3)
        
        # Probe for exact match
        score, retrieved_move = self.table.probe(self.board, 3, -1.0, 1.0)
        self.assertEqual(score, 0.5)
        self.assertEqual(retrieved_move, move)
        
        # Probe for lower bound
        self.table.store_lower_bound(self.board, move, 0.3, 2)
        score, retrieved_move = self.table.probe(self.board, 2, 0.2, 1.0)
        # Note: The exact entry (depth 3) takes precedence over lower bound (depth 2)
        # So we expect the exact score (0.5) to be returned
        self.assertEqual(score, 0.5)
    
    def test_table_stats(self):
        """Test table statistics"""
        stats = self.table.get_stats()
        
        self.assertIn('size', stats)
        self.assertIn('hits', stats)
        self.assertIn('misses', stats)
        self.assertIn('hit_rate', stats)
        self.assertIn('age', stats)
        
        self.assertEqual(stats['hits'], 0)
        self.assertEqual(stats['misses'], 0)
        self.assertEqual(stats['hit_rate'], 0)

class TestQuiescenceSearch(unittest.TestCase):
    """Test cases for QuiescenceSearch class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
        self.quiescence = QuiescenceSearch(max_depth=3)
    
    def test_quiescence_initialization(self):
        """Test quiescence search initialization"""
        self.assertEqual(self.quiescence.max_depth, 3)
        self.assertEqual(self.quiescence.nodes_searched, 0)
    
    def test_quiescence_search(self):
        """Test quiescence search functionality"""
        score = self.quiescence.search(self.board, -1.0, 1.0, Color.WHITE)
        
        # Score should be finite
        self.assertIsInstance(score, float)
        self.assertTrue(abs(score) < float('inf'))
        
        # Should have searched some nodes
        self.assertGreater(self.quiescence.get_nodes_searched(), 0)
    
    def test_reset_stats(self):
        """Test statistics reset"""
        # Search to generate some stats
        self.quiescence.search(self.board, -1.0, 1.0, Color.WHITE)
        
        # Reset stats
        self.quiescence.reset_stats()
        
        # Stats should be reset
        self.assertEqual(self.quiescence.get_nodes_searched(), 0)

if __name__ == '__main__':
    unittest.main()