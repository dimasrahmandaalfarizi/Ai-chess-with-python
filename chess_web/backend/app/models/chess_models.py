"""
Chess-related Pydantic models for API requests and responses
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class GameMode(str, Enum):
    """Game mode enumeration"""
    HUMAN_VS_AI = "human_vs_ai"
    ANALYSIS = "analysis"
    PUZZLE = "puzzle"
    STUDY = "study"

class Difficulty(str, Enum):
    """AI difficulty levels"""
    BEGINNER = "beginner"      # ~800 ELO
    EASY = "easy"              # ~1000 ELO
    MEDIUM = "medium"          # ~1200 ELO
    HARD = "hard"              # ~1400 ELO
    EXPERT = "expert"          # ~1600 ELO

class PieceColor(str, Enum):
    """Chess piece colors"""
    WHITE = "white"
    BLACK = "black"

class GameStatus(str, Enum):
    """Game status enumeration"""
    ACTIVE = "active"
    CHECKMATE = "checkmate"
    STALEMATE = "stalemate"
    DRAW = "draw"
    RESIGNED = "resigned"
    ABORTED = "aborted"

class PlayerType(str, Enum):
    """Player type enumeration"""
    HUMAN = "human"
    AI = "ai"

class DifficultyLevel(int, Enum):
    """AI difficulty levels"""
    BEGINNER = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    EXPERT = 5

class Move(BaseModel):
    """Chess move representation"""
    from_square: str = Field(..., description="Source square (e.g., 'e2')")
    to_square: str = Field(..., description="Target square (e.g., 'e4')")
    promotion: Optional[str] = Field(None, description="Promotion piece (q, r, b, n)")
    san: str = Field(..., description="Standard Algebraic Notation")
    uci: str = Field(..., description="Universal Chess Interface notation")
    is_capture: bool = Field(False, description="Whether move captures a piece")
    is_check: bool = Field(False, description="Whether move gives check")
    is_checkmate: bool = Field(False, description="Whether move is checkmate")
    is_castling: bool = Field(False, description="Whether move is castling")
    is_en_passant: bool = Field(False, description="Whether move is en passant")

class GameSettings(BaseModel):
    """Game configuration settings"""
    player_white: PlayerType = PlayerType.HUMAN
    player_black: PlayerType = PlayerType.AI
    ai_difficulty: DifficultyLevel = DifficultyLevel.MEDIUM
    time_control: Optional[Dict[str, int]] = None
    analysis_enabled: bool = True
    hints_enabled: bool = True
    starting_fen: Optional[str] = None

class GameState(BaseModel):
    """Complete game state"""
    id: str
    fen: str = Field(..., description="Current position in FEN notation")
    pgn: str = Field("", description="Game in PGN notation")
    current_player: str = Field(..., description="Current player to move")
    status: GameStatus = GameStatus.ACTIVE
    moves: List[Move] = Field(default_factory=list)
    settings: GameSettings
    created_at: datetime
    updated_at: datetime
    move_count: int = 0
    result: Optional[str] = None

class ChessPosition(BaseModel):
    """Chess position for analysis"""
    fen: str = Field(..., description="Position in FEN notation")
    moves: Optional[List[str]] = Field(None, description="Move history")

class PositionAnalysis(BaseModel):
    """Complete position analysis"""
    evaluation: float = Field(..., description="Position evaluation in centipawns")
    mate: Optional[int] = Field(None, description="Mate in X moves")
    best_move: Optional[Move] = None
    variations: List['Variation'] = Field(default_factory=list)
    depth: int = Field(..., description="Analysis depth")
    nodes: int = Field(..., description="Nodes searched")
    time: float = Field(..., description="Analysis time in seconds")
    evaluation_breakdown: Optional['EvaluationBreakdown'] = None

class Variation(BaseModel):
    """Move variation with evaluation"""
    moves: List[Move]
    evaluation: float
    depth: int
    pv: str = Field(..., description="Principal variation in SAN")
    description: Optional[str] = None

class EvaluationBreakdown(BaseModel):
    """Detailed evaluation breakdown"""
    material: float
    position: float
    king_safety: float
    pawn_structure: float
    mobility: float
    center_control: float
    development: float
    tempo: float
    total: float

class TacticalMotif(BaseModel):
    """Tactical pattern detection"""
    type: str = Field(..., description="Type of tactical motif")
    squares: List[str] = Field(..., description="Squares involved in the motif")
    description: str = Field(..., description="Human-readable description")
    severity: int = Field(..., description="Importance level (1-5)")

class OpeningInfo(BaseModel):
    """Opening information"""
    name: str
    eco_code: str
    moves: List[str]
    description: str
    frequency: float = Field(..., description="How often this opening is played")

class PuzzleData(BaseModel):
    """Chess puzzle data"""
    id: str
    fen: str
    solution: List[str]
    theme: str
    difficulty: int
    rating: int
    description: str

# Request Models
class NewGameRequest(BaseModel):
    """Request to create a new game"""
    mode: GameMode = GameMode.HUMAN_VS_AI
    difficulty: Optional[Difficulty] = Difficulty.MEDIUM
    player_color: Optional[PieceColor] = PieceColor.WHITE
    time_control: Optional[Dict[str, int]] = None
    starting_fen: Optional[str] = None

class MoveRequest(BaseModel):
    """Request to make a move"""
    move: str = Field(..., description="Move in algebraic notation (e.g., 'e2e4')")
    promotion: Optional[str] = Field(None, description="Promotion piece (q, r, b, n)")

class AnalysisRequest(BaseModel):
    """Request for position analysis"""
    fen: str = Field(..., description="Position in FEN notation")
    depth: Optional[int] = Field(4, ge=1, le=10, description="Analysis depth")
    time_limit: Optional[float] = Field(5.0, ge=0.1, le=30.0, description="Time limit in seconds")
    include_variations: Optional[bool] = Field(True, description="Include move variations")

# Response Models
class MoveInfo(BaseModel):
    """Information about a chess move"""
    move: str
    san: str  # Standard Algebraic Notation
    uci: str  # Universal Chess Interface notation
    from_square: str
    to_square: str
    piece: str
    captured: Optional[str] = None
    promotion: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_castling: bool = False
    is_en_passant: bool = False

class GameState(BaseModel):
    """Current game state"""
    game_id: str
    fen: str
    pgn: str
    status: GameStatus
    turn: PieceColor
    move_number: int
    halfmove_clock: int
    legal_moves: List[str]
    last_move: Optional[MoveInfo] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_stalemate: bool = False
    is_draw: bool = False
    result: Optional[str] = None

class EngineInfo(BaseModel):
    """Chess engine information"""
    name: str
    version: str
    author: str
    features: List[str]
    max_depth: int
    nodes_per_second: int
    evaluation_range: Dict[str, float]

class EngineSettings(BaseModel):
    """Engine configuration settings"""
    depth: int = Field(4, ge=1, le=20)
    time_limit: float = Field(5.0, ge=0.1, le=60.0)
    use_opening_book: bool = True
    use_endgame_tablebase: bool = False
    contempt: float = Field(0.0, ge=-2.0, le=2.0)
    randomness: float = Field(0.0, ge=0.0, le=1.0)

class GameResponse(BaseModel):
    """Generic game response"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: str
