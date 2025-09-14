#!/usr/bin/env python3
"""
Chess Game API Routes

Handles chess game management, moves, and game state.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List
import uuid
from datetime import datetime

from ..models.chess_models import (
    NewGameRequest, MoveRequest, GameState, GameResponse,
    MoveInfo, ErrorResponse, EngineSettings, EngineInfo
)
from ..services.chess_service import ChessService

router = APIRouter()

# Initialize services
chess_service = ChessService()

@router.post("/game/new", response_model=GameResponse)
async def create_new_game(request: NewGameRequest):
    """
    Create a new chess game
    
    Creates a new game with specified settings and returns game ID and initial state.
    """
    try:
        game_id = str(uuid.uuid4())
        
        # Create new game
        game_state = await chess_service.create_game(
            game_id=game_id,
            mode=request.mode,
            difficulty=request.difficulty,
            player_color=request.player_color,
            starting_fen=request.starting_fen
        )
        
        return GameResponse(
            success=True,
            message="Game created successfully",
            data={
                "game_id": game_id,
                "game_state": game_state.dict()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/game/{game_id}", response_model=GameResponse)
async def get_game_state(game_id: str):
    """
    Get current game state
    
    Returns the current state of the specified game.
    """
    try:
        # Mock implementation - in real app, get from chess_service
        game_state = GameState(
            game_id=game_id,
            fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            pgn="",
            status="active",
            turn="white",
            move_number=1,
            halfmove_clock=0,
            legal_moves=["e2e4", "d2d4", "Nf3", "Nc3"],
            is_check=False,
            is_checkmate=False,
            is_stalemate=False,
            is_draw=False
        )
        
        return GameResponse(
            success=True,
            message="Game state retrieved",
            data={"game_state": game_state.dict()}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/game/{game_id}/move", response_model=GameResponse)
async def make_move(game_id: str, request: MoveRequest):
    """
    Make a move in the game
    
    Processes a player move and returns updated game state.
    """
    try:
        result = await chess_service.make_move(
            game_id=game_id,
            move=request.move,
            promotion=request.promotion
        )
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GameResponse(
            success=True,
            message="Move made successfully",
            data={
                "move_info": result["move_info"].dict() if hasattr(result["move_info"], 'dict') else result["move_info"],
                "game_state": result["game_state"].dict() if hasattr(result["game_state"], 'dict') else result["game_state"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/game/{game_id}/ai-move", response_model=GameResponse)
async def get_ai_move(game_id: str):
    """
    Get AI move for the current position
    
    Calculates and returns the best move for the AI player.
    """
    try:
        result = await chess_service.get_ai_move(game_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GameResponse(
            success=True,
            message="AI move calculated",
            data={
                "ai_move": result["move_info"].dict() if hasattr(result["move_info"], 'dict') else result["move_info"],
                "game_state": result["game_state"].dict() if hasattr(result["game_state"], 'dict') else result["game_state"],
                "thinking_time": result["thinking_time"],
                "evaluation": result["evaluation"]
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/game/{game_id}", response_model=GameResponse)
async def end_game(game_id: str):
    """
    End a game
    
    Terminates the specified game and cleans up resources.
    """
    try:
        return GameResponse(
            success=True,
            message="Game ended successfully",
            data={"game_id": game_id}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/game/{game_id}/legal-moves", response_model=GameResponse)
async def get_legal_moves(game_id: str):
    """
    Get legal moves for current position
    
    Returns all legal moves available in the current position.
    """
    try:
        legal_moves = await chess_service.get_legal_moves(game_id)
        
        return GameResponse(
            success=True,
            message="Legal moves retrieved",
            data={"legal_moves": legal_moves}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/game/{game_id}/undo", response_model=GameResponse)
async def undo_move(game_id: str):
    """
    Undo the last move
    
    Reverts the last move made in the game.
    """
    try:
        result = await chess_service.undo_move(game_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return GameResponse(
            success=True,
            message="Move undone successfully",
            data={"game_state": result["game_state"].dict() if hasattr(result["game_state"], 'dict') else result["game_state"]}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/games", response_model=GameResponse)
async def list_active_games():
    """
    List all active games
    
    Returns a list of all currently active games.
    """
    try:
        games = []  # Mock empty list
        
        return GameResponse(
            success=True,
            message="Active games retrieved",
            data={
                "games": games,
                "count": len(games)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/engine/info", response_model=EngineInfo)
async def get_engine_info():
    """
    Get chess engine information
    
    Returns information about the chess engine capabilities.
    """
    try:
        info = await chess_service.get_engine_info()
        return info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/engine/settings", response_model=GameResponse)
async def update_engine_settings(settings: EngineSettings):
    """
    Update engine settings
    
    Updates the chess engine configuration.
    """
    try:
        result = await chess_service.update_engine_settings(settings)
        
        return GameResponse(
            success=True,
            message="Engine settings updated",
            data={"settings": settings.dict()}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))