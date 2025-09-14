// Chess game types
export interface ChessPosition {
  fen: string;
  pgn: string;
  moveNumber: number;
  turn: "white" | "black";
  isCheck: boolean;
  isCheckmate: boolean;
  isStalemate: boolean;
  isDraw: boolean;
}

export interface ChessMove {
  from: string;
  to: string;
  piece: string;
  captured?: string;
  promotion?: string;
  san: string;
  uci: string;
  isCheck: boolean;
  isCheckmate: boolean;
  isCastling: boolean;
  isEnPassant: boolean;
}

export interface GameState {
  gameId: string;
  fen: string;
  pgn: string;
  status: GameStatus;
  turn: PieceColor;
  moveNumber: number;
  halfmoveClockNumber: number;
  legalMoves: string[];
  lastMove?: ChessMove;
  isCheck: boolean;
  isCheckmate: boolean;
  isStalemate: boolean;
  isDraw: boolean;
  result?: string;
}

export type GameStatus =
  | "active"
  | "checkmate"
  | "stalemate"
  | "draw"
  | "resigned"
  | "aborted";
export type PieceColor = "white" | "black";
export type GameMode = "human_vs_ai" | "analysis" | "puzzle" | "study";
export type Difficulty = "beginner" | "easy" | "medium" | "hard" | "expert";

// Analysis types
export interface PositionAnalysis {
  fen: string;
  evaluation: PositionEvaluation;
  bestMoves: BestMove[];
  variations: MoveVariation[];
  tacticalMotifs: string[];
  openingInfo?: OpeningInfo;
  endgameInfo?: EndgameInfo;
  analysisTime: number;
  nodesSearched: number;
}

export interface PositionEvaluation {
  score: number;
  mateIn?: number;
  evaluation: string;
  breakdown?: EvaluationBreakdown;
  bestMove?: string;
}

export interface EvaluationBreakdown {
  material: number;
  position: number;
  kingSafety: number;
  pawnStructure: number;
  mobility: number;
  centerControl: number;
  development: number;
  tempo: number;
  total: number;
}

export interface BestMove {
  move: string;
  san: string;
  evaluation: number;
  confidence: number;
}

export interface MoveVariation {
  moves: string[];
  evaluation: number;
  depth: number;
  description?: string;
}

export interface OpeningInfo {
  name: string;
  eco: string;
  description: string;
  moves: string[];
  popularity: string;
}

export interface EndgameInfo {
  type: string;
  result: string;
  bestPlay: string[];
  difficulty: string;
}

// UI types
export interface BoardTheme {
  id: string;
  name: string;
  lightSquares: string;
  darkSquares: string;
  coordinates: string;
  border: string;
}

export interface PieceSet {
  id: string;
  name: string;
  pieces: Record<string, string>;
}

export interface UserPreferences {
  boardTheme: string;
  pieceSet: string;
  showCoordinates: boolean;
  showLegalMoves: boolean;
  enableSounds: boolean;
  animationSpeed: "slow" | "normal" | "fast";
  autoQueen: boolean;
  confirmMoves: boolean;
  darkMode: boolean;
}

// API types
export interface ApiResponse<T = any> {
  success: boolean;
  message: string;
  data?: T;
  error?: string;
}

export interface GameResponse extends ApiResponse {
  data?: {
    gameId: string;
    gameState: GameState;
  };
}

export interface AnalysisResponse extends ApiResponse {
  data?: PositionAnalysis;
}

export interface MoveResponse extends ApiResponse {
  data?: {
    moveInfo: ChessMove;
    gameState: GameState;
  };
}

// WebSocket types
export interface WebSocketMessage {
  type: string;
  data?: any;
  timestamp?: string;
}

export interface GameUpdateMessage extends WebSocketMessage {
  type: "game_update";
  data: {
    gameId: string;
    gameState: GameState;
    move?: ChessMove;
  };
}

export interface AnalysisUpdateMessage extends WebSocketMessage {
  type: "analysis_update";
  data: {
    fen: string;
    analysis: PositionAnalysis;
  };
}

