# Troubleshooting Guide

This guide helps you resolve common issues when using the Chess Engine.

## Table of Contents

- [Installation Issues](#installation-issues)
- [Runtime Errors](#runtime-errors)
- [Performance Issues](#performance-issues)
- [UCI Interface Problems](#uci-interface-problems)
- [Training Issues](#training-issues)
- [Common Error Messages](#common-error-messages)

## Installation Issues

### Python Version Compatibility

**Problem**: Engine fails to start with Python version error.

**Solution**: Ensure you're using Python 3.8 or higher:
```bash
python --version
```

If using an older version, upgrade Python or use a virtual environment:
```bash
# Using pyenv
pyenv install 3.10.0
pyenv local 3.10.0

# Using conda
conda create -n chess-engine python=3.10
conda activate chess-engine
```

### Missing Dependencies

**Problem**: ImportError when running the engine.

**Solution**: Install all required dependencies:
```bash
pip install -r requirements.txt
```

If specific packages fail to install:
```bash
# For PyTorch
pip install torch torchvision torchaudio

# For numpy
pip install numpy

# For python-chess
pip install python-chess
```

### Permission Issues

**Problem**: Permission denied when creating files or directories.

**Solution**: Check file permissions and run with appropriate privileges:
```bash
# On Linux/Mac
chmod +x main.py
sudo pip install -r requirements.txt

# On Windows
# Run Command Prompt as Administrator
```

## Runtime Errors

### Module Import Errors

**Problem**: `ModuleNotFoundError: No module named 'chess_engine'`

**Solution**: Ensure the chess_engine directory is in your Python path:
```bash
# Run from project root directory
python main.py

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python main.py
```

### Board State Errors

**Problem**: Invalid board state or move generation errors.

**Solution**: Check board initialization and move validation:
```python
from chess_engine.board.board import ChessBoard

# Create board with default position
board = ChessBoard()

# Verify board state
print(board)

# Check if position is valid
if board.is_checkmate(Color.WHITE):
    print("White is in checkmate")
```

### Search Algorithm Errors

**Problem**: Search algorithm fails or returns invalid moves.

**Solution**: Check search parameters and board state:
```python
from chess_engine.search.minimax import MinimaxEngine

# Use appropriate search depth
engine = MinimaxEngine(max_depth=3, time_limit=2.0)

# Ensure board is in valid state
if not board.is_checkmate(board.current_player):
    best_move, score = engine.search(board)
```

## Performance Issues

### Slow Search Performance

**Problem**: Engine searches very slowly.

**Solutions**:
1. **Reduce search depth**:
   ```python
   engine = MinimaxEngine(max_depth=2, time_limit=1.0)
   ```

2. **Enable transposition table**:
   ```python
   # Transposition table is enabled by default
   # Check if it's working properly
   stats = engine.get_search_stats()
   print(f"Transposition hits: {stats['transposition_hits']}")
   ```

3. **Optimize move ordering**:
   ```python
   # Move ordering is enabled by default
   # Check if it's working
   moves = move_gen.generate_legal_moves(Color.WHITE)
   ordered_moves = move_gen.order_moves(moves)
   ```

### Memory Usage Issues

**Problem**: High memory usage during search or training.

**Solutions**:
1. **Reduce transposition table size**:
   ```python
   from chess_engine.search.transposition import TranspositionTable
   
   # Use smaller table
   table = TranspositionTable(size_mb=32)
   ```

2. **Clear tables periodically**:
   ```python
   engine.clear_tables()
   ```

3. **Use smaller batch sizes for training**:
   ```python
   trainer.train(dataset, batch_size=16)
   ```

### Training Performance

**Problem**: Neural network training is slow.

**Solutions**:
1. **Use GPU if available**:
   ```python
   trainer = NeuralTrainer(device="cuda")
   ```

2. **Reduce network size**:
   ```python
   trainer = NeuralTrainer(hidden_sizes=[128, 64])
   ```

3. **Use smaller datasets**:
   ```python
   # Limit positions per game
   positions = dataset.extract_positions(games, max_positions_per_game=20)
   ```

## UCI Interface Problems

### GUI Integration Issues

**Problem**: Engine doesn't work with chess GUIs.

**Solutions**:
1. **Check working directory**:
   - Ensure GUI is set to use the project directory as working directory
   - Verify `main.py` is in the working directory

2. **Test UCI interface manually**:
   ```bash
   python main.py uci
   # Then type: uci
   # Should return engine information
   ```

3. **Check Python path**:
   - Ensure Python is in system PATH
   - Use full path to Python if necessary

### UCI Command Errors

**Problem**: UCI commands fail or return errors.

**Solutions**:
1. **Check command format**:
   ```
   uci
   isready
   position startpos
   go depth 3
   ```

2. **Enable debug mode**:
   ```python
   # Add debug prints to UCIInterface
   print(f"Received command: {command}")
   ```

3. **Verify engine state**:
   ```python
   # Check if engine is ready
   if not uci.is_ready:
       print("Engine not ready")
   ```

## Training Issues

### Dataset Loading Problems

**Problem**: PGN files fail to load or parse.

**Solutions**:
1. **Check file format**:
   - Ensure files are valid PGN format
   - Check file encoding (UTF-8)

2. **Verify file paths**:
   ```python
   import os
   
   # Check if file exists
   if os.path.exists("data/game.pgn"):
       print("File exists")
   else:
       print("File not found")
   ```

3. **Handle parsing errors**:
   ```python
   try:
       games = dataset.load_pgn_file("game.pgn")
   except Exception as e:
       print(f"Error loading PGN: {e}")
   ```

### Neural Network Training Issues

**Problem**: Training fails or produces poor results.

**Solutions**:
1. **Check data quality**:
   ```python
   # Verify dataset statistics
   stats = dataset.get_dataset_stats()
   print(f"Total positions: {stats['total_positions']}")
   ```

2. **Adjust learning rate**:
   ```python
   trainer = NeuralTrainer(learning_rate=0.0001)
   ```

3. **Use validation split**:
   ```python
   trainer.train(dataset, validation_split=0.2)
   ```

### Weight Tuning Issues

**Problem**: Genetic algorithm fails to converge.

**Solutions**:
1. **Adjust population size**:
   ```python
   tuner = WeightTuner(population_size=100)
   ```

2. **Modify mutation rate**:
   ```python
   tuner = WeightTuner(mutation_rate=0.05)
   ```

3. **Use hill climbing**:
   ```python
   weights = tuner.hill_climbing(initial_weights, max_iterations=500)
   ```

## Common Error Messages

### "No module named 'chess_engine'"

**Cause**: Python can't find the chess_engine module.

**Solution**: Run from project root directory or add to PYTHONPATH.

### "Invalid move"

**Cause**: Attempting to make an illegal move.

**Solution**: Check move legality before making it:
```python
if move_gen._is_legal_move(move):
    board.make_move(move)
```

### "Time limit exceeded"

**Cause**: Search takes longer than allowed time.

**Solution**: Increase time limit or reduce search depth:
```python
engine = MinimaxEngine(time_limit=10.0)
```

### "Board state invalid"

**Cause**: Board is in an inconsistent state.

**Solution**: Recreate board or check move history:
```python
board = ChessBoard()  # Reset to starting position
```

### "CUDA out of memory"

**Cause**: GPU memory exhausted during training.

**Solution**: Use CPU or reduce batch size:
```python
trainer = NeuralTrainer(device="cpu")
# Or
trainer.train(dataset, batch_size=8)
```

## Debugging Tips

### Enable Verbose Output

```python
# Add debug prints to key functions
def search(self, board, depth=None):
    print(f"Searching position: {board._get_fen()}")
    # ... rest of function
```

### Check Search Statistics

```python
stats = engine.get_search_stats()
print(f"Nodes searched: {stats['nodes_searched']}")
print(f"Cutoffs: {stats['cutoffs']}")
```

### Validate Board State

```python
# Check if board is in valid state
def validate_board(board):
    # Check for duplicate pieces
    # Verify castling rights
    # Check en passant target
    pass
```

### Test Individual Components

```python
# Test move generation
moves = move_gen.generate_legal_moves(Color.WHITE)
print(f"Generated {len(moves)} moves")

# Test evaluation
score = evaluator.evaluate(board, Color.WHITE)
print(f"Position score: {score}")
```

## Getting Help

If you encounter issues not covered in this guide:

1. **Check the logs**: Look for error messages in console output
2. **Verify dependencies**: Ensure all packages are installed correctly
3. **Test with minimal examples**: Start with simple test cases
4. **Check Python version**: Ensure compatibility with Python 3.8+
5. **Review documentation**: Check API documentation for correct usage

## Reporting Bugs

When reporting bugs, include:

1. **Python version**: `python --version`
2. **Operating system**: Windows, Linux, or macOS
3. **Error message**: Complete error traceback
4. **Steps to reproduce**: Minimal code example
5. **Expected behavior**: What should happen
6. **Actual behavior**: What actually happens

## Performance Optimization

### Search Optimization

1. **Use appropriate depth**: Balance between speed and strength
2. **Enable transposition table**: Significant performance improvement
3. **Optimize move ordering**: Better alpha-beta pruning
4. **Use quiescence search**: Handle tactical positions

### Training Optimization

1. **Use GPU**: Much faster for neural network training
2. **Batch processing**: Process multiple positions together
3. **Data preprocessing**: Clean and normalize data
4. **Model architecture**: Choose appropriate network size

### Memory Optimization

1. **Clear caches**: Regularly clear transposition tables
2. **Limit dataset size**: Use appropriate number of positions
3. **Streaming data**: Process data in batches
4. **Garbage collection**: Force cleanup when needed