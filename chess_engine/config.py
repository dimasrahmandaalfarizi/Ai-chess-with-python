"""
Configuration Management for Chess Engine

This module provides centralized configuration management.
"""

import json
import os
from typing import Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class SearchConfig:
    """Search algorithm configuration"""
    default_depth: int = 4
    max_depth: int = 20
    default_time_limit: float = 5.0
    max_time_limit: float = 300.0
    transposition_table_size: int = 1000000
    use_iterative_deepening: bool = True
    use_quiescence_search: bool = True
    use_move_ordering: bool = True
    aspiration_window_size: int = 50

@dataclass
class EvaluationConfig:
    """Evaluation function configuration"""
    material_weight: float = 1.0
    position_weight: float = 1.0
    king_safety_weight: float = 1.0
    pawn_structure_weight: float = 1.0
    mobility_weight: float = 1.0
    center_control_weight: float = 1.0
    development_weight: float = 1.0
    tempo_weight: float = 1.0

@dataclass
class TrainingConfig:
    """Training configuration"""
    default_epochs: int = 100
    default_batch_size: int = 32
    learning_rate: float = 0.001
    population_size: int = 50
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    elite_size: int = 5

@dataclass
class EngineConfig:
    """Main engine configuration"""
    engine_name: str = "ChessEngine"
    engine_version: str = "1.0.0"
    engine_author: str = "Chess Engine Team"
    
    search: SearchConfig = None
    evaluation: EvaluationConfig = None
    training: TrainingConfig = None
    
    def __post_init__(self):
        if self.search is None:
            self.search = SearchConfig()
        if self.evaluation is None:
            self.evaluation = EvaluationConfig()
        if self.training is None:
            self.training = TrainingConfig()
    
    @classmethod
    def from_file(cls, config_path: str) -> 'EngineConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(config_path):
            # Create default config file
            default_config = cls()
            default_config.save_to_file(config_path)
            return default_config
        
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            
            # Create config objects
            search_config = SearchConfig(**data.get('search', {}))
            eval_config = EvaluationConfig(**data.get('evaluation', {}))
            training_config = TrainingConfig(**data.get('training', {}))
            
            # Remove nested configs from main data
            main_data = {k: v for k, v in data.items() 
                        if k not in ['search', 'evaluation', 'training']}
            
            return cls(
                search=search_config,
                evaluation=eval_config,
                training=training_config,
                **main_data
            )
            
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error loading config from {config_path}: {e}")
            print("Using default configuration")
            return cls()
    
    def save_to_file(self, config_path: str):
        """Save configuration to JSON file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Convert to dictionary
            config_dict = {
                'engine_name': self.engine_name,
                'engine_version': self.engine_version,
                'engine_author': self.engine_author,
                'search': asdict(self.search),
                'evaluation': asdict(self.evaluation),
                'training': asdict(self.training)
            }
            
            with open(config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
                
        except Exception as e:
            print(f"Error saving config to {config_path}: {e}")
    
    def update_from_dict(self, updates: Dict[str, Any]):
        """Update configuration from dictionary"""
        for key, value in updates.items():
            if hasattr(self, key):
                if key in ['search', 'evaluation', 'training']:
                    # Update nested config
                    config_obj = getattr(self, key)
                    for sub_key, sub_value in value.items():
                        if hasattr(config_obj, sub_key):
                            setattr(config_obj, sub_key, sub_value)
                else:
                    setattr(self, key, value)

# Global configuration instance
config = EngineConfig.from_file("config/engine_config.json")