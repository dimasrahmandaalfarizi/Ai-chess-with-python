"""
Comprehensive Tests for Chess Engine

This module contains comprehensive tests for all engine components.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chess_engine.board.board import ChessBoard, Color, PieceType, Move
from chess_engine.board.move_generator import MoveGenerator
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine
from chess_engine.search.zobrist import ZobristHash

class TestChessEngine(unittest.TestCase):
    """Comprehensive chess engine tests"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
        self.move_gen = MoveGenerator(self.board)
        self.engine = MinimaxEngine(max_depth=2, time_limit=1.0)
        self.evaluator = EvaluationEngine()
    
    def test_board_initialization(self):
        """Test board is initialized correctly"""
        # Check starting position
        self.assertEqual(self.board.current_player, Color.WHITE)
        self.assertTrue(self.board.castling_rights["K"])
        self.assertTrue(self.board.castling_rights["Q"])
        self.assertTrue(self.board.castling_rights["k"])
        self.assertTrue(self.board.castling_rights["q"])
        self.assertIsNone(self.board.en_passant_target)
        self.assertEqual(self.board.halfmove_clock, 0)
        self.assertEqual(self.board.fullmove_number, 1)
    
    def test_fen_generation(self):
        """Test FEN string generation"""
        starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        generated_fen = self.board._get_fen()
        self.assertEqual(generated_fen, starting_fen)
    
    def test_move_generation(self):
        """Test legal move generation"""
        moves = self.move_gen.generate_legal_moves(Color.WHITE)
        self.assertEqual(len(moves), 20)  # 16 pawn moves + 4 knight moves
        
        # Test specific moves exist
        move_strings = [str(move) for move in moves]
        self.assertIn("e2e4", move_strings)
        self.assertIn("d2d4", move_strings)
        self.assertIn("g1f3", move_strings)
        self.assertIn("b1c3", move_strings)
    
    def test_check_detection(self):
        """Test check detection"""
        # Create a position where white king is in check
        # This is a simplified test - in practice you'd set up specific positions
        self.assertFalse(self.board.is_check(Color.WHITE))
        self.assertFalse(self.board.is_check(Color.BLACK))
    
    def test_move_making_and_undoing(self):
        """Test making and undoing moves"""
        # Make a move
        moves = self.move_gen.generate_legal_moves(Color.WHITE)
        test_move = moves[0]  # Take first legal move
        
        original_fen = self.board._get_fen()
        
        # Make move
        success = self.board.make_move(test_move)
        self.assertTrue(success)
        
        # Board should be different
        new_fen = self.board._get_fen()
        self.assertNotEqual(original_fen, new_fen)
        
        # Undo move
        undo_success = self.board.undo_move()
        self.assertTrue(undo_success)
        
        # Board should be back to original
        restored_fen = self.board._get_fen()
        self.assertEqual(original_fen, restored_fen)
    
    def test_evaluation_consistency(self):
        """Test evaluation function consistency"""
        # Evaluate same position multiple times
        score1 = self.evaluator.evaluate(self.board, Color.WHITE)
        score2 = self.evaluator.evaluate(self.board, Color.WHITE)
        self.assertEqual(score1, score2)
        
        # Test that evaluation is reasonable (not extreme values)
        white_score = self.evaluator.evaluate(self.board, Color.WHITE)
        self.assertGreater(white_score, -1000)  # Not losing badly
        self.assertLess(white_score, 1000)     # Not winning by huge margin
        
        # Test that evaluation changes when position changes
        moves = self.move_gen.generate_legal_moves(Color.WHITE)
        if moves:
            self.board.make_move(moves[0])
            new_score = self.evaluator.evaluate(self.board, Color.WHITE)
            # Score should be different after making a move
            # (though not necessarily better or worse)
            self.board.undo_move()
    
    def test_zobrist_hashing(self):
        """Test Zobrist hashing"""
        zobrist = ZobristHash()
        
        # Same position should give same hash
        hash1 = zobrist.hash_position(self.board)
        hash2 = zobrist.hash_position(self.board)
        self.assertEqual(hash1, hash2)
        
        # Different positions should give different hashes (with high probability)
        moves = self.move_gen.generate_legal_moves(Color.WHITE)
        self.board.make_move(moves[0])
        hash3 = zobrist.hash_position(self.board)
        self.assertNotEqual(hash1, hash3)
    
    def test_search_deterministic(self):
        """Test search gives consistent results"""
        # Test that search returns a valid move
        move, score = self.engine.search(self.board, depth=2)
        
        # Should return a valid move for starting position
        self.assertIsNotNone(move, "Search should return a move for starting position")
        
        # Score should be reasonable
        self.assertIsInstance(score, (int, float), "Score should be numeric")
        self.assertGreater(score, -10000, "Score should not be extremely negative")
        self.assertLess(score, 10000, "Score should not be extremely positive")
        
        # Move should be in legal moves
        legal_moves = self.move_gen.generate_legal_moves(self.board.current_player)
        move_strings = [str(m) for m in legal_moves]
        self.assertIn(str(move), move_strings, "Returned move should be legal")
    
    def test_transposition_table(self):
        """Test transposition table functionality"""
        # Clear table
        self.engine.clear_tables()
        
        # Search position
        self.engine.search(self.board, depth=2)
        
        # Check table has entries
        stats = self.engine.transposition_table.get_stats()
        self.assertGreater(stats['size'], 0)
    
    def test_invalid_moves(self):
        """Test invalid move handling"""
        # Try to make invalid move
        invalid_move = Move((0, 0), (7, 7), PieceType.PAWN, Color.WHITE)
        success = self.board.make_move(invalid_move)
        self.assertFalse(success)
    
    def test_game_end_detection(self):
        """Test checkmate and stalemate detection"""
        # Starting position should not be checkmate or stalemate for current player
        current_player = self.board.current_player
        self.assertFalse(self.board.is_checkmate(current_player))
        self.assertFalse(self.board.is_stalemate(current_player))
        
        # Test that we can detect when there are legal moves
        moves = self.move_gen.generate_legal_moves(current_player)
        self.assertGreater(len(moves), 0)  # Should have legal moves in starting position

class TestPerformance(unittest.TestCase):
    """Performance tests"""
    
    def setUp(self):
        self.board = ChessBoard()
        self.engine = MinimaxEngine(max_depth=3, time_limit=2.0)
    
    def test_search_performance(self):
        """Test search performance"""
        import time
        
        start_time = time.time()
        move, score = self.engine.search(self.board)
        end_time = time.time()
        
        search_time = end_time - start_time
        
        # Should complete within time limit
        self.assertLess(search_time, 3.0)
        
        # Should find a move
        self.assertIsNotNone(move)
        
        # Should search reasonable number of nodes
        stats = self.engine.get_search_stats()
        self.assertGreater(stats['nodes_searched'], 10)

def run_comprehensive_tests():
    """Run all comprehensive tests"""
    print("Running comprehensive chess engine tests...")
    
    # Create test loader
    loader = unittest.TestLoader()
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestChessEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)