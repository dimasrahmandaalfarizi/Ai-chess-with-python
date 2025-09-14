import { create } from "zustand";
import { GameState, GameMode, Difficulty, ChessMove } from "@types/index";

interface GameStore {
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
  setError: (error: string) => void;
  clearError: () => void;
}

export const useGameStore = create<GameStore>((set, get) => ({
  gameHistory: [],
  currentMoveIndex: -1,
  isLoading: false,

  createGame: async (mode: GameMode, difficulty?: Difficulty) => {
    set({ isLoading: true, error: undefined });

    try {
      // TODO: Implement API call to create game
      console.log("Creating game:", { mode, difficulty });

      // Mock game state for now
      const mockGameState: GameState = {
        gameId: "mock-game-id",
        fen: "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
        pgn: "",
        status: "active",
        turn: "white",
        moveNumber: 1,
        halfmoveClockNumber: 0,
        legalMoves: [],
        isCheck: false,
        isCheckmate: false,
        isStalemate: false,
        isDraw: false,
      };

      set({
        currentGame: mockGameState,
        gameHistory: [],
        currentMoveIndex: -1,
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to create game",
        isLoading: false,
      });
    }
  },

  makeMove: async (move: ChessMove) => {
    const { currentGame } = get();
    if (!currentGame) return;

    set({ isLoading: true, error: undefined });

    try {
      // TODO: Implement API call to make move
      console.log("Making move:", move);

      // Mock implementation
      const updatedHistory = [...get().gameHistory, move];

      set({
        gameHistory: updatedHistory,
        currentMoveIndex: updatedHistory.length - 1,
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to make move",
        isLoading: false,
      });
    }
  },

  undoMove: async () => {
    const { currentMoveIndex, gameHistory } = get();
    if (currentMoveIndex < 0) return;

    set({ isLoading: true, error: undefined });

    try {
      // TODO: Implement API call to undo move
      console.log("Undoing move");

      set({
        currentMoveIndex: Math.max(-1, currentMoveIndex - 1),
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to undo move",
        isLoading: false,
      });
    }
  },

  redoMove: async () => {
    const { currentMoveIndex, gameHistory } = get();
    if (currentMoveIndex >= gameHistory.length - 1) return;

    set({ isLoading: true, error: undefined });

    try {
      // TODO: Implement API call to redo move
      console.log("Redoing move");

      set({
        currentMoveIndex: Math.min(
          gameHistory.length - 1,
          currentMoveIndex + 1
        ),
        isLoading: false,
      });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to redo move",
        isLoading: false,
      });
    }
  },

  loadGame: async (gameId: string) => {
    set({ isLoading: true, error: undefined });

    try {
      // TODO: Implement API call to load game
      console.log("Loading game:", gameId);

      // Mock implementation
      set({ isLoading: false });
    } catch (error) {
      set({
        error: error instanceof Error ? error.message : "Failed to load game",
        isLoading: false,
      });
    }
  },

  resetGame: () => {
    set({
      currentGame: undefined,
      gameHistory: [],
      currentMoveIndex: -1,
      isLoading: false,
      error: undefined,
    });
  },

  setError: (error: string) => {
    set({ error });
  },

  clearError: () => {
    set({ error: undefined });
  },
}));

// Game Provider Component
import React, { createContext, useContext } from "react";

const GameContext = createContext<GameStore | null>(null);

export const GameProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const gameStore = useGameStore();

  return (
    <GameContext.Provider value={gameStore}>{children}</GameContext.Provider>
  );
};

export const useGame = () => {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error("useGame must be used within a GameProvider");
  }
  return context;
};
