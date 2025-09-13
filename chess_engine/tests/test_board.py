"""
Unit tests for chess board module
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from chess_engine.board.board import ChessBoard, Color, PieceType, Move, Square

class TestChessBoard(unittest.TestCase):
    """Test cases for ChessBoard class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
    
    def test_initial_position(self):
        """Test initial board position"""
        # Check that board is initialized correctly
        self.assertIsNotNone(self.board.board)
        self.assertEqual(len(self.board.board), 8)
        self.assertEqual(len(self.board.board[0]), 8)
        
        # Check that white pieces are on ranks 6-7
        for rank in range(6, 8):
            for file in range(8):
                square = self.board.get_piece((file, rank))
                self.assertIsNotNone(square)
                if not square.empty:
                    self.assertEqual(square.color, Color.WHITE)
        
        # Check that black pieces are on ranks 0-1
        for rank in range(0, 2):
            for file in range(8):
                square = self.board.get_piece((file, rank))
                self.assertIsNotNone(square)
                if not square.empty:
                    self.assertEqual(square.color, Color.BLACK)
    
    def test_square_access(self):
        """Test square access methods"""
        # Test valid square access
        square = self.board.get_piece((0, 0))
        self.assertIsNotNone(square)
        
        # Test invalid square access
        invalid_square = self.board.get_piece((8, 8))
        self.assertIsNone(invalid_square)
        
        invalid_square = self.board.get_piece((-1, 0))
        self.assertIsNone(invalid_square)
    
    def test_move_creation(self):
        """Test move creation"""
        move = Move(
            from_square=(1, 6),
            to_square=(1, 4),
            piece_type=PieceType.PAWN,
            color=Color.WHITE
        )
        
        self.assertEqual(move.from_square, (1, 6))
        self.assertEqual(move.to_square, (1, 4))
        self.assertEqual(move.piece_type, PieceType.PAWN)
        self.assertEqual(move.color, Color.WHITE)
        self.assertFalse(move.is_capture)
        self.assertFalse(move.is_castling)
        self.assertFalse(move.is_en_passant)
    
    def test_square_representation(self):
        """Test square string representation"""
        # Test empty square
        empty_square = Square()
        self.assertEqual(str(empty_square), ".")
        
        # Test white pawn
        white_pawn = Square(PieceType.PAWN, Color.WHITE)
        self.assertEqual(str(white_pawn), "P")
        
        # Test black king
        black_king = Square(PieceType.KING, Color.BLACK)
        self.assertEqual(str(black_king), "k")
    
    def test_board_copy(self):
        """Test board copying"""
        board_copy = self.board.copy()
        
        # Check that it's a different object
        self.assertIsNot(board_copy, self.board)
        
        # Check that the board state is the same
        for rank in range(8):
            for file in range(8):
                original = self.board.get_piece((file, rank))
                copied = board_copy.get_piece((file, rank))
                
                if original.empty:
                    self.assertTrue(copied.empty)
                else:
                    self.assertEqual(original.piece_type, copied.piece_type)
                    self.assertEqual(original.color, copied.color)

class TestSquare(unittest.TestCase):
    """Test cases for Square class"""
    
    def test_square_creation(self):
        """Test square creation"""
        # Test empty square
        empty_square = Square()
        self.assertTrue(empty_square.empty)
        self.assertIsNone(empty_square.piece_type)
        self.assertIsNone(empty_square.color)
        
        # Test square with piece
        piece_square = Square(PieceType.QUEEN, Color.WHITE)
        self.assertFalse(piece_square.empty)
        self.assertEqual(piece_square.piece_type, PieceType.QUEEN)
        self.assertEqual(piece_square.color, Color.WHITE)

if __name__ == '__main__':
    unittest.main()