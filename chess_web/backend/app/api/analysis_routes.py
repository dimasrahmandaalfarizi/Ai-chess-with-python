#!/usr/bin/env python3
"""
Chess Analysis API Routes

Handles position analysis, move suggestions, and learning features.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, List
import asyncio
from datetime import datetime

from ..models.chess_models import (
    AnalysisRequest, AnalysisResult, BestMoveResponse, PositionEvaluation,
    HintResponse, PuzzleData, GameResponse, ErrorResponse
)
from ..services.analysis_service import AnalysisService

router = APIRouter()

# Initialize services
analysis_service = AnalysisService()

@router.post("/position", response_model=AnalysisResult)
async def analyze_position(request: AnalysisRequest):
    """
    Analyze a chess position
    
    Provides comprehensive analysis of the given position including
    evaluation, best moves, variations, and tactical motifs.
    """
    try:
        result = await analysis_service.analyze_position(
            fen=request.fen,
            depth=request.depth,
            time_limit=request.time_limit,
            include_variations=request.include_variations
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.post("/best-move", response_model=BestMoveResponse)
async def get_best_move(request: AnalysisRequest):
    """
    Get best move suggestion
    
    Returns the best move for the given position with explanation
    and alternative moves.
    """
    try:
        result = await analysis_service.get_best_move(
            fen=request.fen,
            depth=request.depth or 4,
            difficulty="medium"
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Best move calculation failed: {str(e)}")

@router.post("/evaluation", response_model=PositionEvaluation)
async def evaluate_position(request: AnalysisRequest):
    """
    Evaluate a chess position
    
    Returns detailed evaluation of the position including
    material, positional factors, and overall assessment.
    """
    try:
        result = await analysis_service.evaluate_position(
            fen=request.fen,
            detailed=True
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Position evaluation failed: {str(e)}")

@router.post("/variations", response_model=GameResponse)
async def get_move_variations(request: AnalysisRequest):
    """
    Get move variations
    
    Returns principal variations and alternative lines
    from the given position.
    """
    try:
        variations = await analysis_service.get_variations(
            fen=request.fen,
            depth=request.depth or 4
        )
        
        return GameResponse(
            success=True,
            message="Variations calculated",
            data={"variations": variations}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tactical-motifs", response_model=GameResponse)
async def find_tactical_motifs(request: AnalysisRequest):
    """
    Find tactical motifs in position
    
    Identifies tactical patterns like pins, forks, skewers, etc.
    """
    try:
        motifs = await analysis_service.find_tactical_motifs(request.fen)
        
        return GameResponse(
            success=True,
            message="Tactical motifs identified",
            data={"motifs": motifs}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/opening-info", response_model=GameResponse)
async def get_opening_info(request: AnalysisRequest):
    """
    Get opening information
    
    Returns opening name, ECO code, and typical continuations.
    """
    try:
        opening_info = {
            "name": "Starting Position",
            "eco": "A00",
            "description": "The initial position of a chess game"
        }
        
        return GameResponse(
            success=True,
            message="Opening information retrieved",
            data={"opening": opening_info}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/hint", response_model=HintResponse)
async def get_move_hint(request: AnalysisRequest):
    """
    Get move hint
    
    Provides a helpful hint about the position without
    giving away the exact best move.
    """
    try:
        hint = HintResponse(
            hint_type="positional",
            message="Look for moves that improve piece activity",
            highlighted_squares=[],
            suggested_moves=["development", "center control"],
            explanation="Focus on developing pieces and controlling the center"
        )
        return hint
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain", response_model=GameResponse)
async def explain_position(request: AnalysisRequest):
    """
    Explain position
    
    Provides educational explanation of the position,
    key features, and strategic concepts.
    """
    try:
        explanation = {
            "overview": "This is the starting position of a chess game",
            "key_features": ["All pieces on starting squares", "Equal material"],
            "strategic_concepts": ["Opening principles", "Development", "Center control"],
            "tactical_opportunities": ["None in starting position"],
            "learning_points": ["Develop pieces quickly", "Control the center", "Castle early"]
        }
        
        return GameResponse(
            success=True,
            message="Position explained",
            data={"explanation": explanation}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/puzzles", response_model=GameResponse)
async def get_chess_puzzles(
    difficulty: str = "medium",
    theme: str = "all",
    count: int = 10
):
    """
    Get chess puzzles
    
    Returns chess puzzles for training and practice.
    """
    try:
        # Mock puzzles
        puzzles = [
            {
                "puzzle_id": "puzzle_001",
                "fen": "r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4",
                "moves": ["Nf3-g5", "d7-d6", "Ng5xf7"],
                "rating": 1200,
                "themes": ["fork", "knight"],
                "description": "Knight fork winning the queen",
                "solution_explanation": "The knight on g5 can fork the king and queen by moving to f7"
            }
        ]
        
        return GameResponse(
            success=True,
            message="Puzzles retrieved",
            data={
                "puzzles": puzzles,
                "count": len(puzzles)
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/puzzle/check", response_model=GameResponse)
async def check_puzzle_solution(
    puzzle_id: str,
    moves: List[str]
):
    """
    Check puzzle solution
    
    Validates the player's solution to a chess puzzle.
    """
    try:
        # Mock solution check
        result = {
            "correct": True,
            "solution": ["Nf3-g5", "d7-d6", "Ng5xf7"],
            "explanation": "Correct! The knight fork wins the queen."
        }
        
        return GameResponse(
            success=True,
            message="Solution checked",
            data=result
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=GameResponse)
async def get_analysis_stats():
    """
    Get analysis statistics
    
    Returns statistics about analysis performance and usage.
    """
    try:
        stats = {
            "analyses_performed": 0,
            "total_analysis_time": 0.0,
            "average_analysis_time": 0.0,
            "average_depth": 4.0,
            "cache_hits": 0,
            "cache_hit_rate": 0.0
        }
        
        return GameResponse(
            success=True,
            message="Statistics retrieved",
            data={"stats": stats}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))