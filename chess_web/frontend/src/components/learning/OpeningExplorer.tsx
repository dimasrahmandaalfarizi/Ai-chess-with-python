import React, { useState } from "react";
import {
  BookOpen,
  TrendingUp,
  Users,
  Clock,
  Star,
  ChevronRight,
  Search,
  Filter,
  BarChart3,
} from "lucide-react";
import { OpeningInfo } from "@types/index";
import { cn } from "@utils/index";

interface OpeningExplorerProps {
  fen: string;
  openingInfo?: OpeningInfo;
  loading?: boolean;
  onRequestOpeningInfo: () => void;
}

const OpeningExplorer: React.FC<OpeningExplorerProps> = ({
  fen,
  openingInfo,
  loading = false,
  onRequestOpeningInfo,
}) => {
  const [selectedTab, setSelectedTab] = useState<
    "info" | "moves" | "games" | "stats"
  >("info");

  // Mock data for demonstration
  const mockMasterGames = [
    {
      white: "Kasparov, G.",
      black: "Karpov, A.",
      result: "1-0",
      year: 1984,
      event: "World Championship",
      moves: 42,
    },
    {
      white: "Fischer, R.",
      black: "Spassky, B.",
      result: "1-0",
      year: 1972,
      event: "World Championship",
      moves: 41,
    },
    {
      white: "Carlsen, M.",
      black: "Caruana, F.",
      result: "1/2-1/2",
      year: 2018,
      event: "World Championship",
      moves: 115,
    },
  ];

  const mockContinuations = [
    {
      move: "Nf3",
      games: 15420,
      winRate: 52.3,
      drawRate: 31.2,
      lossRate: 16.5,
    },
    { move: "Nc3", games: 8934, winRate: 48.7, drawRate: 35.1, lossRate: 16.2 },
    { move: "d4", games: 6721, winRate: 51.8, drawRate: 29.4, lossRate: 18.8 },
    { move: "f4", games: 2156, winRate: 45.2, drawRate: 28.9, lossRate: 25.9 },
    { move: "Bc4", games: 1834, winRate: 49.1, drawRate: 32.7, lossRate: 18.2 },
  ];

  const tabs = [
    { id: "info", label: "Opening Info", icon: BookOpen },
    { id: "moves", label: "Continuations", icon: ChevronRight },
    { id: "games", label: "Master Games", icon: Users },
    { id: "stats", label: "Statistics", icon: BarChart3 },
  ];

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="spinner mx-auto mb-4" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Loading opening information...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!openingInfo) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
        <div className="text-center py-12">
          <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400 dark:text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Opening Explorer
          </h3>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Explore opening theory, master games, and statistical data for this
            position.
          </p>
          <button onClick={onRequestOpeningInfo} className="btn btn-primary">
            <BookOpen className="h-4 w-4 mr-2" />
            Explore Opening
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      {/* Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <BookOpen className="h-5 w-5 mr-2 text-primary-600" />
              Opening Explorer
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {openingInfo.name} • ECO: {openingInfo.eco}
            </p>
          </div>

          <button
            onClick={onRequestOpeningInfo}
            className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            title="Refresh opening info"
          >
            <BookOpen className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700">
        <div className="flex space-x-1 p-1">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setSelectedTab(tab.id as any)}
                className={cn(
                  "flex-1 flex items-center justify-center px-3 py-2 text-sm font-medium rounded-md transition-colors",
                  selectedTab === tab.id
                    ? "bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300"
                    : "text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700"
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
      <div className="p-6">
        {selectedTab === "info" && (
          <div className="space-y-6">
            {/* Opening Details */}
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                Opening Details
              </h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Name
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {openingInfo.name}
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    ECO Code
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {openingInfo.eco}
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Popularity
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white flex items-center">
                    <TrendingUp className="h-4 w-4 mr-1 text-green-500" />
                    {openingInfo.popularity}
                  </div>
                </div>

                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <div className="text-sm text-gray-500 dark:text-gray-400">
                    Moves Played
                  </div>
                  <div className="font-semibold text-gray-900 dark:text-white">
                    {openingInfo.moves.length}
                  </div>
                </div>
              </div>
            </div>

            {/* Description */}
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                Description
              </h4>
              <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                {openingInfo.description}
              </p>
            </div>

            {/* Move Sequence */}
            {openingInfo.moves.length > 0 && (
              <div>
                <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
                  Main Line
                </h4>
                <div className="bg-gray-50 dark:bg-gray-700 p-4 rounded-lg">
                  <div className="font-mono text-sm text-gray-900 dark:text-white">
                    {openingInfo.moves.join(" ")}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {selectedTab === "moves" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                Popular Continuations
              </h4>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                Based on master games
              </span>
            </div>

            <div className="space-y-2">
              {mockContinuations.map((continuation, index) => (
                <div
                  key={continuation.move}
                  className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors cursor-pointer"
                >
                  <div className="flex items-center space-x-3">
                    <div className="flex items-center justify-center w-6 h-6 bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300 rounded-full text-xs font-semibold">
                      {index + 1}
                    </div>
                    <div>
                      <div className="font-mono font-semibold text-gray-900 dark:text-white">
                        {continuation.move}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        {continuation.games.toLocaleString()} games
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-4 text-xs">
                    <div className="text-center">
                      <div className="text-green-600 dark:text-green-400 font-semibold">
                        {continuation.winRate}%
                      </div>
                      <div className="text-gray-500 dark:text-gray-400">
                        Win
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-gray-600 dark:text-gray-400 font-semibold">
                        {continuation.drawRate}%
                      </div>
                      <div className="text-gray-500 dark:text-gray-400">
                        Draw
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-red-600 dark:text-red-400 font-semibold">
                        {continuation.lossRate}%
                      </div>
                      <div className="text-gray-500 dark:text-gray-400">
                        Loss
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedTab === "games" && (
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-gray-900 dark:text-white">
                Master Games
              </h4>
              <span className="text-xs text-gray-500 dark:text-gray-400">
                Famous games in this opening
              </span>
            </div>

            <div className="space-y-3">
              {mockMasterGames.map((game, index) => (
                <div
                  key={index}
                  className="p-4 border border-gray-200 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors cursor-pointer"
                >
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold text-gray-900 dark:text-white">
                        {game.white}
                      </span>
                      <span className="text-gray-500 dark:text-gray-400">
                        vs
                      </span>
                      <span className="font-semibold text-gray-900 dark:text-white">
                        {game.black}
                      </span>
                    </div>
                    <div
                      className={cn(
                        "px-2 py-1 rounded text-xs font-semibold",
                        game.result === "1-0" &&
                          "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
                        game.result === "0-1" &&
                          "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
                        game.result === "1/2-1/2" &&
                          "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
                      )}
                    >
                      {game.result}
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400">
                    <span>
                      {game.event} {game.year}
                    </span>
                    <span>{game.moves} moves</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {selectedTab === "stats" && (
          <div className="space-y-6">
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-4">
                Opening Statistics
              </h4>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div className="text-2xl font-bold text-green-600 dark:text-green-400">
                    52.3%
                  </div>
                  <div className="text-sm text-green-700 dark:text-green-300">
                    White Wins
                  </div>
                </div>

                <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div className="text-2xl font-bold text-gray-600 dark:text-gray-400">
                    31.2%
                  </div>
                  <div className="text-sm text-gray-700 dark:text-gray-300">
                    Draws
                  </div>
                </div>

                <div className="text-center p-4 bg-red-50 dark:bg-red-900/20 rounded-lg">
                  <div className="text-2xl font-bold text-red-600 dark:text-red-400">
                    16.5%
                  </div>
                  <div className="text-sm text-red-700 dark:text-red-300">
                    Black Wins
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Total Games
                  </span>
                  <span className="font-semibold text-gray-900 dark:text-white">
                    47,234
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Average Game Length
                  </span>
                  <span className="font-semibold text-gray-900 dark:text-white">
                    38 moves
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Most Common Result
                  </span>
                  <span className="font-semibold text-gray-900 dark:text-white">
                    White Win
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    Performance Rating
                  </span>
                  <span className="font-semibold text-gray-900 dark:text-white">
                    2547
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default OpeningExplorer;