// Puzzle types
export interface ChessPuzzle {
  puzzleId: string;
  fen: string;
  moves: string[];
  rating: number;
  themes: string[];
  description: string;
  solutionExplanation: string;
}

export interface PuzzleAttempt {
  puzzleId: string;
  moves: string[];
  correct: boolean;
  timeSpent: number;
  hintsUsed: number;
}

// Learning types
export interface LearningModule {
  id: string;
  title: string;
  description: string;
  difficulty: Difficulty;
  topics: string[];
  lessons: Lesson[];
  progress: number;
}

export interface Lesson {
  id: string;
  title: string;
  content: string;
  examples: ChessPosition[];
  exercises: Exercise[];
  completed: boolean;
}

export interface Exercise {
  id: string;
  type: "position" | "puzzle" | "quiz";
  question: string;
  position?: ChessPosition;
  options?: string[];
  correctAnswer: string;
  explanation: string;
}

// Statistics types
export interface GameStatistics {
  totalGames: number;
  wins: number;
  losses: number;
  draws: number;
  winRate: number;
  averageGameLength: number;
  favoriteOpenings: string[];
  commonMistakes: string[];
}

export interface AnalysisStatistics {
  analysesPerformed: number;
  totalAnalysisTime: number;
  averageDepth: number;
  accuracyImprovement: number;
  tacticsFound: number;
  blundersAvoided: number;
}

// Error types
export interface ChessError {
  code: string;
  message: string;
  details?: any;
}

// Utility types
export type Square = string; // e.g., 'e4', 'a1'
export type File = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h";
export type Rank = "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8";
export type PieceType =
  | "pawn"
  | "rook"
  | "knight"
  | "bishop"
  | "queen"
  | "king";

export interface Coordinates {
  file: File;
  rank: Rank;
}

export interface SquareInfo {
  square: Square;
  coordinates: Coordinates;
  color: "light" | "dark";
  piece?: {
    type: PieceType;
    color: PieceColor;
  };
}

// Component prop types
export interface ChessBoardProps {
  position: ChessPosition;
  onMove: (move: ChessMove) => void;
  orientation?: PieceColor;
  showCoordinates?: boolean;
  showLegalMoves?: boolean;
  disabled?: boolean;
  highlightedSquares?: Square[];
  theme?: BoardTheme;
  pieceSet?: PieceSet;
}

export interface MoveHistoryProps {
  moves: ChessMove[];
  currentMoveIndex: number;
  onMoveSelect: (index: number) => void;
}

export interface AnalysisPanelProps {
  analysis?: PositionAnalysis;
  loading?: boolean;
  onDepthChange: (depth: number) => void;
  onAnalysisRequest: () => void;
}

export interface GameControlsProps {
  gameState: GameState;
  onNewGame: () => void;
  onUndo: () => void;
  onRedo: () => void;
  onFlipBoard: () => void;
  onResign: () => void;
  onOfferDraw: () => void;
}

// Store types
export interface GameStore {
  currentGame?: GameState;
  gameHistory: ChessMove[];
  currentMoveIndex: number;
  isLoading: boolean;
  error?: string;

  // Actions
  createGame: (mode: GameMode, difficulty?: Difficulty) => Promise<void>;
  makeMove: (move: ChessMove) => Promise<void>;
  undoMove: () => Promise<void>;
  redoMove: () => Promise<void>;
  loadGame: (gameId: string) => Promise<void>;
  resetGame: () => void;
}

export interface AnalysisStore {
  currentAnalysis?: PositionAnalysis;
  analysisHistory: PositionAnalysis[];
  isAnalyzing: boolean;
  error?: string;

  // Actions
  analyzePosition: (fen: string, depth?: number) => Promise<void>;
  getBestMove: (fen: string) => Promise<BestMove>;
  clearAnalysis: () => void;
}

export interface ThemeStore {
  isDarkMode: boolean;
  currentTheme: BoardTheme;
  currentPieceSet: PieceSet;
  preferences: UserPreferences;

  // Actions
  toggleDarkMode: () => void;
  setTheme: (theme: BoardTheme) => void;
  setPieceSet: (pieceSet: PieceSet) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
}
