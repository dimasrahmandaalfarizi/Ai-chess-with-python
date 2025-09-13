# Chess Engine API Documentation

This document provides detailed API documentation for the Chess Engine components.

## Table of Contents

- [Board Module](#board-module)
- [Search Module](#search-module)
- [Evaluation Module](#evaluation-module)
- [Training Module](#training-module)
- [UCI Module](#uci-module)

## Board Module

### ChessBoard Class

The main class for representing chess positions and game state.

#### Constructor
```python
ChessBoard(fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
```

**Parameters:**
- `fen`: Forsyth-Edwards Notation string representing board state

#### Methods

##### `get_piece(square: Tuple[int, int]) -> Optional[Square]`
Get piece at given square coordinates.

**Parameters:**
- `square`: Tuple of (file, rank) coordinates (0-7)

**Returns:**
- `Square` object or `None` if invalid coordinates

##### `make_move(move: Move) -> bool`
Make a move on the board.

**Parameters:**
- `move`: Move object to make

**Returns:**
- `True` if move was successful, `False` otherwise

##### `undo_move() -> bool`
Undo the last move.

**Returns:**
- `True` if move was undone, `False` if no moves to undo

##### `is_check(color: Color) -> bool`
Check if given color is in check.

**Parameters:**
- `color`: Color to check

**Returns:**
- `True` if in check, `False` otherwise

##### `is_checkmate(color: Color) -> bool`
Check if given color is in checkmate.

**Parameters:**
- `color`: Color to check

**Returns:**
- `True` if in checkmate, `False` otherwise

##### `is_stalemate(color: Color) -> bool`
Check if given color is in stalemate.

**Parameters:**
- `color`: Color to check

**Returns:**
- `True` if in stalemate, `False` otherwise

### MoveGenerator Class

Generates legal moves for chess positions.

#### Constructor
```python
MoveGenerator(board: ChessBoard)
```

**Parameters:**
- `board`: Chess board instance

#### Methods

##### `generate_legal_moves(color: Color) -> List[Move]`
Generate all legal moves for given color.

**Parameters:**
- `color`: Color to generate moves for

**Returns:**
- List of legal moves

##### `order_moves(moves: List[Move]) -> List[Move]`
Order moves for better search performance.

**Parameters:**
- `moves`: List of moves to order

**Returns:**
- Ordered list of moves

## Search Module

### MinimaxEngine Class

Minimax search engine with alpha-beta pruning.

#### Constructor
```python
MinimaxEngine(max_depth: int = 4, time_limit: float = 5.0)
```

**Parameters:**
- `max_depth`: Maximum search depth
- `time_limit`: Time limit in seconds

#### Methods

##### `search(board: ChessBoard, depth: Optional[int] = None) -> Tuple[Move, float]`
Search for best move using minimax with alpha-beta pruning.

**Parameters:**
- `board`: Current chess position
- `depth`: Search depth (uses max_depth if None)

**Returns:**
- Tuple of (best_move, evaluation_score)

##### `get_search_stats() -> Dict[str, Any]`
Get search statistics.

**Returns:**
- Dictionary containing search statistics

##### `clear_tables()`
Clear transposition and history tables.

### TranspositionTable Class

Transposition table for position caching.

#### Constructor
```python
TranspositionTable(size_mb: int = 64)
```

**Parameters:**
- `size_mb`: Size of table in megabytes

#### Methods

##### `get_hash(board: ChessBoard) -> int`
Calculate Zobrist hash for board position.

**Parameters:**
- `board`: Chess board position

**Returns:**
- Zobrist hash value

##### `store_exact(board: ChessBoard, move: Optional[Move], score: float, depth: int)`
Store exact score in transposition table.

**Parameters:**
- `board`: Chess board position
- `move`: Best move found
- `score`: Evaluation score
- `depth`: Search depth

##### `retrieve(board: ChessBoard) -> Optional[TranspositionEntry]`
Retrieve position from transposition table.

**Parameters:**
- `board`: Chess board position

**Returns:**
- Transposition entry if found, None otherwise

### QuiescenceSearch Class

Quiescence search for handling tactical positions.

#### Constructor
```python
QuiescenceSearch(max_depth: int = 6)
```

**Parameters:**
- `max_depth`: Maximum quiescence search depth

#### Methods

##### `search(board: ChessBoard, alpha: float, beta: float, color: Color, depth: int = 0) -> float`
Perform quiescence search.

**Parameters:**
- `board`: Current position
- `alpha`: Alpha value
- `beta`: Beta value
- `color`: Color to move
- `depth`: Current depth

**Returns:**
- Evaluation score

## Evaluation Module

### EvaluationEngine Class

Modular chess position evaluation engine.

#### Constructor
```python
EvaluationEngine(weights_file: str = "weights.json")
```

**Parameters:**
- `weights_file`: Path to weights configuration file

#### Methods

##### `evaluate(board: ChessBoard, color: Color) -> float`
Evaluate chess position.

**Parameters:**
- `board`: Chess board position
- `color`: Color to evaluate for

**Returns:**
- Evaluation score (positive = good for color)

##### `get_evaluation_breakdown(board: ChessBoard, color: Color) -> Dict[str, float]`
Get detailed evaluation breakdown.

**Parameters:**
- `board`: Chess board position
- `color`: Color to evaluate for

**Returns:**
- Dictionary containing evaluation components

##### `update_weights(new_weights: Dict[str, float])`
Update evaluation weights.

**Parameters:**
- `new_weights`: Dictionary of new weight values

##### `get_weights() -> Dict[str, float]`
Get current evaluation weights.

**Returns:**
- Dictionary of current weights

##### `reset_weights()`
Reset weights to default values.

## Training Module

### WeightTuner Class

Genetic algorithm tuner for evaluation weights.

#### Constructor
```python
WeightTuner(population_size: int = 50, mutation_rate: float = 0.1, 
           crossover_rate: float = 0.8, elite_size: int = 5)
```

**Parameters:**
- `population_size`: Size of population
- `mutation_rate`: Probability of mutation
- `crossover_rate`: Probability of crossover
- `elite_size`: Number of elite individuals to preserve

#### Methods

##### `initialize_population(base_weights: Optional[Dict[str, float]] = None)`
Initialize population with random weights.

**Parameters:**
- `base_weights`: Starting weights (None for random)

##### `evolve(num_generations: int = 100, games_per_evaluation: int = 10)`
Evolve population for specified number of generations.

**Parameters:**
- `num_generations`: Number of generations to evolve
- `games_per_evaluation`: Number of games per fitness evaluation

##### `hill_climbing(initial_weights: Dict[str, float], max_iterations: int = 1000, 
                 step_size: float = 0.1) -> Dict[str, float]`
Hill climbing optimization as alternative to genetic algorithm.

**Parameters:**
- `initial_weights`: Starting weights
- `max_iterations`: Maximum iterations
- `step_size`: Step size for weight adjustments

**Returns:**
- Optimized weights

##### `save_best_weights(filename: str = "best_weights.json")`
Save best weights to file.

**Parameters:**
- `filename`: Path to save weights

### ChessDataset Class

Dataset for chess position training.

#### Constructor
```python
ChessDataset(data_dir: str = "data")
```

**Parameters:**
- `data_dir`: Directory containing PGN files

#### Methods

##### `load_pgn_file(filename: str) -> List[ChessGame]`
Load games from PGN file.

**Parameters:**
- `filename`: Path to PGN file

**Returns:**
- List of parsed games

##### `extract_positions(games: List[ChessGame], max_positions_per_game: int = 50) -> List[GamePosition]`
Extract positions from games for training.

**Parameters:**
- `games`: List of games to process
- `max_positions_per_game`: Maximum positions to extract per game

**Returns:**
- List of game positions

##### `get_training_data(features: List[str] = None) -> Tuple[List[List[float]], List[float]]`
Get training data in format suitable for machine learning.

**Parameters:**
- `features`: List of features to extract (None for all)

**Returns:**
- Tuple of (features, labels)

### NeuralTrainer Class

Neural network trainer for chess evaluation.

#### Constructor
```python
NeuralTrainer(input_size: int = 64, hidden_sizes: List[int] = [256, 128, 64],
             learning_rate: float = 0.001, device: str = "auto")
```

**Parameters:**
- `input_size`: Size of input feature vector
- `hidden_sizes`: List of hidden layer sizes
- `learning_rate`: Learning rate for optimizer
- `device`: Device to use for training

#### Methods

##### `train(dataset: ChessDataset, epochs: int = 100, batch_size: int = 32,
         validation_split: float = 0.2, save_path: Optional[str] = None) -> Dict[str, List[float]]`
Train the neural network.

**Parameters:**
- `dataset`: Chess dataset
- `epochs`: Number of training epochs
- `batch_size`: Batch size for training
- `validation_split`: Fraction of data to use for validation
- `save_path`: Path to save trained model

**Returns:**
- Training history

##### `evaluate_position(fen: str) -> float`
Evaluate a position using the trained model.

**Parameters:**
- `fen`: FEN string of position

**Returns:**
- Evaluation score

##### `save_model(path: str)`
Save trained model.

**Parameters:**
- `path`: Path to save model

##### `load_model(path: str)`
Load trained model.

**Parameters:**
- `path`: Path to load model from

## UCI Module

### UCIInterface Class

UCI protocol interface for chess engine.

#### Constructor
```python
UCIInterface()
```

#### Methods

##### `run()`
Main UCI loop for communication with chess GUIs.

##### `process_command(command: str) -> Optional[str]`
Process UCI command.

**Parameters:**
- `command`: UCI command string

**Returns:**
- Response string (None if no response needed)

## Data Structures

### Move Class

Represents a chess move.

#### Constructor
```python
Move(from_square: Tuple[int, int], to_square: Tuple[int, int], 
     piece_type: PieceType, color: Color, promotion: Optional[PieceType] = None,
     is_castling: bool = False, is_en_passant: bool = False, is_capture: bool = False)
```

#### Attributes
- `from_square`: Starting square coordinates
- `to_square`: Destination square coordinates
- `piece_type`: Type of piece making the move
- `color`: Color of the piece
- `promotion`: Piece type for promotion (if applicable)
- `is_castling`: Whether move is castling
- `is_en_passant`: Whether move is en passant
- `is_capture`: Whether move is a capture

### Square Class

Represents a square on the chess board.

#### Constructor
```python
Square(piece_type: Optional[PieceType] = None, color: Optional[Color] = None)
```

#### Attributes
- `piece_type`: Type of piece on square (None if empty)
- `color`: Color of piece (None if empty)
- `empty`: Boolean indicating if square is empty

### Enums

#### PieceType
- `PAWN = 1`
- `KNIGHT = 2`
- `BISHOP = 3`
- `ROOK = 4`
- `QUEEN = 5`
- `KING = 6`

#### Color
- `WHITE = 1`
- `BLACK = -1`

#### NodeType
- `EXACT = 0`
- `LOWER_BOUND = 1`
- `UPPER_BOUND = 2`

## Error Handling

All classes include proper error handling and validation:

- Invalid square coordinates return `None` or raise appropriate exceptions
- Invalid moves are rejected with `False` return values
- File operations include try-catch blocks for I/O errors
- Search algorithms include timeout handling
- UCI protocol includes command validation

## Performance Considerations

- Transposition table uses Zobrist hashing for fast position identification
- Move ordering improves alpha-beta pruning efficiency
- Iterative deepening provides time management
- Quiescence search handles tactical positions
- Neural networks use PyTorch for efficient computation

## Threading and Concurrency

- Search algorithms are designed to be interruptible
- UCI interface handles multiple concurrent commands
- Training can be run in background threads
- Transposition table is thread-safe for concurrent access