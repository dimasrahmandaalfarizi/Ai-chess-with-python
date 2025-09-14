/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        // Chess board colors
        "board-light": "#f0d9b5",
        "board-dark": "#b58863",
        "board-highlight": "#ffff00",
        "board-selected": "#20b2aa",
        "board-legal": "#90ee90",
        "board-check": "#ff6b6b",

        // Brand colors
        primary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#3b82f6",
          600: "#2563eb",
          700: "#1d4ed8",
          800: "#1e40af",
          900: "#1e3a8a",
        },

        // Evaluation colors
        "eval-winning": "#22c55e",
        "eval-advantage": "#84cc16",
        "eval-equal": "#6b7280",
        "eval-disadvantage": "#f59e0b",
        "eval-losing": "#ef4444",
      },

      fontFamily: {
        chess: ["Chess Cases", "serif"],
        mono: ["JetBrains Mono", "Consolas", "Monaco", "monospace"],
      },

      animation: {
        "piece-move": "piece-move 0.3s ease-in-out",
        "piece-capture": "piece-capture 0.4s ease-in-out",
        "check-flash": "check-flash 1s ease-in-out infinite",
        "eval-pulse": "eval-pulse 2s ease-in-out infinite",
      },

      keyframes: {
        "piece-move": {
          "0%": { transform: "scale(1)" },
          "50%": { transform: "scale(1.1)" },
          "100%": { transform: "scale(1)" },
        },
        "piece-capture": {
          "0%": { transform: "scale(1) rotate(0deg)", opacity: "1" },
          "50%": { transform: "scale(1.2) rotate(180deg)", opacity: "0.5" },
          "100%": { transform: "scale(0) rotate(360deg)", opacity: "0" },
        },
        "check-flash": {
          "0%, 100%": { backgroundColor: "rgba(239, 68, 68, 0.3)" },
          "50%": { backgroundColor: "rgba(239, 68, 68, 0.7)" },
        },
        "eval-pulse": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.7" },
        },
      },

      boxShadow: {
        piece: "0 2px 4px rgba(0, 0, 0, 0.2)",
        "piece-hover": "0 4px 8px rgba(0, 0, 0, 0.3)",
        board: "0 8px 32px rgba(0, 0, 0, 0.2)",
      },

      spacing: {
        square: "3.5rem", // Standard chess square size
        board: "28rem", // 8 * square size
      },
    },
  },
  plugins: [],
};
