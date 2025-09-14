import React from "react";
import { Target, TrendingUp, TrendingDown } from "lucide-react";
import { BestMove } from "@types/index";
import { evaluationUtils, cn } from "@utils/index";

interface BestMovesProps {
  moves: BestMove[];
}

const BestMoves: React.FC<BestMovesProps> = ({ moves }) => {
  if (moves.length === 0) {
    return (
      <div className="text-center py-8">
        <Target className="h-8 w-8 mx-auto mb-2 text-gray-400 dark:text-gray-600" />
        <p className="text-gray-600 dark:text-gray-400">No moves analyzed</p>
      </div>
    );
  }

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return "text-green-600 dark:text-green-400";
    if (confidence >= 0.6) return "text-yellow-600 dark:text-yellow-400";
    return "text-red-600 dark:text-red-400";
  };

  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 0.7) return TrendingUp;
    if (confidence >= 0.4) return Target;
    return TrendingDown;
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900 dark:text-white">
          Best Moves
        </h4>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {moves.length} move{moves.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="space-y-2">
        {moves.map((move, index) => {
          const Icon = getConfidenceIcon(move.confidence);
          const isTopMove = index === 0;

          return (
            <div
              key={`${move.move}-${index}`}
              className={cn(
                "p-3 rounded-lg border transition-colors hover:bg-gray-50 dark:hover:bg-gray-700",
                isTopMove
                  ? "border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/20"
                  : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
              )}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {/* Rank */}
                  <div
                    className={cn(
                      "flex items-center justify-center w-6 h-6 rounded-full text-xs font-semibold",
                      isTopMove
                        ? "bg-primary-600 text-white"
                        : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                    )}
                  >
                    {index + 1}
                  </div>

                  {/* Move */}
                  <div>
                    <div className="font-mono font-semibold text-gray-900 dark:text-white">
                      {move.san}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      {move.move}
                    </div>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  {/* Evaluation */}
                  <div className="text-right">
                    <div
                      className={cn(
                        "font-mono font-semibold text-sm",
                        evaluationUtils.getEvaluationColor(move.evaluation)
                      )}
                    >
                      {evaluationUtils.formatScore(move.evaluation)}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">
                      evaluation
                    </div>
                  </div>

                  {/* Confidence */}
                  <div className="flex items-center space-x-1">
                    <Icon
                      className={cn(
                        "h-4 w-4",
                        getConfidenceColor(move.confidence)
                      )}
                    />
                    <span
                      className={cn(
                        "text-sm font-medium",
                        getConfidenceColor(move.confidence)
                      )}
                    >
                      {Math.round(move.confidence * 100)}%
                    </span>
                  </div>
                </div>
              </div>

              {/* Additional info for top move */}
              {isTopMove && (
                <div className="mt-2 pt-2 border-t border-primary-200 dark:border-primary-800">
                  <div className="flex items-center space-x-2 text-xs text-primary-700 dark:text-primary-300">
                    <Target className="h-3 w-3" />
                    <span>Recommended move</span>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Move comparison */}
      {moves.length > 1 && (
        <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
            Move Comparison
          </h5>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">
                Best move advantage:
              </span>
              <span className="font-mono text-gray-900 dark:text-white">
                {evaluationUtils.formatScore(
                  moves[0].evaluation - (moves[1]?.evaluation || 0)
                )}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">
                Confidence gap:
              </span>
              <span className="font-mono text-gray-900 dark:text-white">
                {Math.round(
                  (moves[0].confidence - (moves[1]?.confidence || 0)) * 100
                )}
                %
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BestMoves;
