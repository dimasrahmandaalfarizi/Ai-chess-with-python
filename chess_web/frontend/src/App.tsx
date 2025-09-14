import React from "react";
import { Routes, Route } from "react-router-dom";
import { DndProvider } from "react-dnd";
import { HTML5Backend } from "react-dnd-html5-backend";

// Layout components
import Layout from "@components/layout/Layout";
import ErrorBoundary from "@components/common/ErrorBoundary";

// Page components
import HomePage from "@components/pages/HomePage";
import GamePage from "@components/pages/GamePage";
import AnalysisPage from "@components/pages/AnalysisPage";
import PuzzlesPage from "@components/pages/PuzzlesPage";
import LearnPage from "@components/pages/LearnPage";
import SettingsPage from "@components/pages/SettingsPage";
import NotFoundPage from "@components/pages/NotFoundPage";

// Providers
import { ThemeProvider } from "@store/themeStore";
import { GameProvider } from "@store/gameStore";
import { AnalysisProvider } from "@store/analysisStore";

function App() {
  return (
    <ErrorBoundary>
      <ThemeProvider>
        <DndProvider backend={HTML5Backend}>
          <GameProvider>
            <AnalysisProvider>
              <Layout>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/game" element={<GamePage />} />
                  <Route path="/game/:gameId" element={<GamePage />} />
                  <Route path="/analysis" element={<AnalysisPage />} />
                  <Route path="/puzzles" element={<PuzzlesPage />} />
                  <Route path="/learn" element={<LearnPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                  <Route path="*" element={<NotFoundPage />} />
                </Routes>
              </Layout>
            </AnalysisProvider>
          </GameProvider>
        </DndProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
}

export default App;
