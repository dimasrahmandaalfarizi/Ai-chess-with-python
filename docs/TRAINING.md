# Training Guide

This guide covers the machine learning and optimization features of the Chess Engine.

## Table of Contents

- [Overview](#overview)
- [Data Preparation](#data-preparation)
- [Neural Network Training](#neural-network-training)
- [Weight Tuning](#weight-tuning)
- [Self-Play Training](#self-play-training)
- [Advanced Techniques](#advanced-techniques)
- [Performance Optimization](#performance-optimization)

## Overview

The Chess Engine supports several training and optimization methods:

1. **Neural Network Training** - Train evaluation functions using game data
2. **Weight Tuning** - Optimize evaluation parameters using genetic algorithms
3. **Self-Play Training** - Generate training data through engine vs engine games
4. **Reinforcement Learning** - Learn from game outcomes and rewards

## Data Preparation

### PGN File Format

The engine expects PGN (Portable Game Notation) files containing chess games:

```
[Event "World Championship"]
[Site "New York, NY"]
[Date "2023.01.01"]
[Round "1"]
[White "Player1"]
[Black "Player2"]
[Result "1-0"]

1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Ba4 Nf6 5. O-O Be7 6. Re1 b5 7. Bb3 d6 8. c3 O-O 9. h3 Nb8 10. d4 Nbd7 11. c4 c6 12. cxb5 axb5 13. Nc3 Bb7 14. Bg5 b4 15. Nb1 h6 16. Bh4 c5 17. dxe5 Nxe4 18. Bxe7 Qxe7 19. exd6 Qf6 20. Nbd2 Nxd6 21. Nc4 Nxc4 22. Bxc4 Nb6 23. Ne5 Rae8 24. Bxf7+ Rxf7 25. Nxf7 Rxe1+ 26. Qxe1 Kxf7 27. Qe3 Qg5 28. Qxg5 hxg5 29. b3 Ke6 30. a3 Kd6 31. axb4 cxb4 32. Ra5 Nd5 33. f3 Bc8 34. Kf2 Bf5 35. Ra7 g6 36. Ra6+ Kc5 37. Ke1 Nf4 38. g3 Nxh3 39. Kd2 Kb5 40. Rd6 Kc5 41. Ra6 Nf2 42. g4 Bd3 43. Re6 1-0
```

### Loading PGN Data

```python
from chess_engine.train.dataset import ChessDataset

# Create dataset
dataset = ChessDataset("data")

# Load PGN files
dataset.load_pgn_file("games.pgn")
dataset.load_pgn_file("tournament.pgn")

# Extract positions
positions = dataset.extract_positions(dataset.games, max_positions_per_game=50)
```

### Data Preprocessing

```python
# Filter positions by game phase
opening_positions = [p for p in positions if p.move_number <= 20]
middlegame_positions = [p for p in positions if 20 < p.move_number <= 40]
endgame_positions = [p for p in positions if p.move_number > 40]

# Filter by evaluation range
tactical_positions = [p for p in positions if abs(p.evaluation) > 1.0]
```

## Neural Network Training

### Basic Training

```python
from chess_engine.train.trainer import NeuralTrainer

# Create trainer
trainer = NeuralTrainer(
    input_size=64,  # 8x8 board representation
    hidden_sizes=[256, 128, 64],
    learning_rate=0.001
)

# Train the model
history = trainer.train(
    dataset=dataset,
    epochs=100,
    batch_size=32,
    validation_split=0.2
)
```

### Advanced Training Configuration

```python
# Custom network architecture
trainer = NeuralTrainer(
    input_size=64,
    hidden_sizes=[512, 256, 128, 64],
    learning_rate=0.0001,
    device="cuda"  # Use GPU if available
)

# Training with custom parameters
history = trainer.train(
    dataset=dataset,
    epochs=200,
    batch_size=64,
    validation_split=0.1,
    save_path="models/trained_model.pth"
)
```

### Training Monitoring

```python
# Plot training history
trainer.plot_training_history("training_plot.png")

# Get model information
info = trainer.get_model_info()
print(f"Total parameters: {info['total_parameters']}")
print(f"Trainable parameters: {info['trainable_parameters']}")
```

### Using Trained Models

```python
# Load trained model
trainer.load_model("models/trained_model.pth")

# Evaluate position
score = trainer.evaluate_position("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
print(f"Neural network evaluation: {score}")
```

## Weight Tuning

### Genetic Algorithm Tuning

```python
from chess_engine.train.tuner import WeightTuner

# Create tuner
tuner = WeightTuner(
    population_size=50,
    mutation_rate=0.1,
    crossover_rate=0.8,
    elite_size=5
)

# Initialize population
tuner.initialize_population()

# Run evolution
tuner.evolve(
    num_generations=100,
    games_per_evaluation=10
)

# Get best weights
best_weights = tuner.best_individual.weights
print(f"Best weights: {best_weights}")
```

### Hill Climbing Optimization

```python
# Alternative optimization method
initial_weights = {
    "material": 1.0,
    "position": 1.0,
    "king_safety": 1.0,
    "pawn_structure": 1.0,
    "mobility": 1.0,
    "center_control": 1.0,
    "development": 1.0,
    "tempo": 1.0
}

optimized_weights = tuner.hill_climbing(
    initial_weights=initial_weights,
    max_iterations=1000,
    step_size=0.1
)
```

### Custom Fitness Function

```python
def custom_fitness(individual, opponent_weights, num_games=10):
    """Custom fitness function for weight evaluation"""
    wins = 0
    losses = 0
    draws = 0
    
    for _ in range(num_games):
        result = play_game(individual.weights, opponent_weights)
        
        if result == 1:
            wins += 1
        elif result == -1:
            losses += 1
        else:
            draws += 1
    
    # Custom fitness calculation
    fitness = (wins + 0.5 * draws) / num_games
    
    # Bonus for balanced weights
    weight_balance = 1.0 - sum(abs(w - 1.0) for w in individual.weights.values()) / len(individual.weights)
    fitness += 0.1 * weight_balance
    
    return fitness

# Use custom fitness function
tuner.evaluate_fitness = custom_fitness
```

## Self-Play Training

### Basic Self-Play

```python
from chess_engine.board.board import ChessBoard
from chess_engine.search.minimax import MinimaxEngine

def self_play_game(engine1, engine2, max_moves=100):
    """Play a game between two engines"""
    board = ChessBoard()
    moves = []
    
    for move_num in range(max_moves):
        if board.is_checkmate(board.current_player):
            break
        if board.is_stalemate(board.current_player):
            break
        
        # Choose engine based on current player
        if board.current_player == Color.WHITE:
            engine = engine1
        else:
            engine = engine2
        
        # Get best move
        best_move, score = engine.search(board)
        if not best_move:
            break
        
        # Make move
        board.make_move(best_move)
        moves.append(best_move)
    
    return moves, board

# Create engines with different weights
engine1 = MinimaxEngine(max_depth=3)
engine2 = MinimaxEngine(max_depth=3)

# Modify engine2 weights
engine2.evaluation_engine.update_weights({
    "material": 1.2,
    "position": 0.8
})

# Play game
moves, final_board = self_play_game(engine1, engine2)
```

### Self-Play Training Loop

```python
def self_play_training(num_games=1000):
    """Self-play training loop"""
    games = []
    
    for game_num in range(num_games):
        # Create engines with slightly different weights
        engine1 = MinimaxEngine(max_depth=3)
        engine2 = MinimaxEngine(max_depth=3)
        
        # Add random variation to engine2
        random_weights = {
            "material": 1.0 + random.uniform(-0.2, 0.2),
            "position": 1.0 + random.uniform(-0.2, 0.2),
            "king_safety": 1.0 + random.uniform(-0.2, 0.2)
        }
        engine2.evaluation_engine.update_weights(random_weights)
        
        # Play game
        moves, final_board = self_play_game(engine1, engine2)
        
        # Record game
        game_data = {
            "moves": moves,
            "result": get_game_result(final_board),
            "engine1_weights": engine1.evaluation_engine.get_weights(),
            "engine2_weights": engine2.evaluation_engine.get_weights()
        }
        games.append(game_data)
        
        if game_num % 100 == 0:
            print(f"Completed {game_num} games")
    
    return games
```

## Advanced Techniques

### Ensemble Methods

```python
class EnsembleEvaluator:
    """Ensemble of multiple evaluation functions"""
    
    def __init__(self, evaluators, weights=None):
        self.evaluators = evaluators
        self.weights = weights or [1.0] * len(evaluators)
    
    def evaluate(self, board, color):
        """Combine evaluations from multiple engines"""
        scores = []
        for evaluator in self.evaluators:
            score = evaluator.evaluate(board, color)
            scores.append(score)
        
        # Weighted average
        weighted_score = sum(w * s for w, s in zip(self.weights, scores))
        return weighted_score / sum(self.weights)

# Create ensemble
evaluator1 = EvaluationEngine("weights1.json")
evaluator2 = EvaluationEngine("weights2.json")
evaluator3 = EvaluationEngine("weights3.json")

ensemble = EnsembleEvaluator([evaluator1, evaluator2, evaluator3])
```

### Transfer Learning

```python
def transfer_learning(source_model_path, target_dataset):
    """Transfer learning from pre-trained model"""
    # Load pre-trained model
    trainer = NeuralTrainer()
    trainer.load_model(source_model_path)
    
    # Freeze early layers
    for param in trainer.model.network[:-2].parameters():
        param.requires_grad = False
    
    # Fine-tune on new dataset
    history = trainer.train(
        dataset=target_dataset,
        epochs=50,
        learning_rate=0.0001
    )
    
    return trainer
```

### Curriculum Learning

```python
def curriculum_learning(dataset, stages):
    """Curriculum learning with increasing difficulty"""
    trainer = NeuralTrainer()
    
    for stage, difficulty in enumerate(stages):
        print(f"Training stage {stage + 1}: {difficulty}")
        
        # Filter data by difficulty
        if difficulty == "opening":
            stage_data = [p for p in dataset.positions if p.move_number <= 20]
        elif difficulty == "middlegame":
            stage_data = [p for p in dataset.positions if 20 < p.move_number <= 40]
        elif difficulty == "endgame":
            stage_data = [p for p in dataset.positions if p.move_number > 40]
        
        # Train on stage data
        stage_dataset = ChessDataset()
        stage_dataset.positions = stage_data
        
        trainer.train(
            dataset=stage_dataset,
            epochs=50,
            batch_size=32
        )
    
    return trainer
```

## Performance Optimization

### GPU Acceleration

```python
# Use GPU for training
trainer = NeuralTrainer(device="cuda")

# Check GPU availability
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU count: {torch.cuda.device_count()}")
```

### Memory Optimization

```python
# Use smaller batch sizes for large datasets
trainer.train(dataset, batch_size=16)

# Use gradient accumulation
trainer.train(dataset, batch_size=8, gradient_accumulation_steps=4)

# Clear cache periodically
import torch
torch.cuda.empty_cache()
```

### Distributed Training

```python
# Multi-GPU training
import torch.nn as nn

if torch.cuda.device_count() > 1:
    trainer.model = nn.DataParallel(trainer.model)

# Distributed training
import torch.distributed as dist
dist.init_process_group(backend='nccl')
```

### Hyperparameter Tuning

```python
def hyperparameter_search():
    """Search for optimal hyperparameters"""
    best_score = 0
    best_params = None
    
    # Define search space
    learning_rates = [0.001, 0.0001, 0.00001]
    hidden_sizes = [[128, 64], [256, 128, 64], [512, 256, 128]]
    batch_sizes = [16, 32, 64]
    
    for lr in learning_rates:
        for hidden in hidden_sizes:
            for batch_size in batch_sizes:
                # Train model
                trainer = NeuralTrainer(
                    hidden_sizes=hidden,
                    learning_rate=lr
                )
                
                history = trainer.train(
                    dataset=dataset,
                    epochs=50,
                    batch_size=batch_size
                )
                
                # Evaluate model
                score = evaluate_model(trainer)
                
                if score > best_score:
                    best_score = score
                    best_params = {
                        "learning_rate": lr,
                        "hidden_sizes": hidden,
                        "batch_size": batch_size
                    }
    
    return best_params, best_score
```

## Monitoring and Logging

### Training Metrics

```python
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def train_with_logging(trainer, dataset):
    """Train with detailed logging"""
    for epoch in range(100):
        # Training step
        train_loss = trainer._train_epoch(train_loader)
        val_loss = trainer._validate_epoch(val_loader)
        
        # Log metrics
        logger.info(f"Epoch {epoch}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}")
        
        # Save checkpoint
        if epoch % 10 == 0:
            trainer.save_model(f"checkpoint_epoch_{epoch}.pth")
```

### TensorBoard Integration

```python
from torch.utils.tensorboard import SummaryWriter

def train_with_tensorboard(trainer, dataset):
    """Train with TensorBoard logging"""
    writer = SummaryWriter('runs/chess_training')
    
    for epoch in range(100):
        train_loss = trainer._train_epoch(train_loader)
        val_loss = trainer._validate_epoch(val_loader)
        
        # Log to TensorBoard
        writer.add_scalar('Loss/Train', train_loss, epoch)
        writer.add_scalar('Loss/Validation', val_loss, epoch)
        
        # Log model parameters
        for name, param in trainer.model.named_parameters():
            writer.add_histogram(f'Parameters/{name}', param, epoch)
    
    writer.close()
```

## Best Practices

### Data Quality

1. **Use high-quality games**: Prefer games from strong players
2. **Balance data**: Include different game phases and positions
3. **Clean data**: Remove corrupted or invalid games
4. **Augment data**: Use position rotations and reflections

### Training Strategy

1. **Start simple**: Begin with basic evaluation functions
2. **Iterative improvement**: Gradually increase complexity
3. **Validate frequently**: Use holdout sets for validation
4. **Monitor overfitting**: Watch for training/validation gap

### Hyperparameter Tuning

1. **Grid search**: Systematically explore parameter space
2. **Random search**: More efficient for high-dimensional spaces
3. **Bayesian optimization**: Use tools like Optuna
4. **Cross-validation**: Use k-fold validation for robust estimates

### Model Selection

1. **Compare architectures**: Test different network designs
2. **Ensemble methods**: Combine multiple models
3. **Regularization**: Use dropout, weight decay, etc.
4. **Early stopping**: Prevent overfitting

## Troubleshooting

### Common Issues

1. **Overfitting**: Reduce model complexity or increase data
2. **Underfitting**: Increase model capacity or training time
3. **Slow convergence**: Adjust learning rate or optimizer
4. **Memory issues**: Reduce batch size or use gradient accumulation

### Debugging Tips

1. **Check gradients**: Monitor gradient norms and distributions
2. **Visualize data**: Plot training curves and distributions
3. **Compare baselines**: Test against simple evaluation functions
4. **Ablation studies**: Test individual components

## Next Steps

1. **Experiment with architectures**: Try different network designs
2. **Collect more data**: Gather larger and more diverse datasets
3. **Implement advanced techniques**: Use attention mechanisms, transformers
4. **Optimize for deployment**: Consider inference speed and memory usage