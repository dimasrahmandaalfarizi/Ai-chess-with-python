import React from "react";
import { Zap, Target, Shield, Sword, Crown, AlertTriangle } from "lucide-react";

interface TacticalMotifsProps {
  motifs: string[];
}

const TacticalMotifs: React.FC<TacticalMotifsProps> = ({ motifs }) => {
  // Map motifs to icons and descriptions
  const motifInfo: Record<
    string,
    { icon: React.ComponentType<any>; color: string; description: string }
  > = {
    Pin: {
      icon: Target,
      color: "text-red-600 dark:text-red-400",
      description:
        "A piece is pinned and cannot move without exposing a more valuable piece",
    },
    Fork: {
      icon: Sword,
      color: "text-orange-600 dark:text-orange-400",
      description: "One piece attacks two or more enemy pieces simultaneously",
    },
    Skewer: {
      icon: Shield,
      color: "text-purple-600 dark:text-purple-400",
      description:
        "A valuable piece is forced to move, exposing a less valuable piece behind it",
    },
    Check: {
      icon: Crown,
      color: "text-yellow-600 dark:text-yellow-400",
      description: "The enemy king is under attack and must respond",
    },
    Checkmate: {
      icon: Crown,
      color: "text-red-600 dark:text-red-400",
      description:
        "The enemy king is under attack with no legal moves to escape",
    },
    Stalemate: {
      icon: AlertTriangle,
      color: "text-gray-600 dark:text-gray-400",
      description: "No legal moves available but the king is not in check",
    },
    "Discovered Attack": {
      icon: Zap,
      color: "text-blue-600 dark:text-blue-400",
      description: "Moving one piece reveals an attack from another piece",
    },
    "Double Attack": {
      icon: Sword,
      color: "text-green-600 dark:text-green-400",
      description: "Two pieces attack the same target or multiple targets",
    },
    Sacrifice: {
      icon: Shield,
      color: "text-indigo-600 dark:text-indigo-400",
      description: "Giving up material for a positional or tactical advantage",
    },
    Deflection: {
      icon: Target,
      color: "text-pink-600 dark:text-pink-400",
      description: "Forcing a piece to abandon its defensive duties",
    },
    Decoy: {
      icon: Target,
      color: "text-cyan-600 dark:text-cyan-400",
      description: "Luring a piece to a disadvantageous square",
    },
    Zugzwang: {
      icon: AlertTriangle,
      color: "text-amber-600 dark:text-amber-400",
      description: "Any move worsens the position",
    },
  };

  if (motifs.length === 0) {
    return (
      <div className="text-center py-8">
        <Zap className="h-8 w-8 mx-auto mb-2 text-gray-400 dark:text-gray-600" />
        <p className="text-gray-600 dark:text-gray-400">
          No tactical motifs detected
        </p>
        <p className="text-sm text-gray-500 dark:text-gray-500 mt-1">
          The position appears to be positional in nature
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900 dark:text-white">
          Tactical Motifs
        </h4>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {motifs.length} pattern{motifs.length !== 1 ? "s" : ""} found
        </span>
      </div>

      <div className="space-y-2">
        {motifs.map((motif, index) => {
          const info = motifInfo[motif] || {
            icon: Zap,
            color: "text-gray-600 dark:text-gray-400",
            description: "Tactical pattern detected",
          };
          const Icon = info.icon;

          return (
            <div
              key={`${motif}-${index}`}
              className="p-3 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
            >
              <div className="flex items-start space-x-3">
                <div
                  className={`p-2 rounded-lg bg-gray-100 dark:bg-gray-700 ${info.color}`}
                >
                  <Icon className="h-5 w-5" />
                </div>

                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <h5 className="font-semibold text-gray-900 dark:text-white">
                      {motif}
                    </h5>
                    <span className="text-xs text-gray-500 dark:text-gray-400 bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                      Tactical
                    </span>
                  </div>

                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {info.description}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Tactical Summary */}
      <div className="mt-4 p-3 bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-purple-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <div className="flex items-center space-x-2 mb-2">
          <Zap className="h-4 w-4 text-blue-600 dark:text-blue-400" />
          <h5 className="text-sm font-medium text-blue-900 dark:text-blue-300">
            Tactical Assessment
          </h5>
        </div>

        <div className="text-sm text-blue-800 dark:text-blue-200">
          {motifs.includes("Checkmate") && (
            <p className="font-semibold">
              🎯 Checkmate pattern detected! This is a winning position.
            </p>
          )}
          {motifs.includes("Check") && !motifs.includes("Checkmate") && (
            <p>⚡ The king is under attack. Immediate response required.</p>
          )}
          {motifs.includes("Fork") && (
            <p>🍴 Fork opportunity available - can win material.</p>
          )}
          {motifs.includes("Pin") && (
            <p>📌 Pin detected - a piece is restricted in movement.</p>
          )}
          {motifs.includes("Skewer") && (
            <p>🎯 Skewer opportunity - can force material gain.</p>
          )}
          {motifs.length > 0 &&
            !motifs.some((m) =>
              ["Checkmate", "Check", "Fork", "Pin", "Skewer"].includes(m)
            ) && (
              <p>
                🧩 Complex tactical patterns present - careful calculation
                needed.
              </p>
            )}
        </div>
      </div>

      {/* Tactical Tips */}
      <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
          💡 Tactical Tips
        </h5>
        <ul className="text-xs text-gray-600 dark:text-gray-400 space-y-1">
          <li>• Look for forcing moves: checks, captures, and threats</li>
          <li>• Calculate all opponent responses to tactical shots</li>
          <li>• Consider piece coordination and support</li>
          <li>• Don't rush - tactical positions require precise calculation</li>
        </ul>
      </div>
    </div>
  );
};

export default TacticalMotifs;
