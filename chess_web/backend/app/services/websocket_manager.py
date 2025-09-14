#!/usr/bin/env python3
"""
WebSocket Manager

Manages WebSocket connections for real-time communication.
"""

from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List, Set, Any
import json
import asyncio
from datetime import datetime

class WebSocketManager:
    """Manages WebSocket connections for real-time features"""
    
    def __init__(self):
        """Initialize WebSocket manager"""
        self.active_connections: Dict[str, WebSocket] = {}
        self.game_subscribers: Dict[str, Set[str]] = {}  # game_id -> set of client_ids
        self.client_games: Dict[str, str] = {}  # client_id -> game_id
        self.connection_metadata: Dict[str, Dict[str, Any]] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        """Accept a new WebSocket connection"""
        
        await websocket.accept()
        self.active_connections[client_id] = websocket
        self.connection_metadata[client_id] = {
            "connected_at": datetime.now(),
            "last_activity": datetime.now(),
            "message_count": 0
        }
        
        print(f"Client {client_id} connected. Total connections: {len(self.active_connections)}")
        
        # Send welcome message
        await self.send_personal_message(
            json.dumps({
                "type": "connection_established",
                "client_id": client_id,
                "timestamp": datetime.now().isoformat()
            }),
            client_id
        )
    
    def disconnect(self, client_id: str):
        """Remove a WebSocket connection"""
        
        # Remove from active connections
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # Remove from game subscriptions
        if client_id in self.client_games:
            game_id = self.client_games[client_id]
            if game_id in self.game_subscribers:
                self.game_subscribers[game_id].discard(client_id)
                
                # Clean up empty game subscription
                if not self.game_subscribers[game_id]:
                    del self.game_subscribers[game_id]
            
            del self.client_games[client_id]
        
        # Remove metadata
        if client_id in self.connection_metadata:
            del self.connection_metadata[client_id]
        
        print(f"Client {client_id} disconnected. Total connections: {len(self.active_connections)}")
    
    async def send_personal_message(self, message: str, client_id: str):
        """Send message to a specific client"""
        
        if client_id in self.active_connections:
            try:
                websocket = self.active_connections[client_id]
                await websocket.send_text(message)
                
                # Update metadata
                if client_id in self.connection_metadata:
                    self.connection_metadata[client_id]["last_activity"] = datetime.now()
                    self.connection_metadata[client_id]["message_count"] += 1
                
            except Exception as e:
                print(f"Error sending message to {client_id}: {str(e)}")
                # Remove disconnected client
                self.disconnect(client_id)
    
    async def broadcast(self, message: str):
        """Broadcast message to all connected clients"""
        
        if not self.active_connections:
            return
        
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message)
                
                # Update metadata
                if client_id in self.connection_metadata:
                    self.connection_metadata[client_id]["last_activity"] = datetime.now()
                    self.connection_metadata[client_id]["message_count"] += 1
                
            except Exception as e:
                print(f"Error broadcasting to {client_id}: {str(e)}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    async def broadcast_to_game(self, message: str, game_id: str):
        """Broadcast message to all clients subscribed to a specific game"""
        
        if game_id not in self.game_subscribers:
            return
        
        subscribers = self.game_subscribers[game_id].copy()
        disconnected_clients = []
        
        for client_id in subscribers:
            if client_id in self.active_connections:
                try:
                    websocket = self.active_connections[client_id]
                    await websocket.send_text(message)
                    
                    # Update metadata
                    if client_id in self.connection_metadata:
                        self.connection_metadata[client_id]["last_activity"] = datetime.now()
                        self.connection_metadata[client_id]["message_count"] += 1
                    
                except Exception as e:
                    print(f"Error broadcasting to game subscriber {client_id}: {str(e)}")
                    disconnected_clients.append(client_id)
            else:
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            self.disconnect(client_id)
    
    def subscribe_to_game(self, client_id: str, game_id: str):
        """Subscribe a client to game updates"""
        
        # Remove from previous game if any
        if client_id in self.client_games:
            old_game_id = self.client_games[client_id]
            if old_game_id in self.game_subscribers:
                self.game_subscribers[old_game_id].discard(client_id)
        
        # Add to new game
        if game_id not in self.game_subscribers:
            self.game_subscribers[game_id] = set()
        
        self.game_subscribers[game_id].add(client_id)
        self.client_games[client_id] = game_id
        
        print(f"Client {client_id} subscribed to game {game_id}")
    
    def unsubscribe_from_game(self, client_id: str):
        """Unsubscribe a client from game updates"""
        
        if client_id in self.client_games:
            game_id = self.client_games[client_id]
            
            if game_id in self.game_subscribers:
                self.game_subscribers[game_id].discard(client_id)
                
                # Clean up empty game subscription
                if not self.game_subscribers[game_id]:
                    del self.game_subscribers[game_id]
            
            del self.client_games[client_id]
            print(f"Client {client_id} unsubscribed from game {game_id}")
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return len(self.active_connections)
    
    def get_game_subscriber_count(self, game_id: str) -> int:
        """Get number of subscribers for a specific game"""
        return len(self.game_subscribers.get(game_id, set()))
    
    def get_connection_info(self, client_id: str) -> Dict[str, Any]:
        """Get connection information for a client"""
        
        if client_id not in self.connection_metadata:
            return {}
        
        metadata = self.connection_metadata[client_id].copy()
        metadata["is_connected"] = client_id in self.active_connections
        metadata["subscribed_game"] = self.client_games.get(client_id)
        
        return metadata
    
    def get_all_connections_info(self) -> Dict[str, Any]:
        """Get information about all connections"""
        
        return {
            "total_connections": len(self.active_connections),
            "total_games_with_subscribers": len(self.game_subscribers),
            "connections": {
                client_id: self.get_connection_info(client_id)
                for client_id in self.active_connections.keys()
            }
        }
    
    async def send_ping_to_all(self):
        """Send ping to all connections to check connectivity"""
        
        ping_message = json.dumps({
            "type": "ping",
            "timestamp": datetime.now().isoformat()
        })
        
        await self.broadcast(ping_message)
    
    async def handle_message(self, client_id: str, message: str):
        """Handle incoming WebSocket message"""
        
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "subscribe_game":
                game_id = data.get("game_id")
                if game_id:
                    self.subscribe_to_game(client_id, game_id)
                    
                    # Send confirmation
                    await self.send_personal_message(
                        json.dumps({
                            "type": "subscription_confirmed",
                            "game_id": game_id
                        }),
                        client_id
                    )
            
            elif message_type == "unsubscribe_game":
                self.unsubscribe_from_game(client_id)
                
                # Send confirmation
                await self.send_personal_message(
                    json.dumps({
                        "type": "unsubscription_confirmed"
                    }),
                    client_id
                )
            
            elif message_type == "pong":
                # Handle pong response
                if client_id in self.connection_metadata:
                    self.connection_metadata[client_id]["last_activity"] = datetime.now()
            
            else:
                # Handle other message types
                print(f"Unhandled message type '{message_type}' from client {client_id}")
        
        except json.JSONDecodeError:
            print(f"Invalid JSON message from client {client_id}: {message}")
        except Exception as e:
            print(f"Error handling message from client {client_id}: {str(e)}")
    
    async def cleanup_inactive_connections(self, max_inactive_minutes: int = 30):
        """Clean up connections that haven't been active recently"""
        
        from datetime import timedelta
        
        cutoff_time = datetime.now() - timedelta(minutes=max_inactive_minutes)
        inactive_clients = []
        
        for client_id, metadata in self.connection_metadata.items():
            last_activity = metadata.get("last_activity", datetime.now())
            
            if last_activity < cutoff_time:
                inactive_clients.append(client_id)
        
        # Disconnect inactive clients
        for client_id in inactive_clients:
            if client_id in self.active_connections:
                try:
                    websocket = self.active_connections[client_id]
                    await websocket.close(code=1000, reason="Inactive connection")
                except:
                    pass
                
                self.disconnect(client_id)
        
        return len(inactive_clients)