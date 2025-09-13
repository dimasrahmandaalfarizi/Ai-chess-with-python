"""
Chess Engine Demo

This script demonstrates the basic functionality of the chess engine.
Run this to see the engine in action with a simple example.
"""

import sys
import os

# Add the chess_engine directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine
from chess_engine.board.move_generator import MoveGenerator

def demo_basic_functionality():
    """Demonstrate basic engine functionality"""
    print("=== Chess Engine Demo ===\n")
    
    # 1. Create a chess board
    print("1. Creating chess board...")
    board = ChessBoard()
    print("Initial position:")
    print(board)
    print()
    
    # 2. Generate legal moves
    print("2. Generating legal moves for white...")
    move_gen = MoveGenerator(board)
    moves = move_gen.generate_legal_moves(Color.WHITE)
    print(f"Found {len(moves)} legal moves for white")
    
    # Show first 5 moves
    print("First 5 moves:")
    for i, move in enumerate(moves[:5]):
        print(f"  {i+1}. {move}")
    print()
    
    # 3. Evaluate position
    print("3. Evaluating position...")
    evaluator = EvaluationEngine()
    score = evaluator.evaluate(board, Color.WHITE)
    print(f"Position evaluation: {score:.2f}")
    
    # Show evaluation breakdown
    breakdown = evaluator.get_evaluation_breakdown(board, Color.WHITE)
    print("Evaluation breakdown:")
    for component, value in breakdown.items():
        print(f"  {component}: {value:.2f}")
    print()
    
    # 4. Search for best move
    print("4. Searching for best move (depth 2)...")
    engine = MinimaxEngine(max_depth=2, time_limit=2.0)
    best_move, eval_score = engine.search(board)
    
    if best_move:
        print(f"Best move found: {best_move}")
        print(f"Evaluation score: {eval_score:.2f}")
        
        # Show search statistics
        stats = engine.get_search_stats()
        print("Search statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    else:
        print("No legal moves found!")
    print()
    
    # 5. Make a move and continue
    if best_move:
        print("5. Making the best move...")
        if board.make_move(best_move):
            print("Move made successfully!")
            print("New position:")
            print(board)
            print(f"Now it's {board.current_player.name}'s turn")
        else:
            print("Failed to make move!")
    print()
    
    print("=== Demo completed ===")

def demo_evaluation_components():
    """Demonstrate evaluation components"""
    print("=== Evaluation Components Demo ===\n")
    
    board = ChessBoard()
    evaluator = EvaluationEngine()
    
    print("Position evaluation components:")
    print("-" * 40)
    
    # Material evaluation
    material = evaluator._evaluate_material(board, Color.WHITE)
    print(f"Material balance: {material:.2f}")
    
    # Position evaluation
    position = evaluator._evaluate_position(board, Color.WHITE)
    print(f"Positional score: {position:.2f}")
    
    # King safety
    king_safety = evaluator._evaluate_king_safety(board, Color.WHITE)
    print(f"King safety: {king_safety:.2f}")
    
    # Pawn structure
    pawn_structure = evaluator._evaluate_pawn_structure(board, Color.WHITE)
    print(f"Pawn structure: {pawn_structure:.2f}")
    
    # Mobility
    mobility = evaluator._evaluate_mobility(board, Color.WHITE)
    print(f"Mobility: {mobility:.2f}")
    
    # Center control
    center_control = evaluator._evaluate_center_control(board, Color.WHITE)
    print(f"Center control: {center_control:.2f}")
    
    # Development
    development = evaluator._evaluate_development(board, Color.WHITE)
    print(f"Development: {development:.2f}")
    
    # Tempo
    tempo = evaluator._evaluate_tempo(board, Color.WHITE)
    print(f"Tempo: {tempo:.2f}")
    
    print("-" * 40)
    total = evaluator.evaluate(board, Color.WHITE)
    print(f"Total evaluation: {total:.2f}")
    print()

def demo_weight_tuning():
    """Demonstrate weight tuning capabilities"""
    print("=== Weight Tuning Demo ===\n")
    
    evaluator = EvaluationEngine()
    
    print("Current evaluation weights:")
    weights = evaluator.get_weights()
    for component, weight in weights.items():
        print(f"  {component}: {weight}")
    print()
    
    print("Updating weights...")
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
    
    print("Resetting weights to defaults...")
    evaluator.reset_weights()
    
    print("Reset weights:")
    reset_weights = evaluator.get_weights()
    for component, weight in reset_weights.items():
        print(f"  {component}: {weight}")
    print()

def demo_search_engine():
    """Demonstrate search engine capabilities"""
    print("=== Search Engine Demo ===\n")
    
    board = ChessBoard()
    engine = MinimaxEngine(max_depth=3, time_limit=3.0)
    
    print("Search engine configuration:")
    print(f"  Max depth: {engine.max_depth}")
    print(f"  Time limit: {engine.time_limit}s")
    print()
    
    print("Searching for best move...")
    import time
    start_time = time.time()
    
    best_move, score = engine.search(board)
    
    search_time = time.time() - start_time
    
    if best_move:
        print(f"Best move: {best_move}")
        print(f"Evaluation: {score:.2f}")
        print(f"Search time: {search_time:.2f}s")
        
        stats = engine.get_search_stats()
        print(f"Nodes searched: {stats['nodes_searched']}")
        print(f"Nodes per second: {stats['nodes_searched'] / search_time:.0f}")
        print(f"Alpha-beta cutoffs: {stats['cutoffs']}")
        print(f"Transposition hits: {stats['transposition_hits']}")
    else:
        print("No legal moves found!")
    print()

if __name__ == "__main__":
    print("Chess Engine - Comprehensive Demo\n")
    print("This demo showcases the main features of the chess engine.\n")
    
    try:
        # Run all demos
        demo_basic_functionality()
        demo_evaluation_components()
        demo_weight_tuning()
        demo_search_engine()
        
        print("All demos completed successfully!")
        print("\nTo run the engine interactively, use: python main.py play")
        print("To run the UCI interface, use: python main.py uci")
        print("To run tests, use: python main.py test")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        print("This might be due to missing dependencies or incomplete implementation.")
        print("Please check the requirements.txt and install necessary packages.")