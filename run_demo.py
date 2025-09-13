"""
Demo Runner for Chess Engine

This script runs various demos to showcase the engine's capabilities.
"""

import sys
import os
import argparse

# Add the chess_engine directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

def run_basic_demo():
    """Run basic functionality demo"""
    print("Running Basic Functionality Demo...")
    print("=" * 50)
    
    try:
        from demo import demo_basic_functionality
        demo_basic_functionality()
        return True
    except Exception as e:
        print(f"Demo failed: {e}")
        return False

def run_usage_examples():
    """Run usage examples"""
    print("Running Usage Examples...")
    print("=" * 50)
    
    try:
        from examples.basic_usage import (
            example_1_basic_board_usage,
            example_2_move_generation,
            example_3_position_evaluation,
            example_4_engine_search,
            example_5_custom_position,
            example_6_weight_tuning,
            example_7_game_simulation
        )
        
        examples = [
            example_1_basic_board_usage,
            example_2_move_generation,
            example_3_position_evaluation,
            example_4_engine_search,
            example_5_custom_position,
            example_6_weight_tuning,
            example_7_game_simulation
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n--- Example {i} ---")
            example()
        
        return True
    except Exception as e:
        print(f"Usage examples failed: {e}")
        return False

def run_training_examples():
    """Run training examples"""
    print("Running Training Examples...")
    print("=" * 50)
    
    try:
        from examples.training_example import (
            example_weight_tuning,
            example_dataset_loading,
            example_neural_training,
            example_evaluation_comparison,
            example_self_play
        )
        
        examples = [
            example_weight_tuning,
            example_dataset_loading,
            example_neural_training,
            example_evaluation_comparison,
            example_self_play
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n--- Training Example {i} ---")
            example()
        
        return True
    except Exception as e:
        print(f"Training examples failed: {e}")
        return False

def run_uci_examples():
    """Run UCI examples"""
    print("Running UCI Examples...")
    print("=" * 50)
    
    try:
        from examples.uci_example import (
            example_uci_commands,
            example_uci_options,
            example_uci_protocol_flow,
            example_uci_gui_integration,
            example_uci_debugging
        )
        
        examples = [
            example_uci_commands,
            example_uci_options,
            example_uci_protocol_flow,
            example_uci_gui_integration,
            example_uci_debugging
        ]
        
        for i, example in enumerate(examples, 1):
            print(f"\n--- UCI Example {i} ---")
            example()
        
        return True
    except Exception as e:
        print(f"UCI examples failed: {e}")
        return False

def run_quick_test():
    """Run a quick functionality test"""
    print("Running Quick Test...")
    print("=" * 50)
    
    try:
        from chess_engine.board.board import ChessBoard, Color
        from chess_engine.search.minimax import MinimaxEngine
        from chess_engine.eval.evaluation import EvaluationEngine
        from chess_engine.board.move_generator import MoveGenerator
        
        # Test board creation
        print("1. Testing board creation...")
        board = ChessBoard()
        print("   ✓ Board created successfully")
        
        # Test move generation
        print("2. Testing move generation...")
        move_gen = MoveGenerator(board)
        moves = move_gen.generate_legal_moves(Color.WHITE)
        print(f"   ✓ Generated {len(moves)} legal moves")
        
        # Test evaluation
        print("3. Testing position evaluation...")
        evaluator = EvaluationEngine()
        score = evaluator.evaluate(board, Color.WHITE)
        print(f"   ✓ Position evaluation: {score:.2f}")
        
        # Test search
        print("4. Testing search algorithm...")
        engine = MinimaxEngine(max_depth=2, time_limit=1.0)
        best_move, eval_score = engine.search(board)
        if best_move:
            print(f"   ✓ Search completed: {best_move} (score: {eval_score:.2f})")
        else:
            print("   ✓ Search completed: No legal moves")
        
        print("\n✅ Quick test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        return False

def main():
    """Main demo runner"""
    parser = argparse.ArgumentParser(description="Run Chess Engine demos")
    parser.add_argument("--demo", choices=["basic", "usage", "training", "uci", "quick", "all"], 
                       default="all", help="Demo to run")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    print("Chess Engine - Demo Runner")
    print("=" * 50)
    print()
    
    success = True
    
    if args.demo == "all":
        demos = [
            ("Quick Test", run_quick_test),
            ("Basic Demo", run_basic_demo),
            ("Usage Examples", run_usage_examples),
            ("Training Examples", run_training_examples),
            ("UCI Examples", run_uci_examples)
        ]
        
        for name, demo_func in demos:
            print(f"\n{'='*20} {name} {'='*20}")
            if not demo_func():
                success = False
                print(f"❌ {name} failed!")
            else:
                print(f"✅ {name} completed!")
    
    elif args.demo == "basic":
        success = run_basic_demo()
    elif args.demo == "usage":
        success = run_usage_examples()
    elif args.demo == "training":
        success = run_training_examples()
    elif args.demo == "uci":
        success = run_uci_examples()
    elif args.demo == "quick":
        success = run_quick_test()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All demos completed successfully!")
        print("\nTo run the engine interactively:")
        print("  python main.py play")
        print("\nTo run the UCI interface:")
        print("  python main.py uci")
        print("\nTo run tests:")
        print("  python run_tests.py")
    else:
        print("❌ Some demos failed!")
        print("Check the error messages above for details.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)