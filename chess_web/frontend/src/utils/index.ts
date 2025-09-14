import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { Square, Coordinates, File, Rank, PieceColor } from "@types/index";

/**
 * Utility function to merge Tailwind CSS classes
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Chess utility functions
 */
export const chessUtils = {
  /**
   * Convert square notation to coordinates
   */
  squareToCoordinates(square: Square): Coordinates {
    const file = square[0] as File;
    const rank = square[1] as Rank;
    return { file, rank };
  },

  /**
   * Convert coordinates to square notation
   */
  coordinatesToSquare(coordinates: Coordinates): Square {
    return `${coordinates.file}${coordinates.rank}` as Square;
  },

  /**
   * Get square color (light or dark)
   */
  getSquareColor(square: Square): "light" | "dark" {
    const { file, rank } = this.squareToCoordinates(square);
    const fileIndex = file.charCodeAt(0) - "a".charCodeAt(0);
    const rankIndex = parseInt(rank) - 1;
    return (fileIndex + rankIndex) % 2 === 0 ? "dark" : "light";
  },

  /**
   * Get all squares on the board
   */
  getAllSquares(): Square[] {
    const squares: Square[] = [];
    for (let rank = 1; rank <= 8; rank++) {
      for (let file = 0; file < 8; file++) {
        const fileChar = String.fromCharCode("a".charCodeAt(0) + file) as File;
        squares.push(`${fileChar}${rank}` as Square);
      }
    }
    return squares;
  },

  /**
   * Flip square for board orientation
   */
  flipSquare(square: Square): Square {
    const { file, rank } = this.squareToCoordinates(square);
    const flippedFile = String.fromCharCode(
      "h".charCodeAt(0) - (file.charCodeAt(0) - "a".charCodeAt(0))
    ) as File;
    const flippedRank = (9 - parseInt(rank)).toString() as Rank;
    return `${flippedFile}${flippedRank}` as Square;
  },

  /**
   * Get distance between two squares
   */
  getSquareDistance(square1: Square, square2: Square): number {
    const coord1 = this.squareToCoordinates(square1);
    const coord2 = this.squareToCoordinates(square2);

    const fileDistance = Math.abs(
      coord1.file.charCodeAt(0) - coord2.file.charCodeAt(0)
    );
    const rankDistance = Math.abs(
      parseInt(coord1.rank) - parseInt(coord2.rank)
    );

    return Math.max(fileDistance, rankDistance);
  },

  /**
   * Check if square is on the board
   */
  isValidSquare(square: string): square is Square {
    if (square.length !== 2) return false;
    const file = square[0];
    const rank = square[1];
    return file >= "a" && file <= "h" && rank >= "1" && rank <= "8";
  },

  /**
   * Parse UCI move notation
   */
  parseUciMove(
    uci: string
  ): { from: Square; to: Square; promotion?: string } | null {
    if (uci.length < 4) return null;

    const from = uci.slice(0, 2) as Square;
    const to = uci.slice(2, 4) as Square;
    const promotion = uci.length > 4 ? uci[4] : undefined;

    if (!this.isValidSquare(from) || !this.isValidSquare(to)) return null;

    return { from, to, promotion };
  },

  /**
   * Format move time
   */
  formatMoveTime(seconds: number): string {
    if (seconds < 60) {
      return `${seconds.toFixed(1)}s`;
    }
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toFixed(0).padStart(2, "0")}`;
  },

  /**
   * Get piece symbol for display
   */
  getPieceSymbol(piece: string, color: PieceColor): string {
    const symbols = {
      white: {
        king: "♔",
        queen: "♕",
        rook: "♖",
        bishop: "♗",
        knight: "♘",
        pawn: "♙",
      },
      black: {
        king: "♚",
        queen: "♛",
        rook: "♜",
        bishop: "♝",
        knight: "♞",
        pawn: "♟",
      },
    };

    return symbols[color][piece as keyof typeof symbols.white] || "";
  },
};

/**
 * Evaluation utility functions
 */
export const evaluationUtils = {
  /**
   * Format evaluation score for display
   */
  formatScore(score: number): string {
    if (Math.abs(score) > 9000) {
      const mateIn = Math.ceil((10000 - Math.abs(score)) / 2);
      return score > 0 ? `+M${mateIn}` : `-M${mateIn}`;
    }

    const centipawns = score / 100;
    return centipawns > 0 ? `+${centipawns.toFixed(1)}` : centipawns.toFixed(1);
  },

  /**
   * Get evaluation description
   */
  getEvaluationDescription(score: number): string {
    if (Math.abs(score) > 9000) {
      return score > 0 ? "White is winning" : "Black is winning";
    }

    if (score > 500) return "White has a winning advantage";
    if (score > 200) return "White has a significant advantage";
    if (score > 50) return "White has a slight advantage";
    if (score > -50) return "Equal position";
    if (score > -200) return "Black has a slight advantage";
    if (score > -500) return "Black has a significant advantage";
    return "Black has a winning advantage";
  },

  /**
   * Get evaluation color class
   */
  getEvaluationColor(score: number): string {
    if (Math.abs(score) > 9000) return "text-red-600";
    if (Math.abs(score) > 500) return "text-red-500";
    if (Math.abs(score) > 200) return "text-orange-500";
    if (Math.abs(score) > 50) return "text-yellow-500";
    return "text-gray-500";
  },

  /**
   * Calculate evaluation bar percentage
   */
  getEvaluationPercentage(score: number): number {
    // Normalize score to 0-100 range
    const maxScore = 1000; // Cap at 10 pawns advantage
    const normalizedScore = Math.max(-maxScore, Math.min(maxScore, score));
    return ((normalizedScore + maxScore) / (2 * maxScore)) * 100;
  },
};

/**
 * Time utility functions
 */
export const timeUtils = {
  /**
   * Format duration in milliseconds to human readable format
   */
  formatDuration(ms: number): string {
    const seconds = Math.floor(ms / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);

    if (hours > 0) {
      return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
    }
    if (minutes > 0) {
      return `${minutes}m ${seconds % 60}s`;
    }
    return `${seconds}s`;
  },

  /**
   * Format timestamp to relative time
   */
  formatRelativeTime(timestamp: string | Date): string {
    const date =
      typeof timestamp === "string" ? new Date(timestamp) : timestamp;
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();

    const diffSeconds = Math.floor(diffMs / 1000);
    const diffMinutes = Math.floor(diffSeconds / 60);
    const diffHours = Math.floor(diffMinutes / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffDays > 0) return `${diffDays} day${diffDays > 1 ? "s" : ""} ago`;
    if (diffHours > 0)
      return `${diffHours} hour${diffHours > 1 ? "s" : ""} ago`;
    if (diffMinutes > 0)
      return `${diffMinutes} minute${diffMinutes > 1 ? "s" : ""} ago`;
    return "Just now";
  },

  /**
   * Format clock time (mm:ss)
   */
  formatClockTime(seconds: number): string {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, "0")}`;
  },
};

