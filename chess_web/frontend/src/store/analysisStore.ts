import { create } from "zustand";
import { PositionAnalysis, BestMove } from "@types/index";

interface AnalysisStore {
  currentAnalysis?: PositionAnalysis;
  analysisHistory: PositionAnalysis[];
  isAnalyzing: boolean;
  error?: string;

  // Actions
  analyzePosition: (fen: string, depth?: number) => Promise<void>;
  getBestMove: (fen: string) => Promise<BestMove | null>;
  clearAnalysis: () => void;
  setError: (error: string) => void;
  clearError: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
  analysisHistory: [],
  isAnalyzing: false,

  analyzePosition: async (fen: string, depth: number = 4) => {
    set({ isAnalyzing: true, error: undefined });

    try {
      // TODO: Implement API call to analyze position
      console.log("Analyzing position:", { fen, depth });

      // Mock analysis result
      const mockAnalysis: PositionAnalysis = {
        fen,
        evaluation: {
          score: 0.5,
          evaluation: "equal",
          breakdown: {
            material: 0.0,
            position: 0.3,
            kingSafety: 0.1,
            pawnStructure: 0.1,
            mobility: 0.0,
            centerControl: 0.0,
            development: 0.0,
            tempo: 0.0,
            total: 0.5,
          },
        },
        bestMoves: [
          {
            move: "e2e4",
            san: "e4",
            evaluation: 0.5,
            confidence: 0.8,
          },
        ],
        variations: [
          {
            moves: ["e2e4", "e7e5"],
            evaluation: 0.3,
            depth: 2,
            description: "King's Pawn Opening",
          },
        ],
        tacticalMotifs: [],
        openingInfo: {
          name: "Starting Position",
          eco: "A00",
          description: "The initial position of a chess game",
          moves: [],
          popularity: "100%",
        },
        analysisTime: 1.2,
        nodesSearched: 10000,
      };

      const updatedHistory = [...get().analysisHistory, mockAnalysis];

      set({
        currentAnalysis: mockAnalysis,
        analysisHistory: updatedHistory,
        isAnalyzing: false,
      });
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to analyze position",
        isAnalyzing: false,
      });
    }
  },

  getBestMove: async (fen: string): Promise<BestMove | null> => {
    set({ isAnalyzing: true, error: undefined });

    try {
      // TODO: Implement API call to get best move
      console.log("Getting best move for:", fen);

      // Mock best move
      const bestMove: BestMove = {
        move: "e2e4",
        san: "e4",
        evaluation: 0.5,
        confidence: 0.8,
      };

      set({ isAnalyzing: false });
      return bestMove;
    } catch (error) {
      set({
        error:
          error instanceof Error ? error.message : "Failed to get best move",
        isAnalyzing: false,
      });
      return null;
    }
  },

  clearAnalysis: () => {
    set({
      currentAnalysis: undefined,
      analysisHistory: [],
      isAnalyzing: false,
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

// Analysis Provider Component
import React, { createContext, useContext } from "react";

const AnalysisContext = createContext<AnalysisStore | null>(null);

export const AnalysisProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const analysisStore = useAnalysisStore();

  return (
    <AnalysisContext.Provider value={analysisStore}>
      {children}
    </AnalysisContext.Provider>
  );
};

export const useAnalysis = () => {
  const context = useContext(AnalysisContext);
  if (!context) {
    throw new Error("useAnalysis must be used within an AnalysisProvider");
  }
  return context;
};
