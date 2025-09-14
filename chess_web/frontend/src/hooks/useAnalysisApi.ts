import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  PositionAnalysis,
  BestMove,
  Difficulty,
  ChessPuzzle,
  ApiResponse,
} from "@types/index";
import { apiService } from "@services/api";
import toast from "react-hot-toast";

// Query Keys
export const analysisQueryKeys = {
  all: ["analysis"] as const,
  positions: () => [...analysisQueryKeys.all, "positions"] as const,
  position: (fen: string, depth: number) =>
    [...analysisQueryKeys.positions(), { fen, depth }] as const,
  bestMoves: () => [...analysisQueryKeys.all, "best-moves"] as const,
  bestMove: (fen: string, depth: number, difficulty: Difficulty) =>
    [...analysisQueryKeys.bestMoves(), { fen, depth, difficulty }] as const,
  evaluations: () => [...analysisQueryKeys.all, "evaluations"] as const,
  evaluation: (fen: string) =>
    [...analysisQueryKeys.evaluations(), fen] as const,
  puzzles: () => [...analysisQueryKeys.all, "puzzles"] as const,
  puzzle: (difficulty: string, theme: string, count: number) =>
    [...analysisQueryKeys.puzzles(), { difficulty, theme, count }] as const,
  stats: () => [...analysisQueryKeys.all, "stats"] as const,
};

// Analyze Position Hook
export function useAnalyzePosition() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: {
      fen: string;
      depth?: number;
      timeLimit?: number;
      includeVariations?: boolean;
    }) => {
      return await apiService.analyzePosition(
        params.fen,
        params.depth || 4,
        params.timeLimit || 5.0,
        params.includeVariations !== false
      );
    },
    onSuccess: (data, variables) => {
      // Cache the analysis result
      queryClient.setQueryData(
        analysisQueryKeys.position(variables.fen, variables.depth || 4),
        data
      );
    },
    onError: (error: any) => {
      console.error("Failed to analyze position:", error);
      toast.error(error.response?.data?.message || "Analysis failed");
    },
  });
}

// Get Cached Position Analysis Hook
export function usePositionAnalysis(
  fen: string | undefined,
  depth: number = 4,
  enabled: boolean = true
) {
  return useQuery({
    queryKey: analysisQueryKeys.position(fen || "", depth),
    queryFn: async () => {
      if (!fen) throw new Error("FEN is required");
      return await apiService.analyzePosition(fen, depth);
    },
    enabled: enabled && !!fen,
    staleTime: 1000 * 60 * 5, // 5 minutes
    onError: (error: any) => {
      console.error("Failed to fetch position analysis:", error);
    },
  });
}

// Get Best Move Hook
export function useGetBestMove() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: {
      fen: string;
      depth?: number;
      difficulty?: Difficulty;
    }) => {
      return await apiService.getBestMove(
        params.fen,
        params.depth || 4,
        params.difficulty || "medium"
      );
    },
    onSuccess: (data, variables) => {
      // Cache the best move result
      queryClient.setQueryData(
        analysisQueryKeys.bestMove(
          variables.fen,
          variables.depth || 4,
          variables.difficulty || "medium"
        ),
        data
      );
    },
    onError: (error: any) => {
      console.error("Failed to get best move:", error);
      toast.error(error.response?.data?.message || "Failed to get best move");
    },
  });
}

// Evaluate Position Hook
export function useEvaluatePosition() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: { fen: string; detailed?: boolean }) => {
      return await apiService.evaluatePosition(
        params.fen,
        params.detailed !== false
      );
    },
    onSuccess: (data, variables) => {
      // Cache the evaluation result
      queryClient.setQueryData(
        analysisQueryKeys.evaluation(variables.fen),
        data
      );
    },
    onError: (error: any) => {
      console.error("Failed to evaluate position:", error);
      toast.error(error.response?.data?.message || "Evaluation failed");
    },
  });
}

// Get Variations Hook
export function useGetVariations() {
  return useMutation({
    mutationFn: async (params: { fen: string; depth?: number }) => {
      return await apiService.getVariations(params.fen, params.depth || 4);
    },
    onError: (error: any) => {
      console.error("Failed to get variations:", error);
      toast.error(error.response?.data?.message || "Failed to get variations");
    },
  });
}

// Find Tactical Motifs Hook
export function useFindTacticalMotifs() {
  return useMutation({
    mutationFn: async (fen: string) => {
      return await apiService.findTacticalMotifs(fen);
    },
    onError: (error: any) => {
      console.error("Failed to find tactical motifs:", error);
      toast.error(
        error.response?.data?.message || "Failed to find tactical motifs"
      );
    },
  });
}

