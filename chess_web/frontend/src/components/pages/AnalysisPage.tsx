import React, { useState, useEffect } from "react";
import { useSearchParams } from "react-router-dom";
import {
  BarChart3,
  Upload,
  Download,
  Copy,
  Zap,
  BookOpen,
  Target,
  Settings,
  RefreshCw,
} from "lucide-react";
import { motion } from "framer-motion";
import toast from "react-hot-toast";

// Components
import ChessBoard from "@components/chess/ChessBoard";
import AnalysisPanel from "@components/analysis/AnalysisPanel";
import PositionExplanation from "@components/learning/PositionExplanation";
import OpeningExplorer from "@components/learning/OpeningExplorer";

// Hooks
import {
  useAnalyzePosition,
  useGetBestMove,
  useExplainPosition,
  useGetOpeningInfo,
  useGetMoveHint,
} from "@hooks/useAnalysisApi";

// Types
import { ChessMove, ChessPosition } from "@types/index";
import { urlUtils, validationUtils } from "@utils/index";

const AnalysisPage: React.FC = () => {
  const [searchParams, setSearchParams] = useSearchParams();

  // State
  const [currentFen, setCurrentFen] = useState(
    searchParams.get("fen") ||
      "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
  );
  const [fenInput, setFenInput] = useState(currentFen);
  const [boardOrientation, setBoardOrientation] = useState<"white" | "black">(
    "white"
  );
  const [activeTab, setActiveTab] = useState<
    "analysis" | "explanation" | "opening"
  >("analysis");
  const [autoAnalysis, setAutoAnalysis] = useState(true);

  // API Hooks
  const analyzePosition = useAnalyzePosition();
  const getBestMove = useGetBestMove();
  const explainPosition = useExplainPosition();
  const getOpeningInfo = useGetOpeningInfo();
  const getMoveHint = useGetMoveHint();

  // Current position
  const currentPosition: ChessPosition = {
    fen: currentFen,
    pgn: "",
    moveNumber: parseInt(currentFen.split(" ")[5]) || 1,
    turn: currentFen.split(" ")[1] === "w" ? "white" : "black",
    isCheck: false, // TODO: Calculate from FEN
    isCheckmate: false, // TODO: Calculate from FEN
    isStalemate: false, // TODO: Calculate from FEN
    isDraw: false, // TODO: Calculate from FEN
  };

  // Update URL when FEN changes
  useEffect(() => {
    if (currentFen !== searchParams.get("fen")) {
      setSearchParams({ fen: currentFen });
    }
  }, [currentFen, searchParams, setSearchParams]);

  // Auto-analysis
  useEffect(() => {
    if (autoAnalysis && validationUtils.isValidFen(currentFen)) {
      analyzePosition.mutate({
        fen: currentFen,
        depth: 4,
        includeVariations: true,
      });
    }
  }, [currentFen, autoAnalysis]);

  // Handle FEN input
  const handleFenSubmit = () => {
    if (validationUtils.isValidFen(fenInput)) {
      setCurrentFen(fenInput);
      toast.success("Position loaded");
    } else {
      toast.error("Invalid FEN notation");
    }
  };

  // Handle move on board (for analysis)
  const handleMove = (move: ChessMove) => {
    // In analysis mode, we don't actually make moves
    // Instead, we could show what would happen
    toast.info(`Analysis move: ${move.san}`);
  };

  // Load starting position
  const loadStartingPosition = () => {
    const startingFen =
      "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
    setCurrentFen(startingFen);
    setFenInput(startingFen);
  };

  // Import PGN
  const handleImportPGN = () => {
    const input = document.createElement("input");
    input.type = "file";
    input.accept = ".pgn";
    input.onchange = (e) => {
      const file = (e.target as HTMLInputElement).files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const pgn = e.target?.result as string;
          // TODO: Parse PGN and extract final position
          toast.info("PGN import not yet implemented");
        };
        reader.readAsText(file);
      }
    };
    input.click();
  };

  // Export position
  const handleExportFEN = async () => {
    const success = await urlUtils.copyToClipboard(currentFen);
    if (success) {
      toast.success("FEN copied to clipboard");
    } else {
      toast.error("Failed to copy FEN");
    }
  };

  // Share position
  const handleSharePosition = async () => {
    const url = urlUtils.createAnalysisUrl(currentFen);
    const success = await urlUtils.copyToClipboard(url);
    if (success) {
      toast.success("Position URL copied to clipboard");
    } else {
      toast.error("Failed to copy URL");
    }
  };

  const tabs = [
    { id: "analysis", label: "Analysis", icon: BarChart3 },
    { id: "explanation", label: "Explanation", icon: BookOpen },
    { id: "opening", label: "Opening", icon: Target },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="max-w-7xl mx-auto p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-4">
            <BarChart3 className="h-8 w-8 text-primary-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                Position Analysis
              </h1>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Analyze any chess position with AI-powered insights
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-4">
            {/* Auto-analysis toggle */}
            <button
              onClick={() => setAutoAnalysis(!autoAnalysis)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                autoAnalysis
                  ? "bg-green-600 text-white"
                  : "bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-300 dark:hover:bg-gray-600"
              }`}
            >
              Auto Analysis
            </button>

            {/* Import/Export */}
            <div className="flex items-center space-x-2">
              <button
                onClick={handleImportPGN}
                className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
                title="Import PGN"
              >
                <Upload className="h-4 w-4" />
              </button>

              <button
                onClick={handleExportFEN}
                className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
                title="Copy FEN"
              >
                <Copy className="h-4 w-4" />
              </button>

              <button
                onClick={handleSharePosition}
                className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
                title="Share position"
              >
                <Download className="h-4 w-4" />
              </button>
            </div>
          </div>
        </div>

        {/* FEN Input */}
        <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center space-x-4">
            <div className="flex-1">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                FEN Position
              </label>
              <input
                type="text"
                value={fenInput}
                onChange={(e) => setFenInput(e.target.value)}
                placeholder="Enter FEN notation..."
                className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-700 text-gray-900 dark:text-white font-mono text-sm"
              />
            </div>

            <div className="flex items-end space-x-2">
              <button onClick={handleFenSubmit} className="btn btn-primary">
                Load Position
              </button>

              <button
                onClick={loadStartingPosition}
                className="btn btn-secondary"
              >
                Starting Position
              </button>
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Panel - Board */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-gray-900 dark:text-white">
                  Position
                </h3>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() =>
                      setBoardOrientation((prev) =>
                        prev === "white" ? "black" : "white"
                      )
                    }
                    className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
                    title="Flip board"
                  >
                    <RefreshCw className="h-4 w-4" />
                  </button>

                  <button
                    onClick={() => getMoveHint.mutate(currentFen)}
                    disabled={getMoveHint.isPending}
                    className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
                    title="Get hint"
                  >
                    <Zap className="h-4 w-4" />
                  </button>
                </div>
              </div>

              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                className="flex justify-center"
              >
                <ChessBoard
                  position={currentPosition}
                  onMove={handleMove}
                  orientation={boardOrientation}
                  showCoordinates={true}
                  showLegalMoves={false}
                  disabled={false}
                />
              </motion.div>

              {/* Quick Actions */}
              <div className="mt-6 grid grid-cols-2 gap-3">
                <button
                  onClick={() => getBestMove.mutate({ fen: currentFen })}
                  disabled={getBestMove.isPending}
                  className="btn btn-secondary btn-sm"
                >
                  <Target className="h-4 w-4 mr-2" />
                  Best Move
                </button>

                <button
                  onClick={() =>
                    analyzePosition.mutate({ fen: currentFen, depth: 6 })
                  }
                  disabled={analyzePosition.isPending}
                  className="btn btn-secondary btn-sm"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Deep Analysis
                </button>
              </div>
            </div>
          </div>

          {/* Right Panel - Analysis */}
          <div className="lg:col-span-2">
            {/* Tabs */}
            <div className="mb-6">
              <div className="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
                {tabs.map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id as any)}
                      className={`flex-1 flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                        activeTab === tab.id
                          ? "bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 shadow-sm"
                          : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
                      }`}
                    >
                      <Icon className="h-4 w-4 mr-2" />
                      {tab.label}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Tab Content */}
            <div className="space-y-6">
              {activeTab === "analysis" && (
                <AnalysisPanel
                  analysis={analyzePosition.data?.data}
                  loading={analyzePosition.isPending}
                  onDepthChange={(depth) => {
                    analyzePosition.mutate({
                      fen: currentFen,
                      depth,
                      includeVariations: true,
                    });
                  }}
                  onAnalysisRequest={() => {
                    analyzePosition.mutate({
                      fen: currentFen,
                      depth: 4,
                      includeVariations: true,
                    });
                  }}
                />
              )}

              {activeTab === "explanation" && (
                <PositionExplanation
                  fen={currentFen}
                  explanation={explainPosition.data?.data?.explanation}
                  loading={explainPosition.isPending}
                  onRequestExplanation={() =>
                    explainPosition.mutate(currentFen)
                  }
                />
              )}

              {activeTab === "opening" && (
                <OpeningExplorer
                  fen={currentFen}
                  openingInfo={getOpeningInfo.data?.data?.opening}
                  loading={getOpeningInfo.isPending}
                  onRequestOpeningInfo={() => getOpeningInfo.mutate(currentFen)}
                />
              )}
            </div>
          </div>
        </div>

        {/* Best Move Display */}
        {getBestMove.data?.success && getBestMove.data.data && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-6 bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 rounded-lg border border-green-200 dark:border-green-800 p-4"
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <Target className="h-6 w-6 text-green-600 dark:text-green-400" />
                <div>
                  <h4 className="font-semibold text-green-900 dark:text-green-300">
                    Best Move: {getBestMove.data.data.san}
                  </h4>
                  <p className="text-sm text-green-700 dark:text-green-400">
                    Evaluation:{" "}
                    {getBestMove.data.data.evaluation > 0 ? "+" : ""}
                    {getBestMove.data.data.evaluation.toFixed(2)} • Confidence:{" "}
                    {Math.round(getBestMove.data.data.confidence * 100)}%
                  </p>
                </div>
              </div>

              <button
                onClick={() => getBestMove.reset()}
                className="text-green-600 dark:text-green-400 hover:text-green-800 dark:hover:text-green-200"
              >
                ×
              </button>
            </div>
          </motion.div>
        )}
      </div>
    </div>
  );
};

export default AnalysisPage;
