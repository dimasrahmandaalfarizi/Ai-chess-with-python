#!/usr/bin/env python3
"""
WebSocket Routes

Handles WebSocket connections for real-time communication.
"""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio
from datetime import datetime

from ..services.websocket_manager import WebSocketManager
from ..services.chess_service import ChessService
from ..services.analysis_service import AnalysisService

router = APIRouter()

# Initialize services
websocket_manager = WebSocketManager()
chess_service = ChessService()
analysis_service = AnalysisService()

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await websocket_manager.connect(websocket, client_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            message_type = message.get("type")
            
            if message_type == "subscribe_game":
                game_id = message.get("data", {}).get("game_id")
                if game_id:
                    websocket_manager.subscribe_to_game(client_id, game_id)
            
            elif message_type == "unsubscribe_game":
                websocket_manager.unsubscribe_from_game(client_id)
            
            elif message_type == "analysis_request":
                fen = message.get("data", {}).get("fen")
                depth = message.get("data", {}).get("depth", 4)
                
                if fen:
                    try:
                        result = await analysis_service.analyze_position(
                            fen=fen,
                            depth=depth,
                            time_limit=5.0,
                            include_variations=True
                        )
                        
                        await websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "analysis_result",
                                "data": result.dict() if hasattr(result, 'dict') else result
                            }),
                            client_id
                        )
                    except Exception as e:
                        await websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "data": {"message": str(e)}
                            }),
                            client_id
                        )
            
            elif message_type == "move_request":
                game_id = message.get("data", {}).get("game_id")
                move = message.get("data", {}).get("move")
                
                if game_id and move:
                    try:
                        result = await chess_service.make_move(game_id, move)
                        
                        # Broadcast to all game subscribers
                        await websocket_manager.broadcast_to_game(
                            json.dumps({
                                "type": "move_made",
                                "data": {
                                    "game_id": game_id,
                                    "move": result
                                }
                            }),
                            game_id
                        )
                    except Exception as e:
                        await websocket_manager.send_personal_message(
                            json.dumps({
                                "type": "error",
                                "data": {"message": str(e)}
                            }),
                            client_id
                        )
            
            elif message_type == "ping":
                await websocket_manager.send_personal_message(
                    json.dumps({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    }),
                    client_id
                )
            
            else:
                # Handle unknown message types
                await websocket_manager.send_personal_message(
                    json.dumps({
                        "type": "error",
                        "data": {"message": f"Unknown message type: {message_type}"}
                    }),
                    client_id
                )
                
    except WebSocketDisconnect:
        websocket_manager.disconnect(client_id)
    except Exception as e:
        print(f"WebSocket error for client {client_id}: {str(e)}")
        websocket_manager.disconnect(client_id)

@router.get("/ws/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return websocket_manager.get_all_connections_info()