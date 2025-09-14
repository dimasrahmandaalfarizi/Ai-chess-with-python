import axios, { AxiosInstance, AxiosResponse } from "axios";
import {
  ApiResponse,
  GameResponse,
  AnalysisResponse,
  MoveResponse,
  GameMode,
  Difficulty,
  ChessMove,
  PositionAnalysis,
  BestMove,
  ChessPuzzle,
} from "@types/index";

// API Configuration
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add auth token if available
        const token = localStorage.getItem("auth_token");
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }

        console.log(
          `API Request: ${config.method?.toUpperCase()} ${config.url}`
        );
        return config;
      },
      (error) => {
        console.error("API Request Error:", error);
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        console.log(`API Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error) => {
        console.error(
          "API Response Error:",
          error.response?.data || error.message
        );

        // Handle common errors
        if (error.response?.status === 401) {
          // Unauthorized - clear token and redirect to login
          localStorage.removeItem("auth_token");
          window.location.href = "/login";
        }

        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<ApiResponse> {
    const response = await this.client.get("/api/health");
    return response.data;
  }

  // Game Management APIs
  async createGame(
    mode: GameMode,
    difficulty?: Difficulty,
    playerColor?: "white" | "black",
    startingFen?: string
  ): Promise<GameResponse> {
    const response = await this.client.post("/api/chess/game/new", {
      mode,
      difficulty,
      player_color: playerColor,
      starting_fen: startingFen,
    });
    return response.data;
  }

  async getGameState(gameId: string): Promise<GameResponse> {
    const response = await this.client.get(`/api/chess/game/${gameId}`);
    return response.data;
  }

  async makeMove(
    gameId: string,
    move: string,
    promotion?: string
  ): Promise<MoveResponse> {
    const response = await this.client.post(`/api/chess/game/${gameId}/move`, {
      move,
      promotion,
    });
    return response.data;
  }

  async getAiMove(gameId: string): Promise<MoveResponse> {
    const response = await this.client.post(
      `/api/chess/game/${gameId}/ai-move`
    );
    return response.data;
  }

  async undoMove(gameId: string): Promise<GameResponse> {
    const response = await this.client.post(`/api/chess/game/${gameId}/undo`);
    return response.data;
  }

  async getLegalMoves(gameId: string): Promise<ApiResponse<string[]>> {
    const response = await this.client.get(
      `/api/chess/game/${gameId}/legal-moves`
    );
    return response.data;
  }

  async endGame(gameId: string): Promise<GameResponse> {
    const response = await this.client.delete(`/api/chess/game/${gameId}`);
    return response.data;
  }

  async listActiveGames(): Promise<ApiResponse> {
    const response = await this.client.get("/api/chess/games");
    return response.data;
  }

  // Analysis APIs
  async analyzePosition(
    fen: string,
    depth: number = 4,
    timeLimit: number = 5.0,
    includeVariations: boolean = true
  ): Promise<AnalysisResponse> {
    const response = await this.client.post("/api/analysis/position", {
      fen,
      depth,
      time_limit: timeLimit,
      include_variations: includeVariations,
    });
    return response.data;
  }

  async getBestMove(
    fen: string,
    depth: number = 4,
    difficulty: Difficulty = "medium"
  ): Promise<ApiResponse<BestMove>> {
    const response = await this.client.post("/api/analysis/best-move", {
      fen,
      depth,
      difficulty,
    });
    return response.data;
  }

  async evaluatePosition(
    fen: string,
    detailed: boolean = true
  ): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/evaluation", {
      fen,
      detailed,
    });
    return response.data;
  }

  async getVariations(fen: string, depth: number = 4): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/variations", {
      fen,
      depth,
    });
    return response.data;
  }

  async findTacticalMotifs(fen: string): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/tactical-motifs", {
      fen,
    });
    return response.data;
  }

  async getOpeningInfo(fen: string): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/opening-info", {
      fen,
    });
    return response.data;
  }

  async getMoveHint(fen: string): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/hint", {
      fen,
    });
    return response.data;
  }

  async explainPosition(fen: string): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/explain", {
      fen,
    });
    return response.data;
  }

  async checkForBlunders(fen: string): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/blunder-check", {
      fen,
    });
    return response.data;
  }

  async compareMoves(fen: string, moves: string[]): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/compare-moves", {
      fen,
      moves,
    });
    return response.data;
  }

  // Learning APIs
  async getPuzzles(
    difficulty: string = "medium",
    theme: string = "all",
    count: number = 10
  ): Promise<ApiResponse<ChessPuzzle[]>> {
    const response = await this.client.get("/api/analysis/puzzles", {
      params: { difficulty, theme, count },
    });
    return response.data;
  }

  async checkPuzzleSolution(
    puzzleId: string,
    moves: string[]
  ): Promise<ApiResponse> {
    const response = await this.client.post("/api/analysis/puzzle/check", {
      puzzle_id: puzzleId,
      moves,
    });
    return response.data;
  }

  // Engine Management
  async getEngineInfo(): Promise<ApiResponse> {
    const response = await this.client.get("/api/chess/engine/info");
    return response.data;
  }

  async updateEngineSettings(settings: any): Promise<ApiResponse> {
    const response = await this.client.post(
      "/api/chess/engine/settings",
      settings
    );
    return response.data;
  }

  // Statistics
  async getAnalysisStats(): Promise<ApiResponse> {
    const response = await this.client.get("/api/analysis/stats");
    return response.data;
  }
}

// Create singleton instance
export const apiService = new ApiService();

// Export individual methods for convenience
export const {
  healthCheck,
  createGame,
  getGameState,
  makeMove,
  getAiMove,
  undoMove,
  getLegalMoves,
  endGame,
  listActiveGames,
  analyzePosition,
  getBestMove,
  evaluatePosition,
  getVariations,
  findTacticalMotifs,
  getOpeningInfo,
  getMoveHint,
  explainPosition,
  checkForBlunders,
  compareMoves,
  getPuzzles,
  checkPuzzleSolution,
  getEngineInfo,
  updateEngineSettings,
  getAnalysisStats,
} = apiService;

export default apiService;
