"""
Training Example for Chess Engine

This file demonstrates how to train the chess engine using different methods.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chess_engine.train.tuner import WeightTuner
from chess_engine.train.dataset import ChessDataset
from chess_engine.train.trainer import NeuralTrainer
from chess_engine.eval.evaluation import EvaluationEngine

def example_weight_tuning():
    """Example: Weight tuning using genetic algorithm"""
    print("=== Weight Tuning Example ===")
    
    # Initialize tuner
    tuner = WeightTuner(population_size=20, mutation_rate=0.1)
    
    print("Initializing population...")
    tuner.initialize_population()
    
    print("Starting weight optimization...")
    print("(This will run for a few generations as a demo)")
    
    # Run evolution for a few generations
    tuner.evolve(num_generations=5, games_per_evaluation=5)
    
    # Get results
    stats = tuner.get_population_stats()
    print(f"\nOptimization completed!")
    print(f"Best fitness: {stats['best_fitness']:.3f}")
    print(f"Best win rate: {stats['best_win_rate']:.3f}")
    
    # Show best weights
    if tuner.best_individual:
        print("\nBest weights found:")
        for component, weight in tuner.best_individual.weights.items():
            print(f"  {component}: {weight:.3f}")
    print()

def example_dataset_loading():
    """Example: Loading and processing chess dataset"""
    print("=== Dataset Loading Example ===")
    
    # Create dataset
    dataset = ChessDataset("data")
    
    print("Dataset created. You can add PGN files to the 'data' directory.")
    print("For this demo, we'll show the dataset structure.")
    
    # Show dataset stats
    stats = dataset.get_dataset_stats()
    print(f"Dataset statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Example of creating sample data
    print("Creating sample game data...")
    
    # This would normally load from PGN files
    # For demo purposes, we'll show the structure
    print("To load PGN files, use:")
    print("  dataset.load_pgn_file('your_game.pgn')")
    print("  positions = dataset.extract_positions(dataset.games)")
    print()

def example_neural_training():
    """Example: Neural network training"""
    print("=== Neural Network Training Example ===")
    
    # Initialize trainer
    trainer = NeuralTrainer(input_size=64, hidden_sizes=[128, 64])
    
    print("Neural trainer initialized:")
    model_info = trainer.get_model_info()
    for key, value in model_info.items():
        print(f"  {key}: {value}")
    print()
    
    # Create sample dataset
    dataset = ChessDataset("data")
    
    print("To train the neural network:")
    print("1. Add PGN files to the 'data' directory")
    print("2. Run: dataset.load_pgn_file('your_game.pgn')")
    print("3. Run: positions = dataset.extract_positions(dataset.games)")
    print("4. Run: trainer.train(dataset, epochs=100)")
    print()
    
    # Show training structure
    print("Training structure:")
    print("- Input: 64 features (8x8 board representation)")
    print("- Hidden layers: [128, 64] neurons")
    print("- Output: 1 value (position evaluation)")
    print("- Loss function: MSE (Mean Squared Error)")
    print("- Optimizer: Adam")
    print()

def example_evaluation_comparison():
    """Example: Comparing different evaluation methods"""
    print("=== Evaluation Comparison Example ===")
    
    from chess_engine.board.board import ChessBoard, Color
    
    # Create test position
    board = ChessBoard()
    
    # Test different evaluation engines
    evaluator1 = EvaluationEngine()
    evaluator2 = EvaluationEngine()
    
    # Modify weights for comparison
    evaluator2.update_weights({
        "material": 1.5,
        "position": 0.5,
        "king_safety": 2.0
    })
    
    # Evaluate position with both engines
    score1 = evaluator1.evaluate(board, Color.WHITE)
    score2 = evaluator2.evaluate(board, Color.WHITE)
    
    print(f"Evaluation with default weights: {score1:.2f}")
    print(f"Evaluation with modified weights: {score2:.2f}")
    print(f"Difference: {abs(score2 - score1):.2f}")
    print()
    
    # Show weight differences
    weights1 = evaluator1.get_weights()
    weights2 = evaluator2.get_weights()
    
    print("Weight comparison:")
    for component in weights1:
        diff = weights2[component] - weights1[component]
        print(f"  {component}: {weights1[component]:.1f} -> {weights2[component]:.1f} ({diff:+.1f})")
    print()

def example_self_play():
    """Example: Self-play for training"""
    print("=== Self-Play Example ===")
    
    from chess_engine.board.board import ChessBoard
    from chess_engine.search.minimax import MinimaxEngine
    
    print("Self-play simulation:")
    print("(This would normally be used for generating training data)")
    
    # Create two engines with different evaluation weights
    engine1 = MinimaxEngine(max_depth=2, time_limit=1.0)
    engine2 = MinimaxEngine(max_depth=2, time_limit=1.0)
    
    # Modify evaluation weights for engine2
    engine2.evaluation_engine.update_weights({
        "material": 1.2,
        "position": 0.8
    })
    
    print("Engine 1: Default weights")
    print("Engine 2: Modified weights")
    print()
    
    # Simulate a few moves
    board = ChessBoard()
    print("Starting position:")
    print(board)
    print()
    
    for move_num in range(1, 4):
        print(f"Move {move_num}:")
        
        # Choose engine based on current player
        if board.current_player == Color.WHITE:
            engine = engine1
            engine_name = "Engine 1"
        else:
            engine = engine2
            engine_name = "Engine 2"
        
        # Find best move
        best_move, score = engine.search(board)
        
        if best_move and board.make_move(best_move):
            print(f"{engine_name} plays: {best_move} (eval: {score:.2f})")
        else:
            print("Game over!")
            break
    
    print("\nSelf-play completed!")
    print("In a real implementation, this would generate training data")
    print("by recording positions and their evaluations.")
    print()

if __name__ == "__main__":
    print("Chess Engine - Training Examples\n")
    
    try:
        example_weight_tuning()
        example_dataset_loading()
        example_neural_training()
        example_evaluation_comparison()
        example_self_play()
        
        print("All training examples completed!")
        print("\nTo run actual training:")
        print("1. Add PGN files to the 'data' directory")
        print("2. Run: python main.py train --epochs 100")
        print("3. Run: python main.py tune --generations 50")
        
    except Exception as e:
        print(f"Example failed with error: {e}")
        print("This might be due to missing dependencies or incomplete implementation.")
        print("Please check the requirements.txt and install necessary packages.")