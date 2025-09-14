import React, { useState } from "react";
import { TrendingUp, ChevronRight, ChevronDown } from "lucide-react";
import { MoveVariation } from "@types/index";
import { evaluationUtils, cn } from "@utils/index";

interface VariationsProps {
  variations: MoveVariation[];
}

const Variations: React.FC<VariationsProps> = ({ variations }) => {
  const [expandedVariations, setExpandedVariations] = useState<Set<number>>(
    new Set([0])
  );

  const toggleVariation = (index: number) => {
    const newExpanded = new Set(expandedVariations);
    if (newExpanded.has(index)) {
      newExpanded.delete(index);
    } else {
      newExpanded.add(index);
    }
    setExpandedVariations(newExpanded);
  };

  if (variations.length === 0) {
    return (
      <div className="text-center py-8">
        <TrendingUp className="h-8 w-8 mx-auto mb-2 text-gray-400 dark:text-gray-600" />
        <p className="text-gray-600 dark:text-gray-400">
          No variations available
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h4 className="font-medium text-gray-900 dark:text-white">
          Principal Variations
        </h4>
        <span className="text-xs text-gray-500 dark:text-gray-400">
          {variations.length} line{variations.length !== 1 ? "s" : ""}
        </span>
      </div>

      <div className="space-y-2">
        {variations.map((variation, index) => {
          const isExpanded = expandedVariations.has(index);
          const isMainLine = index === 0;

          return (
            <div
              key={index}
              className={cn(
                "border rounded-lg transition-colors",
                isMainLine
                  ? "border-primary-200 dark:border-primary-800 bg-primary-50 dark:bg-primary-900/20"
                  : "border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800"
              )}
            >
              {/* Variation Header */}
              <button
                onClick={() => toggleVariation(index)}
                className="w-full p-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors rounded-lg"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    {/* Rank */}
                    <div
                      className={cn(
                        "flex items-center justify-center w-6 h-6 rounded-full text-xs font-semibold",
                        isMainLine
                          ? "bg-primary-600 text-white"
                          : "bg-gray-200 dark:bg-gray-700 text-gray-600 dark:text-gray-400"
                      )}
                    >
                      {index + 1}
                    </div>

                    {/* First move and description */}
                    <div>
                      <div className="font-mono font-semibold text-gray-900 dark:text-white">
                        {variation.moves[0] || "No moves"}
                      </div>
                      {variation.description && (
                        <div className="text-xs text-gray-500 dark:text-gray-400">
                          {variation.description}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center space-x-3">
                    {/* Evaluation */}
                    <div className="text-right">
                      <div
                        className={cn(
                          "font-mono font-semibold text-sm",
                          evaluationUtils.getEvaluationColor(
                            variation.evaluation
                          )
                        )}
                      >
                        {evaluationUtils.formatScore(variation.evaluation)}
                      </div>
                      <div className="text-xs text-gray-500 dark:text-gray-400">
                        depth {variation.depth}
                      </div>
                    </div>

                    {/* Expand/Collapse Icon */}
                    {isExpanded ? (
                      <ChevronDown className="h-4 w-4 text-gray-400" />
                    ) : (
                      <ChevronRight className="h-4 w-4 text-gray-400" />
                    )}
                  </div>
                </div>
              </button>

              {/* Expanded Content */}
              {isExpanded && (
                <div className="px-3 pb-3 border-t border-gray-200 dark:border-gray-700">
                  <div className="pt-3">
                    {/* Full move sequence */}
                    <div className="mb-3">
                      <h5 className="text-xs font-medium text-gray-700 dark:text-gray-300 mb-2">
                        Move Sequence
                      </h5>
                      <div className="font-mono text-sm text-gray-900 dark:text-white bg-gray-50 dark:bg-gray-700 p-2 rounded">
                        {variation.moves.join(" ")}
                      </div>
                    </div>

                    {/* Move breakdown */}
                    <div className="space-y-1">
                      <h5 className="text-xs font-medium text-gray-700 dark:text-gray-300">
                        Individual Moves
                      </h5>
                      <div className="grid grid-cols-2 gap-1 text-xs">
                        {variation.moves.map((move, moveIndex) => (
                          <div
                            key={moveIndex}
                            className="flex items-center space-x-2 p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-600"
                          >
                            <span className="text-gray-500 dark:text-gray-400 w-4">
                              {Math.floor(moveIndex / 2) + 1}
                              {moveIndex % 2 === 0 ? "." : "..."}
                            </span>
                            <span className="font-mono text-gray-900 dark:text-white">
                              {move}
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Variation stats */}
                    <div className="mt-3 pt-2 border-t border-gray-200 dark:border-gray-600">
                      <div className="grid grid-cols-3 gap-4 text-xs">
                        <div className="text-center">
                          <div className="text-gray-500 dark:text-gray-400">
                            Moves
                          </div>
                          <div className="font-semibold text-gray-900 dark:text-white">
                            {variation.moves.length}
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-gray-500 dark:text-gray-400">
                            Depth
                          </div>
                          <div className="font-semibold text-gray-900 dark:text-white">
                            {variation.depth}
                          </div>
                        </div>
                        <div className="text-center">
                          <div className="text-gray-500 dark:text-gray-400">
                            Eval
                          </div>
                          <div
                            className={cn(
                              "font-semibold font-mono",
                              evaluationUtils.getEvaluationColor(
                                variation.evaluation
                              )
                            )}
                          >
                            {evaluationUtils.formatScore(variation.evaluation)}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Variation comparison */}
      {variations.length > 1 && (
        <div className="mt-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <h5 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
            Line Comparison
          </h5>
          <div className="space-y-1 text-xs">
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">
                Best line:
              </span>
              <span className="font-mono text-gray-900 dark:text-white">
                {evaluationUtils.formatScore(variations[0].evaluation)}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">
                Alternative gap:
              </span>
              <span className="font-mono text-gray-900 dark:text-white">
                {evaluationUtils.formatScore(
                  variations[0].evaluation - (variations[1]?.evaluation || 0)
                )}
              </span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600 dark:text-gray-400">
                Average depth:
              </span>
              <span className="font-mono text-gray-900 dark:text-white">
                {(
                  variations.reduce((sum, v) => sum + v.depth, 0) /
                  variations.length
                ).toFixed(1)}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Variations;
