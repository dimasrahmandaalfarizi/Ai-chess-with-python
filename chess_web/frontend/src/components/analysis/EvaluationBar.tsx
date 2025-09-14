import React from "react";
import { PositionEvaluation } from "@types/index";
import { evaluationUtils, cn } from "@utils/index";

interface EvaluationBarProps {
  evaluation: PositionEvaluation;
  className?: string;
}

const EvaluationBar: React.FC<EvaluationBarProps> = ({
  evaluation,
  className,
}) => {
  const percentage = evaluationUtils.getEvaluationPercentage(evaluation.score);
  const formattedScore = evaluationUtils.formatScore(evaluation.score);

  // Determine bar color based on evaluation
  const getBarColor = () => {
    if (evaluation.mateIn) {
      return evaluation.mateIn > 0 ? "bg-green-600" : "bg-red-600";
    }

    const absScore = Math.abs(evaluation.score);
    if (absScore > 500)
      return evaluation.score > 0 ? "bg-green-600" : "bg-red-600";
    if (absScore > 200)
      return evaluation.score > 0 ? "bg-green-500" : "bg-red-500";
    if (absScore > 50)
      return evaluation.score > 0 ? "bg-green-400" : "bg-red-400";
    return "bg-gray-400";
  };

  return (
    <div className={cn("space-y-2", className)}>
      {/* Score Display */}
      <div className="flex items-center justify-between text-sm">
        <span className="font-medium text-gray-900 dark:text-white">
          Evaluation
        </span>
        <span
          className={cn(
            "font-mono font-semibold",
            evaluationUtils.getEvaluationColor(evaluation.score)
          )}
        >
          {evaluation.mateIn
            ? evaluation.mateIn > 0
              ? `+M${evaluation.mateIn}`
              : `-M${Math.abs(evaluation.mateIn)}`
            : formattedScore}
        </span>
      </div>

      {/* Evaluation Bar */}
      <div className="evaluation-bar relative">
        {/* Background */}
        <div className="absolute inset-0 bg-gray-200 dark:bg-gray-700 rounded-full" />

        {/* White advantage (right side) */}
        <div
          className={cn(
            "absolute top-0 right-0 h-full rounded-r-full transition-all duration-500",
            percentage > 50 ? getBarColor() : "bg-transparent"
          )}
          style={{
            width: `${Math.max(0, percentage - 50)}%`,
          }}
        />

        {/* Black advantage (left side) */}
        <div
          className={cn(
            "absolute top-0 left-0 h-full rounded-l-full transition-all duration-500",
            percentage < 50 ? getBarColor() : "bg-transparent"
          )}
          style={{
            width: `${Math.max(0, 50 - percentage)}%`,
          }}
        />

        {/* Center line */}
        <div className="absolute top-0 left-1/2 transform -translate-x-0.5 w-0.5 h-full bg-gray-800 dark:bg-gray-200" />

        {/* Evaluation marker */}
        <div
          className="absolute top-0 h-full w-1 bg-yellow-400 border border-yellow-600 rounded-full transition-all duration-500 transform -translate-x-0.5"
          style={{
            left: `${percentage}%`,
          }}
        />
      </div>

      {/* Labels */}
      <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
        <span>Black</span>
        <span>Equal</span>
        <span>White</span>
      </div>

      {/* Detailed Breakdown */}
      {evaluation.breakdown && (
        <details className="mt-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100">
            Detailed Breakdown
          </summary>
          <div className="mt-2 space-y-2 text-xs">
            {Object.entries(evaluation.breakdown).map(([key, value]) => {
              if (key === "total") return null;

              const label =
                key.charAt(0).toUpperCase() +
                key.slice(1).replace(/([A-Z])/g, " $1");
              const formattedValue =
                typeof value === "number" ? value.toFixed(2) : value;

              return (
                <div key={key} className="flex justify-between">
                  <span className="text-gray-600 dark:text-gray-400">
                    {label}:
                  </span>
                  <span className="font-mono text-gray-900 dark:text-white">
                    {formattedValue > 0 ? "+" : ""}
                    {formattedValue}
                  </span>
                </div>
              );
            })}
            <div className="border-t border-gray-200 dark:border-gray-600 pt-2 flex justify-between font-semibold">
              <span className="text-gray-900 dark:text-white">Total:</span>
              <span className="font-mono text-gray-900 dark:text-white">
                {evaluation.breakdown.total > 0 ? "+" : ""}
                {evaluation.breakdown.total.toFixed(2)}
              </span>
            </div>
          </div>
        </details>
      )}
    </div>
  );
};

export default EvaluationBar;
