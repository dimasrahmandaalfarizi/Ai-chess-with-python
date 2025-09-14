import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Play,
  Pause,
  RotateCcw,
  Settings,
  Crown,
  Clock,
  User,
  Bot,
} from "lucide-react";
import { motion } from "framer-motion";
import toast from "react-hot-toast";

// Components
import ChessBoard from "@components/chess/ChessBoard";
import GameControls from "@components/chess/GameControls";
import MoveHistory from "@components/chess/MoveHistory";
import AnalysisPanel from "@components/analysis/AnalysisPanel";

// Hooks
import {
  useCreateGame,
  useGameState,
  useMakeMove,
  useGetAiMove,
  useUndoMove,
} from "@hooks/useGameApi";
import { useAnalyzePosition } from "@hooks/useAnalysisApi";
import { useWebSocket } from "@services/websocket";

// Types
import {
  ChessMove,
  GameMode,
  Difficulty,
  PieceColor,
  ChessPosition,
} from "@types/index";
import { chessUtils } from "@utils/index";

const GamePage: React.FC = () => {
  const { gameId } = useParams<{ gameId?: string }>();
  const navigate = useNavigate();

  // State
  const [currentGameId, setCurrentGameId] = useState<string | undefined>(
    gameId
  );
  const [boardOrientation, setBoardOrientation] = useState<PieceColor>("white");
  const [isAnalysisMode, setIsAnalysisMode] = useState(false);
  const [gameSettings, setGameSettings] = useState({
    mode: "human_vs_ai" as GameMode,
    difficulty: "medium" as Difficulty,
    playerColor: "white" as PieceColor,
  });

  // API Hooks
  const createGame = useCreateGame();
  const { data: gameData, isLoading: gameLoading } = useGameState(
    currentGameId,
    !!currentGameId
  );
  const makeMove = useMakeMove();
  const getAiMove = useGetAiMove();
  const undoMove = useUndoMove();
  const analyzePosition = useAnalyzePosition();

  // WebSocket
  const { connect, subscribeToGame, subscribe, isConnected } = useWebSocket();

  // Game state
  const gameState = gameData?.data?.game_state;
  const currentPosition: ChessPosition | undefined = gameState
    ? {
        fen: gameState.fen,
        pgn: gameState.pgn,
        moveNumber: gameState.moveNumber,
        turn: gameState.turn,
        isCheck: gameState.isCheck,
        isCheckmate: gameState.isCheckmate,
        isStalemate: gameState.isStalemate,
        isDraw: gameState.isDraw,
      }
    : undefined;

  // Initialize WebSocket connection
  useEffect(() => {
    if (!isConnected) {
      connect().catch(console.error);
    }
  }, [connect, isConnected]);

  // Subscribe to game updates
  useEffect(() => {
    if (currentGameId && isConnected) {
      subscribeToGame(currentGameId);

      const unsubscribe = subscribe("game_update", (data) => {
        console.log("Game update received:", data);
        // Game state will be updated via React Query
      });

      return unsubscribe;
    }
  }, [currentGameId, isConnected, subscribeToGame, subscribe]);

  // Auto-analysis
  useEffect(() => {
    if (isAnalysisMode && currentPosition) {
      analyzePosition.mutate({
        fen: currentPosition.fen,
        depth: 4,
        includeVariations: true,
      });
    }
  }, [currentPosition?.fen, isAnalysisMode]);

  // Handle new game creation
  const handleNewGame = async () => {
    try {
      const result = await createGame.mutateAsync({
        mode: gameSettings.mode,
        difficulty: gameSettings.difficulty,
        playerColor: gameSettings.playerColor,
      });

      if (result.success && result.data) {
        setCurrentGameId(result.data.gameId);
        navigate(`/game/${result.data.gameId}`);
        toast.success("New game started!");
      }
    } catch (error) {
      console.error("Failed to create game:", error);
    }
  };

  // Handle move
  const handleMove = async (move: ChessMove) => {
    if (!currentGameId || !gameState) return;

    try {
      await makeMove.mutateAsync({
        gameId: currentGameId,
        move: move.uci,
        promotion: move.promotion,
      });

      // If playing against AI and it's AI's turn, get AI move
      if (
        gameSettings.mode === "human_vs_ai" &&
        gameState.turn !== gameSettings.playerColor
      ) {
        setTimeout(async () => {
          try {
            await getAiMove.mutateAsync(currentGameId);
          } catch (error) {
            console.error("AI move failed:", error);
          }
        }, 500); // Small delay for better UX
      }
    } catch (error) {
      console.error("Move failed:", error);
    }
  };

  // Handle undo
  const handleUndo = async () => {
    if (!currentGameId) return;

    try {
      await undoMove.mutateAsync(currentGameId);
    } catch (error) {
      console.error("Undo failed:", error);
    }
  };

  // Handle board flip
  const handleFlipBoard = () => {
    setBoardOrientation((prev) => (prev === "white" ? "black" : "white"));
  };

  // Handle game controls
  const handleResign = () => {
    toast.error("Game resigned");
    // TODO: Implement resign logic
  };

  const handleOfferDraw = () => {
    toast.info("Draw offered");
    // TODO: Implement draw offer logic
  };

  // Loading state
  if (gameLoading && currentGameId) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400">Loading game...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <Crown className="h-8 w-8 text-primary-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Chess Game
              </h1>
              {gameState && (
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Game ID: {currentGameId} • {gameState.status}
                </p>
              )}
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Analysis Mode Toggle */}
            <button
              onClick={() => setIsAnalysisMode(!isAnalysisMode)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                isAnalysisMode
                  ? "bg-primary-600 text-white"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600"
              }`}
            >
              Analysis Mode
            </button>

            {/* New Game Button */}
            <button
              onClick={handleNewGame}
              disabled={createGame.isPending}
              className="btn btn-primary"
            >
              <Play className="h-4 w-4 mr-2" />
              New Game
            </button>
          </div>
        </div>

        {/* Game Content */}
        {currentPosition && gameState ? (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* Left Panel - Game Controls */}
            <div className="lg:col-span-1 space-y-6">
              <GameControls
                gameState={gameState}
                onNewGame={handleNewGame}
                onUndo={handleUndo}
                onRedo={() => {}} // TODO: Implement redo
                onFlipBoard={handleFlipBoard}
                onResign={handleResign}
                onOfferDraw={handleOfferDraw}
              />

              {/* Player Info */}
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4">
                <h3 className="font-semibold text-gray-900 dark:text-white mb-4">
                  Players
                </h3>

                <div className="space-y-3">
                  {/* Black Player */}
                  <div
                    className={`flex items-center space-x-3 p-3 rounded-lg ${
                      gameState.turn === "black"
                        ? "bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800"
                        : "bg-gray-50 dark:bg-gray-700"
                    }`}
                  >
                    {gameSettings.playerColor === "black" ? (
                      <User className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                    ) : (
                      <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                    )}
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 dark:text-white">
                        {gameSettings.playerColor === "black"
                          ? "You"
                          : "AI Engine"}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        Black
                      </div>
                    </div>
                    {gameState.turn === "black" && (
                      <Clock className="h-4 w-4 text-primary-600" />
                    )}
                  </div>

                  {/* White Player */}
                  <div
                    className={`flex items-center space-x-3 p-3 rounded-lg ${
                      gameState.turn === "white"
                        ? "bg-primary-50 dark:bg-primary-900/20 border border-primary-200 dark:border-primary-800"
                        : "bg-gray-50 dark:bg-gray-700"
                    }`}
                  >
                    {gameSettings.playerColor === "white" ? (
                      <User className="h-5 w-5 text-gray-600 dark:text-gray-400" />
                    ) : (
                      <Bot className="h-5 w-5 text-blue-600 dark:text-blue-400" />
                    )}
                    <div className="flex-1">
                      <div className="font-medium text-gray-900 dark:text-white">
                        {gameSettings.playerColor === "white"
                          ? "You"
                          : "AI Engine"}
                      </div>
                      <div className="text-sm text-gray-500 dark:text-gray-400">
                        White
                      </div>
                    </div>
                    {gameState.turn === "white" && (
                      <Clock className="h-4 w-4 text-primary-600" />
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Center - Chess Board */}
            <div className="lg:col-span-2 flex justify-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
              >
                <ChessBoard
                  position={currentPosition}
                  onMove={handleMove}
                  orientation={boardOrientation}
                  showCoordinates={true}
                  showLegalMoves={true}
                  disabled={makeMove.isPending || getAiMove.isPending}
                />
              </motion.div>
            </div>

            {/* Right Panel */}
            <div className="lg:col-span-1 space-y-6">
              {/* Move History */}
              <MoveHistory
                moves={[]} // TODO: Parse moves from PGN
                currentMoveIndex={-1}
                onMoveSelect={(index) => {
                  // TODO: Implement move navigation
                }}
              />

              {/* Analysis Panel (if enabled) */}
              {isAnalysisMode && (
                <AnalysisPanel
                  analysis={analyzePosition.data?.data}
                  loading={analyzePosition.isPending}
                  onDepthChange={(depth) => {
                    if (currentPosition) {
                      analyzePosition.mutate({
                        fen: currentPosition.fen,
                        depth,
                        includeVariations: true,
                      });
                    }
                  }}
                  onAnalysisRequest={() => {
                    if (currentPosition) {
                      analyzePosition.mutate({
                        fen: currentPosition.fen,
                        depth: 4,
                        includeVariations: true,
                      });
                    }
                  }}
                />
              )}
            </div>
          </div>
        ) : (
          /* No Game State - New Game Setup */
          <div className="max-w-2xl mx-auto">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-8">
              <div className="text-center mb-8">
                <Crown className="h-16 w-16 mx-auto mb-4 text-primary-600" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                  Start a New Game
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  Configure your game settings and begin playing
                </p>
              </div>

              {/* Game Settings */}
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Game Mode
                  </label>
                  <select
                    value={gameSettings.mode}
                    onChange={(e) =>
                      setGameSettings((prev) => ({
                        ...prev,
                        mode: e.target.value as GameMode,
                      }))
                    }
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                  >
                    <option value="human_vs_ai">Human vs AI</option>
                    <option value="analysis">Analysis Mode</option>
                  </select>
                </div>

                {gameSettings.mode === "human_vs_ai" && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Your Color
                      </label>
                      <div className="grid grid-cols-2 gap-3">
                        <button
                          onClick={() =>
                            setGameSettings((prev) => ({
                              ...prev,
                              playerColor: "white",
                            }))
                          }
                          className={`p-3 rounded-lg border-2 transition-colors ${
                            gameSettings.playerColor === "white"
                              ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                              : "border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
                          }`}
                        >
                          <div className="text-center">
                            <div className="text-2xl mb-1">♔</div>
                            <div className="text-sm font-medium">White</div>
                          </div>
                        </button>

                        <button
                          onClick={() =>
                            setGameSettings((prev) => ({
                              ...prev,
                              playerColor: "black",
                            }))
                          }
                          className={`p-3 rounded-lg border-2 transition-colors ${
                            gameSettings.playerColor === "black"
                              ? "border-primary-500 bg-primary-50 dark:bg-primary-900/20"
                              : "border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500"
                          }`}
                        >
                          <div className="text-center">
                            <div className="text-2xl mb-1">♚</div>
                            <div className="text-sm font-medium">Black</div>
                          </div>
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                        AI Difficulty
                      </label>
                      <select
                        value={gameSettings.difficulty}
                        onChange={(e) =>
                          setGameSettings((prev) => ({
                            ...prev,
                            difficulty: e.target.value as Difficulty,
                          }))
                        }
                        className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      >
                        <option value="beginner">Beginner (~800 ELO)</option>
                        <option value="easy">Easy (~1000 ELO)</option>
                        <option value="medium">Medium (~1200 ELO)</option>
                        <option value="hard">Hard (~1400 ELO)</option>
                        <option value="expert">Expert (~1600 ELO)</option>
                      </select>
                    </div>
                  </>
                )}

                <button
                  onClick={handleNewGame}
                  disabled={createGame.isPending}
                  className="w-full btn btn-primary btn-lg"
                >
                  {createGame.isPending ? (
                    <>
                      <div className="spinner mr-2" />
                      Creating Game...
                    </>
                  ) : (
                    <>
                      <Play className="h-5 w-5 mr-2" />
                      Start Game
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default GamePage;
