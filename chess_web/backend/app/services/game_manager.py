#!/usr/bin/env python3
"""
Game Manager Service

Manages active chess games and their states.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import threading
import time

from ..models.chess_models import GameState, GameMode, GameStatus

class GameManager:
    """Manages active chess games"""
    
    def __init__(self):
        """Initialize game manager"""
        self.games: Dict[str, GameState] = {}
        self.game_metadata: Dict[str, Dict[str, Any]] = {}
        self.cleanup_thread = None
        self.running = True
        
        # Start cleanup thread
        self._start_cleanup_thread()
    
    def add_game(self, game_id: str, game_state: GameState) -> bool:
        """Add a new game to the manager"""
        
        try:
            self.games[game_id] = game_state
            self.game_metadata[game_id] = {
                "created_at": datetime.now(),
                "last_activity": datetime.now(),
                "player_count": 1,
                "spectator_count": 0
            }
            
            return True
            
        except Exception as e:
            print(f"Error adding game {game_id}: {str(e)}")
            return False
    
    def get_game(self, game_id: str) -> Optional[GameState]:
        """Get game state by ID"""
        
        if game_id in self.games:
            # Update last activity
            if game_id in self.game_metadata:
                self.game_metadata[game_id]["last_activity"] = datetime.now()
            
            return self.games[game_id]
        
        return None
    
    def update_game(self, game_id: str, game_state: GameState) -> bool:
        """Update game state"""
        
        try:
            if game_id in self.games:
                self.games[game_id] = game_state
                
                # Update metadata
                if game_id in self.game_metadata:
                    self.game_metadata[game_id]["last_activity"] = datetime.now()
                
                return True
            
            return False
            
        except Exception as e:
            print(f"Error updating game {game_id}: {str(e)}")
            return False
    
    def remove_game(self, game_id: str) -> bool:
        """Remove game from manager"""
        
        try:
            if game_id in self.games:
                del self.games[game_id]
            
            if game_id in self.game_metadata:
                del self.game_metadata[game_id]
            
            return True
            
        except Exception as e:
            print(f"Error removing game {game_id}: {str(e)}")
            return False
    
    def list_games(self) -> List[Dict[str, Any]]:
        """List all active games"""
        
        game_list = []
        
        for game_id, game_state in self.games.items():
            metadata = self.game_metadata.get(game_id, {})
            
            game_info = {
                "game_id": game_id,
                "status": game_state.status,
                "turn": game_state.turn,
                "move_number": game_state.move_number,
                "created_at": metadata.get("created_at"),
                "last_activity": metadata.get("last_activity"),
                "player_count": metadata.get("player_count", 1),
                "spectator_count": metadata.get("spectator_count", 0)
            }
            
            game_list.append(game_info)
        
        return game_list
    
    def get_game_count(self) -> int:
        """Get total number of active games"""
        return len(self.games)
    
    def get_games_by_status(self, status: GameStatus) -> List[str]:
        """Get game IDs by status"""
        
        return [
            game_id for game_id, game_state in self.games.items()
            if game_state.status == status
        ]
    
    def add_spectator(self, game_id: str) -> bool:
        """Add spectator to game"""
        
        if game_id in self.game_metadata:
            self.game_metadata[game_id]["spectator_count"] += 1
            self.game_metadata[game_id]["last_activity"] = datetime.now()
            return True
        
        return False
    
    def remove_spectator(self, game_id: str) -> bool:
        """Remove spectator from game"""
        
        if game_id in self.game_metadata:
            self.game_metadata[game_id]["spectator_count"] = max(
                0, self.game_metadata[game_id]["spectator_count"] - 1
            )
            return True
        
        return False
    
    def get_game_statistics(self) -> Dict[str, Any]:
        """Get overall game statistics"""
        
        stats = {
            "total_games": len(self.games),
            "active_games": len(self.get_games_by_status(GameStatus.ACTIVE)),
            "completed_games": (
                len(self.get_games_by_status(GameStatus.CHECKMATE)) +
                len(self.get_games_by_status(GameStatus.STALEMATE)) +
                len(self.get_games_by_status(GameStatus.DRAW)) +
                len(self.get_games_by_status(GameStatus.RESIGNED))
            ),
            "total_spectators": sum(
                metadata.get("spectator_count", 0)
                for metadata in self.game_metadata.values()
            )
        }
        
        return stats
    
    def cleanup_inactive_games(self, max_age_hours: int = 24) -> int:
        """Clean up inactive games older than specified hours"""
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        games_to_remove = []
        
        for game_id, metadata in self.game_metadata.items():
            last_activity = metadata.get("last_activity", datetime.now())
            
            if last_activity < cutoff_time:
                games_to_remove.append(game_id)
        
        # Remove inactive games
        for game_id in games_to_remove:
            self.remove_game(game_id)
        
        return len(games_to_remove)
    
    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        
        def cleanup_worker():
            while self.running:
                try:
                    # Clean up games older than 24 hours
                    removed_count = self.cleanup_inactive_games(24)
                    
                    if removed_count > 0:
                        print(f"Cleaned up {removed_count} inactive games")
                    
                    # Sleep for 1 hour before next cleanup
                    time.sleep(3600)
                    
                except Exception as e:
                    print(f"Error in cleanup thread: {str(e)}")
                    time.sleep(300)  # Sleep 5 minutes on error
        
        self.cleanup_thread = threading.Thread(target=cleanup_worker, daemon=True)
        self.cleanup_thread.start()
    
    def shutdown(self):
        """Shutdown the game manager"""
        
        self.running = False
        
        if self.cleanup_thread and self.cleanup_thread.is_alive():
            self.cleanup_thread.join(timeout=5)
        
        # Clear all games
        self.games.clear()
        self.game_metadata.clear()
    
    def __del__(self):
        """Destructor to ensure cleanup"""
        self.shutdown()