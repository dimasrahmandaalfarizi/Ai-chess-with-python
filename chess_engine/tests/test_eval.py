"""
Unit tests for evaluation module
"""

import unittest
import sys
import os
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.eval.evaluation import EvaluationEngine

class TestEvaluationEngine(unittest.TestCase):
    """Test cases for EvaluationEngine class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
        self.evaluator = EvaluationEngine()
    
    def test_evaluator_initialization(self):
        """Test evaluator initialization"""
        self.assertIsNotNone(self.evaluator.weights)
        self.assertIsNotNone(self.evaluator.material_values)
        self.assertIsNotNone(self.evaluator.piece_square_tables)
    
    def test_material_evaluation(self):
        """Test material evaluation"""
        score = self.evaluator._evaluate_material(self.board, Color.WHITE)
        
        # Initial position should have equal material
        self.assertAlmostEqual(score, 0.0, places=1)
        
        # Score should be finite
        self.assertTrue(abs(score) < float('inf'))
    
    def test_position_evaluation(self):
        """Test position evaluation"""
        score = self.evaluator._evaluate_position(self.board, Color.WHITE)
        
        # Score should be finite
        self.assertIsInstance(score, float)
        self.assertTrue(abs(score) < float('inf'))
    
    def test_full_evaluation(self):
        """Test full position evaluation"""
        score = self.evaluator.evaluate(self.board, Color.WHITE)
        
        # Score should be finite
        self.assertIsInstance(score, float)
        self.assertTrue(abs(score) < float('inf'))
    
    def test_evaluation_breakdown(self):
        """Test evaluation breakdown"""
        breakdown = self.evaluator.get_evaluation_breakdown(self.board, Color.WHITE)
        
        # Should contain all evaluation components
        expected_components = [
            "material", "position", "king_safety", "pawn_structure",
            "mobility", "center_control", "development", "tempo"
        ]
        
        for component in expected_components:
            self.assertIn(component, breakdown)
            self.assertIsInstance(breakdown[component], float)
    
    def test_weights_management(self):
        """Test weights management"""
        # Test getting weights
        weights = self.evaluator.get_weights()
        self.assertIsInstance(weights, dict)
        self.assertIn("material", weights)
        
        # Test updating weights
        new_weights = {"material": 1.5, "position": 0.8}
        self.evaluator.update_weights(new_weights)
        
        updated_weights = self.evaluator.get_weights()
        self.assertEqual(updated_weights["material"], 1.5)
        self.assertEqual(updated_weights["position"], 0.8)
        
        # Other weights should remain unchanged
        self.assertEqual(updated_weights["king_safety"], 1.0)
    
    def test_weights_file_operations(self):
        """Test weights file operations"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test saving weights
            self.evaluator.weights_file = temp_file
            self.evaluator._save_weights({"test": 1.0})
            
            # Test loading weights
            loaded_weights = self.evaluator._load_weights()
            self.assertEqual(loaded_weights["test"], 1.0)
            
        finally:
            # Clean up
            os.unlink(temp_file)
    
    def test_reset_weights(self):
        """Test weights reset"""
        # Modify weights
        self.evaluator.update_weights({"material": 2.0, "position": 0.5})
        
        # Reset weights
        self.evaluator.reset_weights()
        
        # Check that weights are reset to defaults
        weights = self.evaluator.get_weights()
        self.assertEqual(weights["material"], 1.0)
        self.assertEqual(weights["position"], 1.0)
        self.assertEqual(weights["king_safety"], 1.0)
    
    def test_piece_square_tables(self):
        """Test piece-square tables"""
        tables = self.evaluator.piece_square_tables
        
        # Check that all piece types have tables
        from chess_engine.board.board import PieceType
        for piece_type in PieceType:
            self.assertIn(piece_type, tables)
            self.assertEqual(len(tables[piece_type]), 8)
            self.assertEqual(len(tables[piece_type][0]), 8)
    
    def test_material_values(self):
        """Test material values"""
        values = self.evaluator.material_values
        
        # Check that all piece types have values
        from chess_engine.board.board import PieceType
        for piece_type in PieceType:
            self.assertIn(piece_type, values)
            self.assertGreater(values[piece_type], 0)
        
        # Check relative values make sense
        self.assertGreater(values[PieceType.QUEEN], values[PieceType.ROOK])
        self.assertGreater(values[PieceType.ROOK], values[PieceType.BISHOP])
        self.assertGreater(values[PieceType.BISHOP], values[PieceType.PAWN])
    
    def test_evaluation_consistency(self):
        """Test evaluation consistency"""
        # Same position should give same evaluation
        score1 = self.evaluator.evaluate(self.board, Color.WHITE)
        score2 = self.evaluator.evaluate(self.board, Color.WHITE)
        self.assertEqual(score1, score2)
        
        # Evaluation for opposite colors should be opposite
        score_white = self.evaluator.evaluate(self.board, Color.WHITE)
        score_black = self.evaluator.evaluate(self.board, Color.BLACK)
        self.assertAlmostEqual(score_white, -score_black, places=1)

if __name__ == '__main__':
    unittest.main()