# Analysis Models
class EvaluationBreakdown(BaseModel):
    """Detailed position evaluation"""
    material: float
    position: float
    king_safety: float
    pawn_structure: float
    mobility: float
    center_control: float
    development: float
    tempo: float
    total: float

class PositionEvaluation(BaseModel):
    """Position evaluation response"""
    score: float
    mate_in: Optional[int] = None
    evaluation: str  # "equal", "slight advantage", "winning", etc.
    breakdown: Optional[EvaluationBreakdown] = None
    best_move: Optional[str] = None

class MoveVariation(BaseModel):
    """Move variation with evaluation"""
    moves: List[str]
    evaluation: float
    depth: int
    description: Optional[str] = None

class AnalysisResult(BaseModel):
    """Complete position analysis"""
    fen: str
    evaluation: PositionEvaluation
    best_moves: List[Dict[str, Any]]
    variations: List[MoveVariation]
    tactical_motifs: List[str]
    opening_info: Optional[Dict[str, str]] = None
    endgame_info: Optional[Dict[str, Any]] = None
    analysis_time: float
    nodes_searched: int

class BestMoveResponse(BaseModel):
    """Best move suggestion response"""
    move: str
    san: str
    evaluation: float
    confidence: float  # 0.0 to 1.0
    explanation: str
    alternatives: List[Dict[str, Any]]
    tactical_theme: Optional[str] = None

class HintResponse(BaseModel):
    """Move hint response"""
    hint_type: str  # "tactical", "positional", "strategic"
    message: str
    highlighted_squares: List[str]
    suggested_moves: List[str]
    explanation: str

class PuzzleData(BaseModel):
    """Chess puzzle data"""
    puzzle_id: str
    fen: str
    moves: List[str]  # Solution moves
    rating: int
    themes: List[str]
    description: str
    solution_explanation: str