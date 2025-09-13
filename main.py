"""
Chess Engine - Main entry point

This is the main entry point for the chess engine with CLI interface.
Supports multiple modes: engine play, training, tuning, and UCI interface.
"""

import argparse
import sys
import os
from typing import Optional

# Add the chess_engine directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.eval.evaluation import EvaluationEngine
from chess_engine.train.tuner import WeightTuner
from chess_engine.train.dataset import ChessDataset
from chess_engine.train.trainer import NeuralTrainer
from chess_engine.uci.uci_interface import UCIInterface

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Chess Engine - A modular chess engine with training capabilities")
    
    # Main mode selection
    parser.add_argument("mode", choices=["play", "uci", "train", "tune", "test"], 
                       help="Mode to run the engine in")
    
    # Common options
    parser.add_argument("--depth", type=int, default=4, help="Search depth")
    parser.add_argument("--time", type=float, default=5.0, help="Time limit per move (seconds)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    # Training options
    parser.add_argument("--data-dir", default="data", help="Directory containing training data")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs")
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size for training")
    
    # Tuning options
    parser.add_argument("--generations", type=int, default=100, help="Number of generations for tuning")
    parser.add_argument("--population-size", type=int, default=50, help="Population size for genetic algorithm")
    
    args = parser.parse_args()
    
    if args.mode == "play":
        play_mode(args)
    elif args.mode == "uci":
        uci_mode(args)
    elif args.mode == "train":
        train_mode(args)
    elif args.mode == "tune":
        tune_mode(args)
    elif args.mode == "test":
        test_mode(args)

def play_mode(args):
    """Interactive play mode"""
    print("Chess Engine - Play Mode")
    print("Commands: move (e.g., e2e4), quit, new, eval, help")
    print()
    
    board = ChessBoard()
    engine = MinimaxEngine(max_depth=args.depth, time_limit=args.time)
    evaluator = EvaluationEngine()
    
    while True:
        print(f"\nCurrent position (Move {len(board.move_history) + 1}):")
        print(board)
        print(f"To move: {board.current_player.name}")
        
        # Check for game end
        if board.is_checkmate(board.current_player):
            print(f"Checkmate! {board.current_player.name} loses!")
            break
        elif board.is_stalemate(board.current_player):
            print("Stalemate! Game is a draw!")
            break
        
        command = input("\nEnter command: ").strip().lower()
        
        if command == "quit":
            break
        elif command == "new":
            board = ChessBoard()
            print("New game started!")
        elif command == "eval":
            score = evaluator.evaluate(board, board.current_player)
            print(f"Position evaluation: {score:.2f}")
        elif command == "help":
            print_help()
        elif command.startswith("move ") or len(command) == 4:
            # Parse move
            if command.startswith("move "):
                move_str = command[5:]
            else:
                move_str = command
            
            # TODO: Implement move parsing and validation
            print(f"Move {move_str} not implemented yet")
        elif command == "engine":
            # Let engine make a move
            print("Engine is thinking...")
            best_move, score = engine.search(board)
            if best_move:
                print(f"Engine plays: {best_move}")
                board.make_move(best_move)
            else:
                print("Engine has no legal moves!")
        else:
            print("Unknown command. Type 'help' for available commands.")

def uci_mode(args):
    """UCI interface mode"""
    print("Starting UCI interface...")
    uci = UCIInterface()
    uci.run()

def train_mode(args):
    """Training mode"""
    print("Chess Engine - Training Mode")
    print(f"Data directory: {args.data_dir}")
    print(f"Epochs: {args.epochs}")
    print(f"Batch size: {args.batch_size}")
    print()
    
    # Load dataset
    dataset = ChessDataset(args.data_dir)
    
    # Load PGN files if they exist
    pgn_files = [f for f in os.listdir(args.data_dir) if f.endswith('.pgn')]
    if pgn_files:
        print(f"Found {len(pgn_files)} PGN files")
        for pgn_file in pgn_files:
            dataset.load_pgn_file(pgn_file)
    else:
        print("No PGN files found in data directory")
        print("Please add some PGN files to train the neural network")
        return
    
    # Extract positions
    positions = dataset.extract_positions(dataset.games)
    if not positions:
        print("No positions extracted from games")
        return
    
    # Train neural network
    trainer = NeuralTrainer()
    print("Starting neural network training...")
    
    history = trainer.train(dataset, epochs=args.epochs, batch_size=args.batch_size)
    
    # Save trained model
    model_path = os.path.join(args.data_dir, "trained_model.pth")
    trainer.save_model(model_path)
    
    print(f"Training completed! Model saved to {model_path}")

def tune_mode(args):
    """Weight tuning mode"""
    print("Chess Engine - Weight Tuning Mode")
    print(f"Generations: {args.generations}")
    print(f"Population size: {args.population_size}")
    print()
    
    # Initialize tuner
    tuner = WeightTuner(population_size=args.population_size)
    
    # Initialize population
    tuner.initialize_population()
    
    # Run evolution
    print("Starting weight optimization...")
    tuner.evolve(num_generations=args.generations)
    
    # Save best weights
    best_weights_path = os.path.join(args.data_dir, "best_weights.json")
    tuner.save_best_weights(best_weights_path)
    
    # Print results
    stats = tuner.get_population_stats()
    print(f"\nOptimization completed!")
    print(f"Best fitness: {stats['best_fitness']:.3f}")
    print(f"Best win rate: {stats['best_win_rate']:.3f}")
    print(f"Best weights saved to {best_weights_path}")

def test_mode(args):
    """Test mode"""
    print("Chess Engine - Test Mode")
    print("Running basic functionality tests...")
    print()
    
    # Test board creation
    print("Testing board creation...")
    board = ChessBoard()
    print("✓ Board created successfully")
    
    # Test move generation
    print("Testing move generation...")
    from chess_engine.board.move_generator import MoveGenerator
    move_gen = MoveGenerator(board)
    moves = move_gen.generate_legal_moves(Color.WHITE)
    print(f"✓ Generated {len(moves)} legal moves for white")
    
    # Test evaluation
    print("Testing position evaluation...")
    evaluator = EvaluationEngine()
    score = evaluator.evaluate(board, Color.WHITE)
    print(f"✓ Position evaluation: {score:.2f}")
    
    # Test search
    print("Testing search algorithm...")
    engine = MinimaxEngine(max_depth=2, time_limit=1.0)
    best_move, eval_score = engine.search(board)
    if best_move:
        print(f"✓ Search completed: {best_move} (score: {eval_score:.2f})")
    else:
        print("✓ Search completed: No legal moves")
    
    print("\nAll basic tests passed!")

def print_help():
    """Print help information"""
    print("Available commands:")
    print("  move <move>  - Make a move (e.g., 'move e2e4' or 'e2e4')")
    print("  engine       - Let the engine make a move")
    print("  eval         - Show position evaluation")
    print("  new          - Start a new game")
    print("  quit         - Quit the program")
    print("  help         - Show this help")

if __name__ == "__main__":
    main()