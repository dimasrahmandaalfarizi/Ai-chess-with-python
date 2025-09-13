# Chess Engine

A modular chess engine built from scratch in Python with training capabilities. This engine implements advanced chess algorithms including minimax with alpha-beta pruning, quiescence search, transposition tables, and machine learning-based evaluation.

## 🎯 Features

### Core Engine
- **Modular Architecture**: Clean separation of concerns with board representation, move generation, search algorithms, and evaluation
- **Advanced Search**: Minimax with alpha-beta pruning, iterative deepening, and quiescence search
- **Position Caching**: Transposition table with Zobrist hashing for improved performance
- **Move Ordering**: MVV-LVA, killer moves, and history heuristic for better pruning

### Evaluation System
- **Modular Evaluation**: Separate components for material, position, king safety, pawn structure, mobility, and more
- **Tunable Weights**: JSON-based weight configuration for easy parameter tuning
- **Piece-Square Tables**: Positional evaluation based on piece placement
- **Machine Learning**: Neural network training for position evaluation

### Training & Tuning
- **Genetic Algorithm**: Automated weight optimization using evolutionary algorithms
- **Neural Networks**: PyTorch-based training for evaluation functions
- **PGN Support**: Load and parse chess games for supervised learning
- **Self-Play**: Engine vs engine training capabilities

### Interface
- **UCI Protocol**: Compatible with chess GUIs like Arena, CuteChess, and ChessBase
- **CLI Interface**: Command-line interface for interactive play and testing
- **Multiple Modes**: Play, training, tuning, and testing modes

## 📁 Project Structure

```
chess_engine/
├── __init__.py
├── board/                    # Board representation and move generation
│   ├── __init__.py
│   ├── board.py             # Chess board and game state
│   └── move_generator.py    # Legal move generation
├── search/                   # Search algorithms
│   ├── __init__.py
│   ├── minimax.py           # Minimax with alpha-beta pruning
│   ├── quiescence.py        # Quiescence search
│   └── transposition.py     # Transposition table
├── eval/                     # Position evaluation
│   ├── __init__.py
│   ├── evaluation.py        # Modular evaluation engine
│   └── weights.json         # Evaluation weights
├── train/                    # Training and tuning
│   ├── __init__.py
│   ├── tuner.py             # Genetic algorithm weight tuning
│   ├── dataset.py           # PGN loading and parsing
│   └── trainer.py           # Neural network training
├── uci/                      # UCI protocol interface
│   ├── __init__.py
│   └── uci_interface.py     # UCI protocol implementation
└── tests/                    # Unit tests
    ├── __init__.py
    ├── test_board.py
    ├── test_search.py
    └── test_eval.py
```

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chess-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Basic Usage

1. **Interactive Play Mode**:
```bash
python main.py play
```

2. **UCI Interface** (for chess GUIs):
```bash
python main.py uci
```

3. **Test Mode**:
```bash
python main.py test
```

4. **Training Mode**:
```bash
python main.py train --data-dir data --epochs 100
```

5. **Weight Tuning**:
```bash
python main.py tune --generations 50 --population-size 30
```

## 🎮 Usage Examples

### Playing Against the Engine

```bash
python main.py play --depth 4 --time 5.0
```

Commands in play mode:
- `e2e4` - Make a move
- `engine` - Let engine make a move
- `eval` - Show position evaluation
- `new` - Start new game
- `quit` - Exit

### Training a Neural Network

1. Add PGN files to the `data/` directory
2. Run training:
```bash
python main.py train --epochs 200 --batch-size 64
```

### Tuning Evaluation Weights

```bash
python main.py tune --generations 100 --population-size 50
```

## 🔧 Configuration

### Evaluation Weights

Edit `chess_engine/eval/weights.json` to adjust evaluation parameters:

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

Command-line options:
- `--depth`: Search depth (default: 4)
- `--time`: Time limit per move in seconds (default: 5.0)
- `--epochs`: Training epochs (default: 100)
- `--batch-size`: Training batch size (default: 32)
- `--generations`: Tuning generations (default: 100)
- `--population-size`: Genetic algorithm population size (default: 50)

## 🧪 Testing

Run unit tests:
```bash
python -m pytest chess_engine/tests/
```

Or run individual test files:
```bash
python chess_engine/tests/test_board.py
python chess_engine/tests/test_search.py
python chess_engine/tests/test_eval.py
```

## 📊 Performance

The engine is designed for educational purposes and moderate performance. Typical performance characteristics:

- **Search Speed**: ~1000-10000 nodes/second (depending on depth and position)
- **Memory Usage**: ~50-100MB (with transposition table)
- **Training Time**: Varies based on dataset size and network architecture

## 🔬 Architecture Details

### Search Algorithm
- **Minimax**: Core search algorithm with alpha-beta pruning
- **Iterative Deepening**: Progressive depth increase with time management
- **Quiescence Search**: Tactical position handling
- **Transposition Table**: Position caching with Zobrist hashing
- **Move Ordering**: MVV-LVA, killer moves, history heuristic

### Evaluation System
- **Material Balance**: Piece values and material counting
- **Positional Factors**: Piece-square tables, center control, development
- **Tactical Factors**: King safety, pawn structure, mobility
- **Machine Learning**: Neural network evaluation with PyTorch

### Training Pipeline
1. **Data Collection**: PGN parsing and position extraction
2. **Feature Engineering**: Position encoding for neural networks
3. **Model Training**: Supervised learning with game results
4. **Weight Optimization**: Genetic algorithm for parameter tuning
5. **Validation**: Performance testing against known positions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Chess programming community for algorithms and techniques
- PyTorch team for the machine learning framework
- Python-chess library for PGN parsing inspiration
- UCI protocol specification for GUI compatibility

## 📚 References

- [Chess Programming Wiki](https://www.chessprogramming.org/)
- [UCI Protocol Specification](http://wbec-ridderkerk.nl/html/UCIProtocol.html)
- [Minimax Algorithm](https://en.wikipedia.org/wiki/Minimax)
- [Alpha-Beta Pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning)
- [Zobrist Hashing](https://en.wikipedia.org/wiki/Zobrist_hashing)

---

**Note**: This is an educational project. For production use, consider additional optimizations and testing.