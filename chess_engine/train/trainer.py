"""
Neural Network Trainer - Training evaluation networks

This module implements:
- Neural network training for position evaluation
- Supervised learning from game data
- Model architecture and optimization
- Training loop and validation
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from ..train.dataset import ChessDataset, GamePosition

class ChessPositionDataset(Dataset):
    """PyTorch dataset for chess positions"""
    
    def __init__(self, positions: List[GamePosition], feature_extractor):
        """
        Initialize dataset
        
        Args:
            positions: List of game positions
            feature_extractor: Function to extract features from FEN
        """
        self.positions = positions
        self.feature_extractor = feature_extractor
    
    def __len__(self):
        return len(self.positions)
    
    def __getitem__(self, idx):
        position = self.positions[idx]
        features = self.feature_extractor(position.fen)
        evaluation = torch.tensor(position.evaluation, dtype=torch.float32)
        
        return torch.tensor(features, dtype=torch.float32), evaluation

class EvaluationNetwork(nn.Module):
    """Neural network for chess position evaluation"""
    
    def __init__(self, input_size: int = 64, hidden_sizes: List[int] = [256, 128, 64]):
        """
        Initialize evaluation network
        
        Args:
            input_size: Size of input feature vector
            hidden_sizes: List of hidden layer sizes
        """
        super(EvaluationNetwork, self).__init__()
        
        layers = []
        prev_size = input_size
        
        for hidden_size in hidden_sizes:
            layers.append(nn.Linear(prev_size, hidden_size))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(0.2))
            prev_size = hidden_size
        
        # Output layer
        layers.append(nn.Linear(prev_size, 1))
        
        self.network = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.network(x).squeeze()

class NeuralTrainer:
    """Neural network trainer for chess evaluation"""
    
    def __init__(self, input_size: int = 64, hidden_sizes: List[int] = [256, 128, 64],
                 learning_rate: float = 0.001, device: str = "auto"):
        """
        Initialize neural trainer
        
        Args:
            input_size: Size of input feature vector
            hidden_sizes: List of hidden layer sizes
            learning_rate: Learning rate for optimizer
            device: Device to use for training ("auto", "cpu", "cuda")
        """
        self.input_size = input_size
        self.hidden_sizes = hidden_sizes
        self.learning_rate = learning_rate
        
        # Set device
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)
        
        print(f"Using device: {self.device}")
        
        # Initialize model
        self.model = EvaluationNetwork(input_size, hidden_sizes).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.MSELoss()
        
        # Training history
        self.training_history = {
            'train_loss': [],
            'val_loss': [],
            'epochs': []
        }
    
    def train(self, dataset: ChessDataset, epochs: int = 100, batch_size: int = 32,
              validation_split: float = 0.2, save_path: Optional[str] = None) -> Dict[str, List[float]]:
        """
        Train the neural network
        
        Args:
            dataset: Chess dataset
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_split: Fraction of data to use for validation
            save_path: Path to save trained model
            
        Returns:
            Training history
        """
        # Prepare data
        X, y = dataset.get_training_data()
        
        if not X or not y:
            print("No training data available")
            return self.training_history
        
        # Convert to numpy arrays
        X = np.array(X)
        y = np.array(y)
        
        # Split data
        split_idx = int(len(X) * (1 - validation_split))
        X_train, X_val = X[:split_idx], X[split_idx:]
        y_train, y_val = y[:split_idx], y[split_idx:]
        
        # Create datasets
        train_dataset = self._create_dataset(X_train, y_train)
        val_dataset = self._create_dataset(X_val, y_val)
        
        # Create data loaders
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        print(f"Training on {len(train_dataset)} samples, validating on {len(val_dataset)} samples")
        
        # Training loop
        for epoch in range(epochs):
            # Training
            train_loss = self._train_epoch(train_loader)
            
            # Validation
            val_loss = self._validate_epoch(val_loader)
            
            # Record history
            self.training_history['train_loss'].append(train_loss)
            self.training_history['val_loss'].append(val_loss)
            self.training_history['epochs'].append(epoch + 1)
            
            # Print progress
            if (epoch + 1) % 10 == 0:
                print(f"Epoch {epoch + 1}/{epochs}: Train Loss = {train_loss:.4f}, Val Loss = {val_loss:.4f}")
        
        # Save model
        if save_path:
            self.save_model(save_path)
        
        print("Training completed!")
        return self.training_history
    
    def _create_dataset(self, X: np.ndarray, y: np.ndarray) -> torch.utils.data.TensorDataset:
        """Create PyTorch dataset from numpy arrays"""
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.float32)
        return torch.utils.data.TensorDataset(X_tensor, y_tensor)
    
    def _train_epoch(self, train_loader: DataLoader) -> float:
        """Train for one epoch"""
        self.model.train()
        total_loss = 0.0
        num_batches = 0
        
        for batch_X, batch_y in train_loader:
            batch_X = batch_X.to(self.device)
            batch_y = batch_y.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            predictions = self.model(batch_X)
            loss = self.criterion(predictions, batch_y)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
            num_batches += 1
        
        return total_loss / num_batches
    
    def _validate_epoch(self, val_loader: DataLoader) -> float:
        """Validate for one epoch"""
        self.model.eval()
        total_loss = 0.0
        num_batches = 0
        
        with torch.no_grad():
            for batch_X, batch_y in val_loader:
                batch_X = batch_X.to(self.device)
                batch_y = batch_y.to(self.device)
                
                predictions = self.model(batch_X)
                loss = self.criterion(predictions, batch_y)
                
                total_loss += loss.item()
                num_batches += 1
        
        return total_loss / num_batches
    
    def evaluate_position(self, fen: str) -> float:
        """
        Evaluate a position using the trained model
        
        Args:
            fen: FEN string of position
            
        Returns:
            Evaluation score
        """
        self.model.eval()
        
        # Extract features
        features = self._extract_features(fen)
        features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            evaluation = self.model(features_tensor)
        
        return evaluation.item()
    
    def _extract_features(self, fen: str) -> List[float]:
        """Extract features from FEN string"""
        # TODO: Implement comprehensive feature extraction
        # This should match the feature extraction used in training
        
        # Placeholder: return random features
        return [np.random.random() for _ in range(self.input_size)]
    
    def save_model(self, path: str):
        """Save trained model"""
        torch.save({
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'learning_rate': self.learning_rate
        }, path)
        print(f"Model saved to {path}")
    
    def load_model(self, path: str):
        """Load trained model"""
        checkpoint = torch.load(path, map_location=self.device)
        
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.input_size = checkpoint['input_size']
        self.hidden_sizes = checkpoint['hidden_sizes']
        self.learning_rate = checkpoint['learning_rate']
        
        print(f"Model loaded from {path}")
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        total_params = sum(p.numel() for p in self.model.parameters())
        trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
        
        return {
            'input_size': self.input_size,
            'hidden_sizes': self.hidden_sizes,
            'total_parameters': total_params,
            'trainable_parameters': trainable_params,
            'device': str(self.device),
            'learning_rate': self.learning_rate
        }
    
    def plot_training_history(self, save_path: Optional[str] = None):
        """Plot training history"""
        try:
            import matplotlib.pyplot as plt
            
            plt.figure(figsize=(10, 6))
            plt.plot(self.training_history['epochs'], self.training_history['train_loss'], 
                    label='Training Loss', color='blue')
            plt.plot(self.training_history['epochs'], self.training_history['val_loss'], 
                    label='Validation Loss', color='red')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.title('Training History')
            plt.legend()
            plt.grid(True)
            
            if save_path:
                plt.savefig(save_path)
                print(f"Training history plot saved to {save_path}")
            else:
                plt.show()
                
        except ImportError:
            print("Matplotlib not available for plotting")