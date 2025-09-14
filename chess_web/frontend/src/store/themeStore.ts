import { create } from "zustand";
import { persist } from "zustand/middleware";
import { BoardTheme, PieceSet, UserPreferences } from "@types/index";
import { storageUtils } from "@utils/index";

// Default themes
const defaultBoardThemes: BoardTheme[] = [
  {
    id: "classic",
    name: "Classic",
    lightSquares: "#f0d9b5",
    darkSquares: "#b58863",
    coordinates: "#8b4513",
    border: "#654321",
  },
  {
    id: "modern",
    name: "Modern",
    lightSquares: "#eeeed2",
    darkSquares: "#769656",
    coordinates: "#4a5c2a",
    border: "#2d3d1a",
  },
  {
    id: "blue",
    name: "Blue Ocean",
    lightSquares: "#e6f3ff",
    darkSquares: "#4a90e2",
    coordinates: "#2c5aa0",
    border: "#1a3d73",
  },
  {
    id: "purple",
    name: "Royal Purple",
    lightSquares: "#f3e6ff",
    darkSquares: "#8e44ad",
    coordinates: "#5d2e6b",
    border: "#3d1a47",
  },
  {
    id: "green",
    name: "Forest Green",
    lightSquares: "#e8f5e8",
    darkSquares: "#27ae60",
    coordinates: "#1e7e34",
    border: "#155724",
  },
];

const defaultPieceSets: PieceSet[] = [
  {
    id: "classic",
    name: "Classic",
    pieces: {
      "white-king": "♔",
      "white-queen": "♕",
      "white-rook": "♖",
      "white-bishop": "♗",
      "white-knight": "♘",
      "white-pawn": "♙",
      "black-king": "♚",
      "black-queen": "♛",
      "black-rook": "♜",
      "black-bishop": "♝",
      "black-knight": "♞",
      "black-pawn": "♟",
    },
  },
  {
    id: "modern",
    name: "Modern",
    pieces: {
      "white-king": "🤴",
      "white-queen": "👸",
      "white-rook": "🏰",
      "white-bishop": "⛪",
      "white-knight": "🐎",
      "white-pawn": "👤",
      "black-king": "♚",
      "black-queen": "♛",
      "black-rook": "♜",
      "black-bishop": "♝",
      "black-knight": "♞",
      "black-pawn": "♟",
    },
  },
];

const defaultPreferences: UserPreferences = {
  boardTheme: "classic",
  pieceSet: "classic",
  showCoordinates: true,
  showLegalMoves: true,
  enableSounds: true,
  animationSpeed: "normal",
  autoQueen: false,
  confirmMoves: false,
  darkMode: false,
};

interface ThemeState {
  isDarkMode: boolean;
  currentTheme: BoardTheme;
  currentPieceSet: PieceSet;
  preferences: UserPreferences;
  availableThemes: BoardTheme[];
  availablePieceSets: PieceSet[];

  // Actions
  toggleDarkMode: () => void;
  setTheme: (themeId: string) => void;
  setPieceSet: (pieceSetId: string) => void;
  updatePreferences: (preferences: Partial<UserPreferences>) => void;
  resetToDefaults: () => void;
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      isDarkMode: defaultPreferences.darkMode,
      currentTheme: defaultBoardThemes[0],
      currentPieceSet: defaultPieceSets[0],
      preferences: defaultPreferences,
      availableThemes: defaultBoardThemes,
      availablePieceSets: defaultPieceSets,

      toggleDarkMode: () => {
        set((state) => {
          const newDarkMode = !state.isDarkMode;

          // Update document class for Tailwind dark mode
          if (newDarkMode) {
            document.documentElement.classList.add("dark");
          } else {
            document.documentElement.classList.remove("dark");
          }

          return {
            isDarkMode: newDarkMode,
            preferences: {
              ...state.preferences,
              darkMode: newDarkMode,
            },
          };
        });
      },

      setTheme: (themeId: string) => {
        set((state) => {
          const theme = state.availableThemes.find((t) => t.id === themeId);
          if (!theme) return state;

          return {
            currentTheme: theme,
            preferences: {
              ...state.preferences,
              boardTheme: themeId,
            },
          };
        });
      },

      setPieceSet: (pieceSetId: string) => {
        set((state) => {
          const pieceSet = state.availablePieceSets.find(
            (p) => p.id === pieceSetId
          );
          if (!pieceSet) return state;

          return {
            currentPieceSet: pieceSet,
            preferences: {
              ...state.preferences,
              pieceSet: pieceSetId,
            },
          };
        });
      },

      updatePreferences: (newPreferences: Partial<UserPreferences>) => {
        set((state) => {
          const updatedPreferences = {
            ...state.preferences,
            ...newPreferences,
          };

          // Update theme if changed
          let newState: Partial<ThemeState> = {
            preferences: updatedPreferences,
          };

          if (
            newPreferences.boardTheme &&
            newPreferences.boardTheme !== state.preferences.boardTheme
          ) {
            const theme = state.availableThemes.find(
              (t) => t.id === newPreferences.boardTheme
            );
            if (theme) {
              newState.currentTheme = theme;
            }
          }

          if (
            newPreferences.pieceSet &&
            newPreferences.pieceSet !== state.preferences.pieceSet
          ) {
            const pieceSet = state.availablePieceSets.find(
              (p) => p.id === newPreferences.pieceSet
            );
            if (pieceSet) {
              newState.currentPieceSet = pieceSet;
            }
          }

          if (
            newPreferences.darkMode !== undefined &&
            newPreferences.darkMode !== state.isDarkMode
          ) {
            newState.isDarkMode = newPreferences.darkMode;

            // Update document class
            if (newPreferences.darkMode) {
              document.documentElement.classList.add("dark");
            } else {
              document.documentElement.classList.remove("dark");
            }
          }

          return newState;
        });
      },

      resetToDefaults: () => {
        set({
          isDarkMode: defaultPreferences.darkMode,
          currentTheme: defaultBoardThemes[0],
          currentPieceSet: defaultPieceSets[0],
          preferences: defaultPreferences,
        });

        // Reset document class
        document.documentElement.classList.remove("dark");
      },
    }),
    {
      name: "chess-theme-store",
      partialize: (state) => ({
        isDarkMode: state.isDarkMode,
        preferences: state.preferences,
      }),
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Apply dark mode class on hydration
          if (state.isDarkMode) {
            document.documentElement.classList.add("dark");
          }

          // Set current theme and piece set based on preferences
          const theme = defaultBoardThemes.find(
            (t) => t.id === state.preferences.boardTheme
          );
          const pieceSet = defaultPieceSets.find(
            (p) => p.id === state.preferences.pieceSet
          );

          if (theme) state.currentTheme = theme;
          if (pieceSet) state.currentPieceSet = pieceSet;
        }
      },
    }
  )
);

// Theme Provider Component
import React, { createContext, useContext, useEffect } from "react";

const ThemeContext = createContext<ThemeState | null>(null);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const themeStore = useThemeStore();

  useEffect(() => {
    // Initialize theme on mount
    if (themeStore.isDarkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [themeStore.isDarkMode]);

  return (
    <ThemeContext.Provider value={themeStore}>{children}</ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
};
