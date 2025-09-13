"""
Chess Dataset - PGN loading and parsing for training

This module implements:
- PGN file loading and parsing
- Position extraction from games
- Label generation for supervised learning
- Dataset preprocessing and augmentation
"""

import re
import os
import json
from typing import List, Dict, Tuple, Any, Optional
from dataclasses import dataclass
from ..board.board import ChessBoard, Color, Move

@dataclass
class GamePosition:
    """Represents a position from a chess game"""
    fen: str
    move: str
    evaluation: float
    game_result: str  # "1-0", "0-1", "1/2-1/2"
    move_number: int
    color_to_move: Color

@dataclass
class ChessGame:
    """Represents a complete chess game"""
    moves: List[str]
    result: str
    white_player: str
    black_player: str
    event: str
    site: str
    date: str
    eco: str  # Opening code

class ChessDataset:
    """Dataset for chess position training"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize chess dataset
        
        Args:
            data_dir: Directory containing PGN files
        """
        self.data_dir = data_dir
        self.games = []
        self.positions = []
        self.loaded_files = set()
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
    
    def load_pgn_file(self, filename: str) -> List[ChessGame]:
        """
        Load games from PGN file
        
        Args:
            filename: Path to PGN file
            
        Returns:
            List of parsed games
        """
        if filename in self.loaded_files:
            return []
        
        games = []
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found")
            return games
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            games = self._parse_pgn_content(content)
            self.games.extend(games)
            self.loaded_files.add(filename)
            
            print(f"Loaded {len(games)} games from {filename}")
            
        except Exception as e:
            print(f"Error loading {filename}: {e}")
        
        return games
    
    def _parse_pgn_content(self, content: str) -> List[ChessGame]:
        """Parse PGN content and extract games"""
        games = []
        
        # Split content into individual games
        game_blocks = re.split(r'\n\n(?=\[)', content.strip())
        
        for block in game_blocks:
            if not block.strip():
                continue
            
            try:
                game = self._parse_single_game(block)
                if game:
                    games.append(game)
            except Exception as e:
                print(f"Error parsing game: {e}")
                continue
        
        return games
    
    def _parse_single_game(self, game_text: str) -> Optional[ChessGame]:
        """Parse a single PGN game"""
        lines = game_text.strip().split('\n')
        
        # Parse headers
        headers = {}
        move_text = ""
        
        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                # Parse header
                match = re.match(r'\[(\w+)\s+"([^"]+)"\]', line)
                if match:
                    key, value = match.groups()
                    headers[key] = value
            else:
                # Move text
                move_text += line + " "
        
        # Extract moves
        moves = self._extract_moves(move_text)
        
        if not moves:
            return None
        
        return ChessGame(
            moves=moves,
            result=headers.get('Result', '*'),
            white_player=headers.get('White', 'Unknown'),
            black_player=headers.get('Black', 'Unknown'),
            event=headers.get('Event', 'Unknown'),
            site=headers.get('Site', 'Unknown'),
            date=headers.get('Date', '????.??.??'),
            eco=headers.get('ECO', '')
        )
    
    def _extract_moves(self, move_text: str) -> List[str]:
        """Extract moves from move text"""
        # Remove game result and other annotations
        move_text = re.sub(r'\s+\d+-\d+|\s+\d+/\d+-\d+/\d+|\s+\*', '', move_text)
        
        # Split by move numbers and extract moves
        moves = []
        move_pattern = r'(\d+\.\s*)?([NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?[+#]?)\s*([NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?[+#]?)?'
        
        matches = re.findall(move_pattern, move_text)
        for match in matches:
            white_move = match[1]
            black_move = match[2]
            
            if white_move:
                moves.append(white_move)
            if black_move:
                moves.append(black_move)
        
        return moves
    
    def extract_positions(self, games: List[ChessGame], max_positions_per_game: int = 50) -> List[GamePosition]:
        """
        Extract positions from games for training
        
        Args:
            games: List of games to process
            max_positions_per_game: Maximum positions to extract per game
            
        Returns:
            List of game positions
        """
        positions = []
        
        for game in games:
            try:
                game_positions = self._extract_game_positions(game, max_positions_per_game)
                positions.extend(game_positions)
            except Exception as e:
                print(f"Error extracting positions from game: {e}")
                continue
        
        self.positions.extend(positions)
        print(f"Extracted {len(positions)} positions from {len(games)} games")
        
        return positions
    
    def _extract_game_positions(self, game: ChessGame, max_positions: int) -> List[GamePosition]:
        """Extract positions from a single game"""
        positions = []
        
        # Create board and play through moves
        board = ChessBoard()
        move_number = 1
        
        for i, move_str in enumerate(game.moves):
            if len(positions) >= max_positions:
                break
            
            # Parse move and make it
            move = self._parse_move(move_str, board)
            if not move or not board.make_move(move):
                continue
            
            # Create position
            position = GamePosition(
                fen=board._get_fen(),
                move=move_str,
                evaluation=self._estimate_evaluation(board, game.result, move_number),
                game_result=game.result,
                move_number=move_number,
                color_to_move=board.current_player
            )
            
            positions.append(position)
            move_number += 1
        
        return positions
    
    def _parse_move(self, move_str: str, board: ChessBoard) -> Optional[Move]:
        """Parse move string and create Move object"""
        # TODO: Implement proper move parsing
        # This is a simplified version - real implementation would be more complex
        
        # For now, return None to indicate parsing not implemented
        return None
    
    def _estimate_evaluation(self, board: ChessBoard, game_result: str, move_number: int) -> float:
        """Estimate position evaluation based on game result and position"""
        # TODO: Implement proper evaluation estimation
        # - Use engine evaluation
        # - Consider game result and move number
        # - Apply result scaling based on game phase
        
        # Placeholder: random evaluation
        import random
        return random.uniform(-2.0, 2.0)
    
    def save_positions(self, filename: str = "positions.json"):
        """Save extracted positions to file"""
        positions_data = []
        
        for pos in self.positions:
            positions_data.append({
                'fen': pos.fen,
                'move': pos.move,
                'evaluation': pos.evaluation,
                'game_result': pos.game_result,
                'move_number': pos.move_number,
                'color_to_move': pos.color_to_move.name
            })
        
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(positions_data, f, indent=2)
        
        print(f"Saved {len(positions_data)} positions to {filepath}")
    
    def load_positions(self, filename: str = "positions.json") -> List[GamePosition]:
        """Load positions from file"""
        filepath = os.path.join(self.data_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found")
            return []
        
        try:
            with open(filepath, 'r') as f:
                positions_data = json.load(f)
            
            positions = []
            for data in positions_data:
                position = GamePosition(
                    fen=data['fen'],
                    move=data['move'],
                    evaluation=data['evaluation'],
                    game_result=data['game_result'],
                    move_number=data['move_number'],
                    color_to_move=Color[data['color_to_move']]
                )
                positions.append(position)
            
            self.positions.extend(positions)
            print(f"Loaded {len(positions)} positions from {filepath}")
            
            return positions
            
        except Exception as e:
            print(f"Error loading positions: {e}")
            return []
    
    def get_training_data(self, features: List[str] = None) -> Tuple[List[List[float]], List[float]]:
        """
        Get training data in format suitable for machine learning
        
        Args:
            features: List of features to extract (None for all)
            
        Returns:
            Tuple of (features, labels)
        """
        if not self.positions:
            return [], []
        
        # TODO: Implement feature extraction
        # - Convert FEN to feature vector
        # - Extract piece positions, material, etc.
        # - Normalize features
        
        X = []  # Features
        y = []  # Labels (evaluations)
        
        for position in self.positions:
            # Placeholder feature extraction
            features_vector = self._extract_features(position.fen, features)
            X.append(features_vector)
            y.append(position.evaluation)
        
        return X, y
    
    def _extract_features(self, fen: str, feature_list: List[str] = None) -> List[float]:
        """Extract features from FEN string"""
        # TODO: Implement comprehensive feature extraction
        # - Material balance
        # - Piece positions
        # - King safety
        # - Pawn structure
        # - Mobility
        # - Center control
        
        # Placeholder: return random features
        import random
        return [random.random() for _ in range(64)]  # 64 features as placeholder
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        if not self.positions:
            return {}
        
        evaluations = [pos.evaluation for pos in self.positions]
        move_numbers = [pos.move_number for pos in self.positions]
        
        return {
            "total_games": len(self.games),
            "total_positions": len(self.positions),
            "avg_evaluation": sum(evaluations) / len(evaluations),
            "min_evaluation": min(evaluations),
            "max_evaluation": max(evaluations),
            "avg_move_number": sum(move_numbers) / len(move_numbers),
            "loaded_files": len(self.loaded_files)
        }