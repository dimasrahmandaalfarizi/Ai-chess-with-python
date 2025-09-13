"""
Basic Usage Examples for Chess Engine

This file demonstrates how to use the chess engine for various tasks.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine
from chess_engine.board.move_generator import MoveGenerator

def example_1_basic_board_usage():
    """Example 1: Basic board operations"""
    print("=== Example 1: Basic Board Operations ===")
    
    # Create a new chess board
    board = ChessBoard()
    print("Initial position:")
    print(board)
    print()
    
    # Get piece at a specific square
    piece = board.get_piece((0, 0))  # a8
    print(f"Piece at a8: {piece}")
    
    piece = board.get_piece((4, 7))  # e1
    print(f"Piece at e1: {piece}")
    print()

def example_2_move_generation():
    """Example 2: Move generation"""
    print("=== Example 2: Move Generation ===")
    
    board = ChessBoard()
    move_gen = MoveGenerator(board)
    
    # Generate moves for white
    white_moves = move_gen.generate_legal_moves(Color.WHITE)
    print(f"White has {len(white_moves)} legal moves")
    
    # Show first 5 moves
    print("First 5 moves for white:")
    for i, move in enumerate(white_moves[:5]):
        print(f"  {i+1}. {move}")
    print()
    
    # Generate moves for black
    black_moves = move_gen.generate_legal_moves(Color.BLACK)
    print(f"Black has {len(black_moves)} legal moves")
    print()

def example_3_position_evaluation():
    """Example 3: Position evaluation"""
    print("=== Example 3: Position Evaluation ===")
    
    board = ChessBoard()
    evaluator = EvaluationEngine()
    
    # Evaluate position for white
    score = evaluator.evaluate(board, Color.WHITE)
    print(f"Position evaluation for white: {score:.2f}")
    
    # Get detailed breakdown
    breakdown = evaluator.get_evaluation_breakdown(board, Color.WHITE)
    print("Evaluation breakdown:")
    for component, value in breakdown.items():
        print(f"  {component}: {value:.2f}")
    print()

def example_4_engine_search():
    """Example 4: Engine search"""
    print("=== Example 4: Engine Search ===")
    
    board = ChessBoard()
    engine = MinimaxEngine(max_depth=3, time_limit=2.0)
    
    print("Searching for best move...")
    best_move, score = engine.search(board)
    
    if best_move:
        print(f"Best move: {best_move}")
        print(f"Evaluation: {score:.2f}")
        
        # Show search statistics
        stats = engine.get_search_stats()
        print("Search statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        print("No legal moves found!")
    print()

def example_5_custom_position():
    """Example 5: Working with custom positions"""
    print("=== Example 5: Custom Position ===")
    
    # Create board from FEN string
    fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
    board = ChessBoard(fen)
    
    print("Position after 1.e4:")
    print(board)
    print(f"To move: {board.current_player.name}")
    
    # Evaluate the position
    evaluator = EvaluationEngine()
    score = evaluator.evaluate(board, Color.WHITE)
    print(f"Evaluation for white: {score:.2f}")
    
    # Find best move for black
    engine = MinimaxEngine(max_depth=2, time_limit=1.0)
    best_move, score = engine.search(board)
    
    if best_move:
        print(f"Best move for black: {best_move}")
        print(f"Evaluation: {score:.2f}")
    print()

def example_6_weight_tuning():
    """Example 6: Weight tuning"""
    print("=== Example 6: Weight Tuning ===")
    
    evaluator = EvaluationEngine()
    
    # Show current weights
    print("Current evaluation weights:")
    weights = evaluator.get_weights()
    for component, weight in weights.items():
        print(f"  {component}: {weight}")
    print()
    
    # Modify weights
    print("Modifying weights...")
    new_weights = {
        "material": 1.2,
        "position": 0.8,
        "king_safety": 1.5
    }
    evaluator.update_weights(new_weights)
    
    print("Updated weights:")
    updated_weights = evaluator.get_weights()
    for component, weight in updated_weights.items():
        print(f"  {component}: {weight}")
    print()

def example_7_game_simulation():
    """Example 7: Simple game simulation"""
    print("=== Example 7: Game Simulation ===")
    
    board = ChessBoard()
    engine = MinimaxEngine(max_depth=2, time_limit=1.0)
    move_gen = MoveGenerator(board)
    
    print("Starting game simulation...")
    print("Initial position:")
    print(board)
    print()
    
    # Play a few moves
    for move_num in range(1, 4):  # Play 3 moves
        print(f"Move {move_num}:")
        
        # Generate moves
        moves = move_gen.generate_legal_moves(board.current_player)
        if not moves:
            print("No legal moves - game over!")
            break
        
        # Find best move
        best_move, score = engine.search(board)
        if not best_move:
            print("Engine found no legal moves - game over!")
            break
        
        # Make the move
        if board.make_move(best_move):
            print(f"{board.current_player.name} plays: {best_move}")
            print(f"Evaluation: {score:.2f}")
            print("Position after move:")
            print(board)
            print()
        else:
            print("Failed to make move!")
            break

if __name__ == "__main__":
    print("Chess Engine - Usage Examples\n")
    
    try:
        example_1_basic_board_usage()
        example_2_move_generation()
        example_3_position_evaluation()
        example_4_engine_search()
        example_5_custom_position()
        example_6_weight_tuning()
        example_7_game_simulation()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Example failed with error: {e}")
        print("This might be due to missing dependencies or incomplete implementation.")
        print("Please check the requirements.txt and install necessary packages.")