# User Guide

This guide provides comprehensive instructions for using the Chess Engine.

## Table of Contents

- [Getting Started](#getting-started)
- [Interactive Play Mode](#interactive-play-mode)
- [UCI Interface](#uci-interface)
- [Training and Tuning](#training-and-tuning)
- [Configuration](#configuration)
- [Advanced Usage](#advanced-usage)
- [Tips and Tricks](#tips-and-tricks)

## Getting Started

### Quick Start

1. **Run the engine**:
   ```bash
   python main.py play
   ```

2. **Let the engine make a move**:
   ```
   engine
   ```

3. **Make your own move**:
   ```
   e2e4
   ```

4. **Quit**:
   ```
   quit
   ```

### Available Modes

- `play` - Interactive play mode
- `uci` - UCI protocol for chess GUIs
- `train` - Neural network training
- `tune` - Weight optimization
- `test` - Run tests

## Interactive Play Mode

### Starting Play Mode

```bash
python main.py play [options]
```

**Options**:
- `--depth N` - Search depth (default: 4)
- `--time N` - Time limit per move in seconds (default: 5.0)
- `--verbose` - Verbose output

### Commands

#### Basic Commands
- `e2e4` - Make a move (algebraic notation)
- `engine` - Let the engine make a move
- `eval` - Show position evaluation
- `new` - Start a new game
- `quit` - Exit the program
- `help` - Show help

#### Advanced Commands
- `show` - Display current position
- `history` - Show move history
- `undo` - Undo last move
- `fen` - Show FEN string
- `moves` - List all legal moves

### Example Session

```
Chess Engine - Play Mode
Commands: move (e.g., e2e4), quit, new, eval, help

Current position (Move 1):
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
P P P P P P P P
R N B Q K B N R
To move: WHITE

Enter command: e2e4
Move e2e4 made successfully!

Current position (Move 2):
r n b q k b n r
p p p p p p p p
. . . . . . . .
. . . . . . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
To move: BLACK

Enter command: engine
Engine is thinking...
Engine plays: e7e5 (score: 0.00)

Current position (Move 3):
r n b q k b n r
p p p p . p p p
. . . . . . . .
. . . . p . . .
. . . . P . . .
. . . . . . . .
P P P P . P P P
R N B Q K B N R
To move: WHITE

Enter command: quit
```

## UCI Interface

### Starting UCI Mode

```bash
python main.py uci
```

### Using with Chess GUIs

#### Arena Chess GUI
1. Download Arena from [playwitharena.com](http://www.playwitharena.com/)
2. Go to Engine → Install New Engine
3. Command: `python main.py uci`
4. Working Directory: Path to chess-engine folder

#### CuteChess GUI
1. Download CuteChess from [cutechess.com](https://cutechess.com/)
2. Go to Engine → New Engine
3. Command: `python main.py uci`
4. Working Directory: Path to chess-engine folder

#### ChessBase
1. Go to Engine → Install Engine
2. Command: `python main.py uci`
3. Working Directory: Path to chess-engine folder

### UCI Commands

The engine supports standard UCI commands:

- `uci` - Engine identification
- `isready` - Check if engine is ready
- `ucinewgame` - Start new game
- `position startpos` - Set starting position
- `position fen <fen>` - Set position from FEN
- `go depth N` - Search to depth N
- `go movetime N` - Search for N milliseconds
- `stop` - Stop search
- `quit` - Quit engine

### UCI Options

The engine supports these UCI options:

- `Hash` - Transposition table size (1-1024 MB)
- `Depth` - Default search depth (1-20)
- `Time` - Default time limit (1-300 seconds)
- `Threads` - Number of threads (1-8)
- `OwnBook` - Use opening book (true/false)
- `Ponder` - Enable pondering (true/false)

## Training and Tuning

### Neural Network Training

#### Prepare Data
1. Add PGN files to the `data/` directory
2. Run training:
   ```bash
   python main.py train --epochs 100 --batch-size 32
   ```

#### Training Options
- `--data-dir DIR` - Data directory (default: data)
- `--epochs N` - Number of training epochs (default: 100)
- `--batch-size N` - Batch size (default: 32)

### Weight Tuning

#### Genetic Algorithm Tuning
```bash
python main.py tune --generations 50 --population-size 30
```

#### Tuning Options
- `--generations N` - Number of generations (default: 100)
- `--population-size N` - Population size (default: 50)

### Example Training Workflow

1. **Collect data**:
   ```bash
   # Add PGN files to data/ directory
   cp games/*.pgn data/
   ```

2. **Extract positions**:
   ```python
   from chess_engine.train.dataset import ChessDataset
   
   dataset = ChessDataset("data")
   dataset.load_pgn_file("games.pgn")
   positions = dataset.extract_positions(dataset.games)
   ```

3. **Train neural network**:
   ```bash
   python main.py train --epochs 200 --batch-size 64
   ```

4. **Tune weights**:
   ```bash
   python main.py tune --generations 100
   ```

## Configuration

### Evaluation Weights

Edit `chess_engine/eval/weights.json`:

```json
{
  "material": 1.0,
  "position": 1.0,
  "king_safety": 1.0,
  "pawn_structure": 1.0,
  "mobility": 1.0,
  "center_control": 1.0,
  "development": 1.0,
  "tempo": 1.0
}
```

### Engine Parameters

Set default parameters in `main.py`:

```python
# Search parameters
engine = MinimaxEngine(max_depth=4, time_limit=5.0)

# Evaluation parameters
evaluator = EvaluationEngine("custom_weights.json")
```

### UCI Options

Configure UCI options in `chess_engine/uci/uci_interface.py`:

```python
self.options = {
    "Hash": {"type": "spin", "default": 64, "min": 1, "max": 1024},
    "Depth": {"type": "spin", "default": 4, "min": 1, "max": 20},
    # ... other options
}
```

## Advanced Usage

### Custom Position Analysis

```python
from chess_engine.board.board import ChessBoard
from chess_engine.eval.evaluation import EvaluationEngine

# Load custom position
fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
board = ChessBoard(fen)

# Evaluate position
evaluator = EvaluationEngine()
score = evaluator.evaluate(board, Color.WHITE)
print(f"Position evaluation: {score}")

# Get detailed breakdown
breakdown = evaluator.get_evaluation_breakdown(board, Color.WHITE)
for component, value in breakdown.items():
    print(f"{component}: {value}")
```

### Custom Search Parameters

```python
from chess_engine.search.minimax import MinimaxEngine

# Create engine with custom parameters
engine = MinimaxEngine(max_depth=6, time_limit=10.0)

# Search for best move
best_move, score = engine.search(board)

# Get search statistics
stats = engine.get_search_stats()
print(f"Nodes searched: {stats['nodes_searched']}")
print(f"Cutoffs: {stats['cutoffs']}")
```

### Batch Analysis

```python
from chess_engine.train.dataset import ChessDataset

# Load dataset
dataset = ChessDataset("data")
dataset.load_pgn_file("games.pgn")

# Extract positions
positions = dataset.extract_positions(dataset.games)

# Analyze positions
for position in positions:
    board = ChessBoard(position.fen)
    score = evaluator.evaluate(board, position.color_to_move)
    print(f"Move: {position.move}, Score: {score}")
```

## Tips and Tricks

### Improving Engine Strength

1. **Increase search depth**:
   ```bash
   python main.py play --depth 6
   ```

2. **Use more time**:
   ```bash
   python main.py play --time 10
   ```

3. **Tune evaluation weights**:
   ```bash
   python main.py tune --generations 200
   ```

4. **Train neural network**:
   ```bash
   python main.py train --epochs 500
   ```

### Performance Optimization

1. **Use transposition table**:
   - Increase hash size in UCI options
   - Clear table periodically

2. **Optimize move ordering**:
   - Enable killer moves
   - Use history heuristic

3. **Adjust search parameters**:
   - Use iterative deepening
   - Enable quiescence search

### Debugging

1. **Enable verbose output**:
   ```bash
   python main.py play --verbose
   ```

2. **Check search statistics**:
   ```python
   stats = engine.get_search_stats()
   print(stats)
   ```

3. **Validate moves**:
   ```python
   moves = move_gen.generate_legal_moves(color)
   for move in moves:
       if not move_gen._is_legal_move(move):
           print(f"Invalid move: {move}")
   ```

### Common Patterns

#### Opening Analysis
```python
# Analyze opening position
opening_fen = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"
board = ChessBoard(opening_fen)
score = evaluator.evaluate(board, Color.WHITE)
```

#### Endgame Analysis
```python
# Analyze endgame position
endgame_fen = "8/8/8/8/8/8/4K3/4k3 w - - 0 1"
board = ChessBoard(endgame_fen)
score = evaluator.evaluate(board, Color.WHITE)
```

#### Tactical Analysis
```python
# Analyze tactical position
tactical_fen = "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/3P1N2/PPP2PPP/RNBQK2R w KQkq - 4 4"
board = ChessBoard(tactical_fen)
score = evaluator.evaluate(board, Color.WHITE)
```

## Troubleshooting

### Common Issues

1. **Engine doesn't respond**: Check if Python is in PATH
2. **Invalid moves**: Verify move notation format
3. **Slow performance**: Reduce search depth or increase time limit
4. **Memory issues**: Clear transposition table or reduce batch size

### Getting Help

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Run tests to verify installation
3. Check the [API Documentation](API.md)
4. Create an issue with detailed information

## Next Steps

1. **Explore Examples**: Check the `examples/` directory
2. **Read API Docs**: See `docs/API.md` for detailed reference
3. **Join Community**: Participate in discussions and contributions
4. **Advanced Features**: Explore machine learning and tuning capabilities