/**
 * Storage utility functions
 */
export const storageUtils = {
  /**
   * Get item from localStorage with JSON parsing
   */
  getItem<T>(key: string, defaultValue: T): T {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : defaultValue;
    } catch {
      return defaultValue;
    }
  },

  /**
   * Set item in localStorage with JSON stringification
   */
  setItem<T>(key: string, value: T): void {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error("Failed to save to localStorage:", error);
    }
  },

  /**
   * Remove item from localStorage
   */
  removeItem(key: string): void {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error("Failed to remove from localStorage:", error);
    }
  },

  /**
   * Clear all items from localStorage
   */
  clear(): void {
    try {
      localStorage.clear();
    } catch (error) {
      console.error("Failed to clear localStorage:", error);
    }
  },
};

/**
 * URL utility functions
 */
export const urlUtils = {
  /**
   * Create shareable game URL
   */
  createGameUrl(gameId: string): string {
    return `${window.location.origin}/game/${gameId}`;
  },

  /**
   * Create analysis URL with FEN
   */
  createAnalysisUrl(fen: string): string {
    const encodedFen = encodeURIComponent(fen);
    return `${window.location.origin}/analysis?fen=${encodedFen}`;
  },

  /**
   * Parse FEN from URL parameters
   */
  getFenFromUrl(): string | null {
    const params = new URLSearchParams(window.location.search);
    return params.get("fen");
  },

  /**
   * Copy text to clipboard
   */
  async copyToClipboard(text: string): Promise<boolean> {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch {
      // Fallback for older browsers
      const textArea = document.createElement("textarea");
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      const success = document.execCommand("copy");
      document.body.removeChild(textArea);
      return success;
    }
  },
};

/**
 * Validation utility functions
 */
export const validationUtils = {
  /**
   * Validate FEN string
   */
  isValidFen(fen: string): boolean {
    const fenRegex =
      /^([rnbqkpRNBQKP1-8]+\/){7}[rnbqkpRNBQKP1-8]+\s[bw]\s(-|[KQkq]+)\s(-|[a-h][36])\s\d+\s\d+$/;
    return fenRegex.test(fen);
  },

  /**
   * Validate PGN string
   */
  isValidPgn(pgn: string): boolean {
    // Basic PGN validation - check for move patterns
    const movePattern =
      /\d+\.\s*[NBRQK]?[a-h]?[1-8]?x?[a-h][1-8](?:=[NBRQ])?[+#]?/;
    return movePattern.test(pgn);
  },

  /**
   * Validate email address
   */
  isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  },
};

/**
 * Debounce function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null;

  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * Throttle function
 */
export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;

  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

/**
 * Generate random ID
 */
export function generateId(length: number = 8): string {
  const chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let result = "";
  for (let i = 0; i < length; i++) {
    result += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return result;
}

/**
 * Format file size
 */
export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";

  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

/**
 * Sleep function
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
