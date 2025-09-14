import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  GameMode,
  Difficulty,
  GameState,
  ChessMove,
  ApiResponse,
  GameResponse,
  MoveResponse,
} from "@types/index";
import { apiService } from "@services/api";
import toast from "react-hot-toast";

// Query Keys
export const gameQueryKeys = {
  all: ["games"] as const,
  lists: () => [...gameQueryKeys.all, "list"] as const,
  list: (filters: string) => [...gameQueryKeys.lists(), { filters }] as const,
  details: () => [...gameQueryKeys.all, "detail"] as const,
  detail: (id: string) => [...gameQueryKeys.details(), id] as const,
  legalMoves: (id: string) =>
    [...gameQueryKeys.detail(id), "legal-moves"] as const,
};

// Create Game Hook
export function useCreateGame() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: {
      mode: GameMode;
      difficulty?: Difficulty;
      playerColor?: "white" | "black";
      startingFen?: string;
    }) => {
      const response = await apiService.createGame(
        params.mode,
        params.difficulty,
        params.playerColor,
        params.startingFen
      );
      return response;
    },
    onSuccess: (data) => {
      // Invalidate games list
      queryClient.invalidateQueries({ queryKey: gameQueryKeys.lists() });

      // Add new game to cache
      if (data.success && data.data) {
        queryClient.setQueryData(gameQueryKeys.detail(data.data.gameId), data);
      }

      toast.success("Game created successfully!");
    },
    onError: (error: any) => {
      console.error("Failed to create game:", error);
      toast.error(error.response?.data?.message || "Failed to create game");
    },
  });
}

// Get Game State Hook
export function useGameState(
  gameId: string | undefined,
  enabled: boolean = true
) {
  return useQuery({
    queryKey: gameQueryKeys.detail(gameId || ""),
    queryFn: async () => {
      if (!gameId) throw new Error("Game ID is required");
      return await apiService.getGameState(gameId);
    },
    enabled: enabled && !!gameId,
    staleTime: 1000 * 30, // 30 seconds
    refetchInterval: (data) => {
      // Auto-refetch if game is active
      if (data?.data?.game_state?.status === "active") {
        return 1000 * 10; // 10 seconds
      }
      return false;
    },
    onError: (error: any) => {
      console.error("Failed to fetch game state:", error);
      toast.error("Failed to load game");
    },
  });
}

// Make Move Hook
export function useMakeMove() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (params: {
      gameId: string;
      move: string;
      promotion?: string;
    }) => {
      return await apiService.makeMove(
        params.gameId,
        params.move,
        params.promotion
      );
    },
    onSuccess: (data, variables) => {
      // Update game state in cache
      queryClient.setQueryData(
        gameQueryKeys.detail(variables.gameId),
        (oldData: GameResponse | undefined) => {
          if (oldData && data.success && data.data) {
            return {
              ...oldData,
              data: {
                ...oldData.data,
                game_state: data.data.gameState,
              },
            };
          }
          return oldData;
        }
      );

      // Invalidate legal moves
      queryClient.invalidateQueries({
        queryKey: gameQueryKeys.legalMoves(variables.gameId),
      });
    },
    onError: (error: any) => {
      console.error("Failed to make move:", error);
      toast.error(error.response?.data?.message || "Invalid move");
    },
  });
}

// Get AI Move Hook
export function useGetAiMove() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (gameId: string) => {
      return await apiService.getAiMove(gameId);
    },
    onSuccess: (data, gameId) => {
      // Update game state in cache
      queryClient.setQueryData(
        gameQueryKeys.detail(gameId),
        (oldData: GameResponse | undefined) => {
          if (oldData && data.success && data.data) {
            return {
              ...oldData,
              data: {
                ...oldData.data,
                game_state: data.data.gameState,
              },
            };
          }
          return oldData;
        }
      );

      // Invalidate legal moves
      queryClient.invalidateQueries({
        queryKey: gameQueryKeys.legalMoves(gameId),
      });
    },
    onError: (error: any) => {
      console.error("Failed to get AI move:", error);
      toast.error(error.response?.data?.message || "AI move failed");
    },
  });
}

// Undo Move Hook
export function useUndoMove() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (gameId: string) => {
      return await apiService.undoMove(gameId);
    },
    onSuccess: (data, gameId) => {
      // Update game state in cache
      queryClient.setQueryData(gameQueryKeys.detail(gameId), data);

      // Invalidate legal moves
      queryClient.invalidateQueries({
        queryKey: gameQueryKeys.legalMoves(gameId),
      });

      toast.success("Move undone");
    },
    onError: (error: any) => {
      console.error("Failed to undo move:", error);
      toast.error(error.response?.data?.message || "Cannot undo move");
    },
  });
}

// Get Legal Moves Hook
export function useLegalMoves(
  gameId: string | undefined,
  enabled: boolean = true
) {
  return useQuery({
    queryKey: gameQueryKeys.legalMoves(gameId || ""),
    queryFn: async () => {
      if (!gameId) throw new Error("Game ID is required");
      return await apiService.getLegalMoves(gameId);
    },
    enabled: enabled && !!gameId,
    staleTime: 1000 * 10, // 10 seconds
    onError: (error: any) => {
      console.error("Failed to fetch legal moves:", error);
    },
  });
}

// End Game Hook
export function useEndGame() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (gameId: string) => {
      return await apiService.endGame(gameId);
    },
    onSuccess: (data, gameId) => {
      // Remove game from cache
      queryClient.removeQueries({ queryKey: gameQueryKeys.detail(gameId) });

      // Invalidate games list
      queryClient.invalidateQueries({ queryKey: gameQueryKeys.lists() });

      toast.success("Game ended");
    },
    onError: (error: any) => {
      console.error("Failed to end game:", error);
      toast.error(error.response?.data?.message || "Failed to end game");
    },
  });
}

// List Active Games Hook
export function useActiveGames(enabled: boolean = true) {
  return useQuery({
    queryKey: gameQueryKeys.lists(),
    queryFn: async () => {
      return await apiService.listActiveGames();
    },
    enabled,
    staleTime: 1000 * 60, // 1 minute
    refetchInterval: 1000 * 30, // 30 seconds
    onError: (error: any) => {
      console.error("Failed to fetch active games:", error);
    },
  });
}

// Engine Info Hook
export function useEngineInfo() {
  return useQuery({
    queryKey: ["engine", "info"],
    queryFn: async () => {
      return await apiService.getEngineInfo();
    },
    staleTime: 1000 * 60 * 5, // 5 minutes
    onError: (error: any) => {
      console.error("Failed to fetch engine info:", error);
    },
  });
}

// Update Engine Settings Hook
export function useUpdateEngineSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (settings: any) => {
      return await apiService.updateEngineSettings(settings);
    },
    onSuccess: () => {
      // Invalidate engine info
      queryClient.invalidateQueries({ queryKey: ["engine", "info"] });
      toast.success("Engine settings updated");
    },
    onError: (error: any) => {
      console.error("Failed to update engine settings:", error);
      toast.error(error.response?.data?.message || "Failed to update settings");
    },
  });
}
