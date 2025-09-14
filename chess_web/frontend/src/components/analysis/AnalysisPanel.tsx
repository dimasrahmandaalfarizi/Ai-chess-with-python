import React, { useState } from "react";
import {
  BarChart3,
  Brain,
  Target,
  TrendingUp,
  Zap,
  Settings,
  RefreshCw,
  Play,
  Pause,
} from "lucide-react";
import { AnalysisPanelProps } from "@types/index";
import { evaluationUtils, cn } from "@utils/index";
import EvaluationBar from "./EvaluationBar";
import BestMoves from "./BestMoves";
import Variations from "./Variations";
import TacticalMotifs from "./TacticalMotifs";

const AnalysisPanel: React.FC<AnalysisPanelProps> = ({
  analysis,
  loading = false,
  onDepthChange,
  onAnalysisRequest,
}) => {
  const [selectedDepth, setSelectedDepth] = useState(4);
  const [isAutoAnalysis, setIsAutoAnalysis] = useState(false);
  const [activeTab, setActiveTab] = useState<
    "overview" | "moves" | "variations" | "tactics"
  >("overview");

  const handleDepthChange = (depth: number) => {
    setSelectedDepth(depth);
    onDepthChange(depth);
  };

  const tabs = [
    { id: "overview", label: "Overview", icon: BarChart3 },
    { id: "moves", label: "Best Moves", icon: Target },
    { id: "variations", label: "Variations", icon: TrendingUp },
    { id: "tactics", label: "Tactics", icon: Zap },
  ];

  return (
    <div className="analysis-panel">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Brain className="h-5 w-5 mr-2 text-primary-600" />
          Position Analysis
        </h3>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setIsAutoAnalysis(!isAutoAnalysis)}
            className={cn(
              "p-2 rounded-md transition-colors",
              isAutoAnalysis
                ? "text-green-600 bg-green-100 dark:bg-green-900 dark:text-green-400"
                : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
            )}
            title={
              isAutoAnalysis ? "Disable auto-analysis" : "Enable auto-analysis"
            }
          >
            {isAutoAnalysis ? (
              <Pause className="h-4 w-4" />
            ) : (
              <Play className="h-4 w-4" />
            )}
          </button>

          <button
            onClick={onAnalysisRequest}
            disabled={loading}
            className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors disabled:opacity-50"
            title="Refresh analysis"
          >
            <RefreshCw className={cn("h-4 w-4", loading && "animate-spin")} />
          </button>
        </div>
      </div>

      {/* Analysis Controls */}
      <div className="mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div className="flex items-center justify-between mb-3">
          <label className="text-sm font-medium text-gray-700 dark:text-gray-300">
            Analysis Depth
          </label>
          <span className="text-sm text-gray-500 dark:text-gray-400">
            {selectedDepth} plies
          </span>
        </div>

        <input
          type="range"
          min="1"
          max="10"
          value={selectedDepth}
          onChange={(e) => handleDepthChange(parseInt(e.target.value))}
          className="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer"
        />

        <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400 mt-1">
          <span>Fast</span>
          <span>Balanced</span>
          <span>Deep</span>
        </div>
      </div>

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="spinner mx-auto mb-4" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Analyzing position...
            </p>
          </div>
        </div>
      )}

      {/* Analysis Content */}
      {!loading && analysis && (
        <>
          {/* Evaluation Bar */}
          <div className="mb-6">
            <EvaluationBar evaluation={analysis.evaluation} className="mb-2" />
            <div className="text-center text-sm text-gray-600 dark:text-gray-400">
              {evaluationUtils.getEvaluationDescription(
                analysis.evaluation.score
              )}
            </div>
          </div>

          {/* Tabs */}
          <div className="mb-4">
            <div className="flex space-x-1 bg-gray-100 dark:bg-gray-700 rounded-lg p-1">
              {tabs.map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as any)}
                    className={cn(
                      "flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                      activeTab === tab.id
                        ? "bg-white dark:bg-gray-800 text-primary-600 dark:text-primary-400 shadow-sm"
                        : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200"
                    )}
                  >
                    <Icon className="h-4 w-4 mr-1" />
                    <span className="hidden sm:inline">{tab.label}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-4">
            {activeTab === "overview" && (
              <div className="space-y-4">
                {/* Quick Stats */}
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Evaluation
                    </div>
                    <div className="font-semibold text-gray-900 dark:text-white">
                      {evaluationUtils.formatScore(analysis.evaluation.score)}
                    </div>
                  </div>

                  <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Best Move
                    </div>
                    <div className="font-semibold text-gray-900 dark:text-white font-mono">
                      {analysis.bestMoves[0]?.san || "N/A"}
                    </div>
                  </div>

                  <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Analysis Time
                    </div>
                    <div className="font-semibold text-gray-900 dark:text-white">
                      {analysis.analysisTime.toFixed(1)}s
                    </div>
                  </div>

                  <div className="bg-gray-50 dark:bg-gray-700 p-3 rounded-lg">
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      Nodes
                    </div>
                    <div className="font-semibold text-gray-900 dark:text-white">
                      {analysis.nodesSearched.toLocaleString()}
                    </div>
                  </div>
                </div>

                {/* Opening Info */}
                {analysis.openingInfo && (
                  <div className="bg-blue-50 dark:bg-blue-900 p-4 rounded-lg">
                    <h4 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">
                      Opening Information
                    </h4>
                    <div className="text-sm text-blue-800 dark:text-blue-200">
                      <div className="font-medium">
                        {analysis.openingInfo.name}
                      </div>
                      <div className="text-xs opacity-75">
                        ECO: {analysis.openingInfo.eco} • Popularity:{" "}
                        {analysis.openingInfo.popularity}
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}

            {activeTab === "moves" && <BestMoves moves={analysis.bestMoves} />}

            {activeTab === "variations" && (
              <Variations variations={analysis.variations} />
            )}

            {activeTab === "tactics" && (
              <TacticalMotifs motifs={analysis.tacticalMotifs} />
            )}
          </div>
        </>
      )}

      {/* No Analysis State */}
      {!loading && !analysis && (
        <div className="text-center py-12">
          <Brain className="h-12 w-12 mx-auto mb-4 text-gray-400 dark:text-gray-600" />
          <p className="text-gray-600 dark:text-gray-400 mb-4">
            No analysis available
          </p>
          <button onClick={onAnalysisRequest} className="btn btn-primary">
            Start Analysis
          </button>
        </div>
      )}
    </div>
  );
};

export default AnalysisPanel;
