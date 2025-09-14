"""
API Response models for Chess AI Helper
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from .chess_models import GameState, Move, PositionAnalysis

class BaseResponse(BaseModel):
    """Base response model"""
    success: bool = True
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: Optional[str] = None

class ErrorResponse(BaseResponse):
    """Error response model"""
    success: bool = False
    error: str
    code: int
    details: Optional[Dict[str, Any]] = None

class GameResponse(BaseResponse):
    """Game-related response"""
    game: GameState

class MoveResponse(BaseResponse):
    """Move-related response"""
    game: GameState
    move: Move
    analysis: Optional[PositionAnalysis] = None

class AnalysisResponse(BaseResponse):
    """Analysis response"""
    analysis: PositionAnalysis
    position: str = Field(..., description="FEN of analyzed position")

class BestMoveResponse(BaseResponse):
    """Best move response"""
    move: Move
    evaluation: float
    depth: int
    alternatives: List[Move] = Field(default_factory=list)

class ExplanationResponse(BaseResponse):
    """Move explanation response"""
    explanation: str
    concepts: List[str] = Field(default_factory=list)
    tactical_motifs: List[str] = Field(default_factory=list)
    strategic_themes: List[str] = Field(default_factory=list)

class EngineInfoResponse(BaseResponse):
    """Engine information response"""
    name: str
    version: str
    author: str
    features: List[str]
    settings: Dict[str, Any]

class EngineStatsResponse(BaseResponse):
    """Engine statistics response"""
    nodes_searched: int
    positions_analyzed: int
    cache_hits: int
    cache_misses: int
    average_depth: float
    uptime: float