// Get Opening Info Hook
export function useGetOpeningInfo() {
  return useMutation({
    mutationFn: async (fen: string) => {
      return await apiService.getOpeningInfo(fen);
    },
    onError: (error: any) => {
      console.error("Failed to get opening info:", error);
      toast.error(
        error.response?.data?.message || "Failed to get opening info"
      );
    },
  });
}

// Get Move Hint Hook
export function useGetMoveHint() {
  return useMutation({
    mutationFn: async (fen: string) => {
      return await apiService.getMoveHint(fen);
    },
    onSuccess: (data) => {
      if (data.success && data.data) {
        toast.success("Hint: " + data.data.message, { duration: 5000 });
      }
    },
    onError: (error: any) => {
      console.error("Failed to get move hint:", error);
      toast.error(error.response?.data?.message || "Failed to get hint");
    },
  });
}

// Explain Position Hook
export function useExplainPosition() {
  return useMutation({
    mutationFn: async (fen: string) => {
      return await apiService.explainPosition(fen);
    },
    onError: (error: any) => {
      console.error("Failed to explain position:", error);
      toast.error(
        error.response?.data?.message || "Failed to explain position"
      );
    },
  });
}

// Check for Blunders Hook
export function useCheckForBlunders() {
  return useMutation({
    mutationFn: async (fen: string) => {
      return await apiService.checkForBlunders(fen);
    },
    onSuccess: (data) => {
      if (data.success && data.data?.blunders?.length > 0) {
        toast.warning(
          `${data.data.blunders.length} potential blunder(s) detected`
        );
      }
    },
    onError: (error: any) => {
      console.error("Failed to check for blunders:", error);
      toast.error(
        error.response?.data?.message || "Failed to check for blunders"
      );
    },
  });
}

// Compare Moves Hook
export function useCompareMoves() {
  return useMutation({
    mutationFn: async (params: { fen: string; moves: string[] }) => {
      return await apiService.compareMoves(params.fen, params.moves);
    },
    onError: (error: any) => {
      console.error("Failed to compare moves:", error);
      toast.error(error.response?.data?.message || "Failed to compare moves");
    },
  });
}

// Get Puzzles Hook
export function useGetPuzzles(
  difficulty: string = "medium",
  theme: string = "all",
  count: number = 10,
  enabled: boolean = true
) {
  return useQuery({
    queryKey: analysisQueryKeys.puzzle(difficulty, theme, count),
    queryFn: async () => {
      return await apiService.getPuzzles(difficulty, theme, count);
    },
    enabled,
    staleTime: 1000 * 60 * 10, // 10 minutes
    onError: (error: any) => {
      console.error("Failed to fetch puzzles:", error);
      toast.error("Failed to load puzzles");
    },
  });
}

// Check Puzzle Solution Hook
export function useCheckPuzzleSolution() {
  return useMutation({
    mutationFn: async (params: { puzzleId: string; moves: string[] }) => {
      return await apiService.checkPuzzleSolution(
        params.puzzleId,
        params.moves
      );
    },
    onSuccess: (data) => {
      if (data.success && data.data) {
        if (data.data.correct) {
          toast.success("Correct solution! 🎉");
        } else {
          toast.error("Incorrect. Try again!");
        }
      }
    },
    onError: (error: any) => {
      console.error("Failed to check puzzle solution:", error);
      toast.error(error.response?.data?.message || "Failed to check solution");
    },
  });
}

// Get Analysis Statistics Hook
export function useAnalysisStats(enabled: boolean = true) {
  return useQuery({
    queryKey: analysisQueryKeys.stats(),
    queryFn: async () => {
      return await apiService.getAnalysisStats();
    },
    enabled,
    staleTime: 1000 * 60 * 5, // 5 minutes
    refetchInterval: 1000 * 60, // 1 minute
    onError: (error: any) => {
      console.error("Failed to fetch analysis stats:", error);
    },
  });
}

// Auto-Analysis Hook (for real-time analysis)
export function useAutoAnalysis(
  fen: string | undefined,
  enabled: boolean = false,
  depth: number = 4
) {
  const analyzePosition = useAnalyzePosition();

  // Auto-trigger analysis when FEN changes
  React.useEffect(() => {
    if (enabled && fen && !analyzePosition.isPending) {
      const timeoutId = setTimeout(() => {
        analyzePosition.mutate({ fen, depth });
      }, 500); // Debounce for 500ms

      return () => clearTimeout(timeoutId);
    }
  }, [fen, enabled, depth, analyzePosition]);

  return analyzePosition;
}

// Import React for useEffect
import React from "react";
