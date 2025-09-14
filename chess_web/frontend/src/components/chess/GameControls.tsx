import React from "react";
import {
  Play,
  RotateCcw,
  RotateCw,
  RotateClockwise,
  Flag,
  Handshake,
  Settings,
  Pause,
  Square as SquareIcon,
  Crown,
} from "lucide-react";
import { GameControlsProps } from "@types/index";
import { cn } from "@utils/index";

const GameControls: React.FC<GameControlsProps> = ({
  gameState,
  onNewGame,
  onUndo,
  onRedo,
  onFlipBoard,
  onResign,
  onOfferDraw,
}) => {
  const canUndo = gameState.moveNumber > 1;
  const canRedo = false; // TODO: Implement redo logic
  const isGameActive = gameState.status === "active";

  const controlButtons = [
    {
      icon: Play,
      label: "New Game",
      onClick: onNewGame,
      variant: "primary" as const,
      disabled: false,
    },
    {
      icon: RotateCcw,
      label: "Undo",
      onClick: onUndo,
      variant: "secondary" as const,
      disabled: !canUndo || !isGameActive,
    },
    {
      icon: RotateCw,
      label: "Redo",
      onClick: onRedo,
      variant: "secondary" as const,
      disabled: !canRedo || !isGameActive,
    },
    {
      icon: RotateClockwise,
      label: "Flip Board",
      onClick: onFlipBoard,
      variant: "secondary" as const,
      disabled: false,
    },
  ];

  const gameActions = [
    {
      icon: Flag,
      label: "Resign",
      onClick: onResign,
      variant: "danger" as const,
      disabled: !isGameActive,
    },
    {
      icon: Handshake,
      label: "Offer Draw",
      onClick: onOfferDraw,
      variant: "secondary" as const,
      disabled: !isGameActive,
    },
  ];

  const getButtonClasses = (
    variant: "primary" | "secondary" | "danger",
    disabled: boolean
  ) => {
    const baseClasses =
      "inline-flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

    switch (variant) {
      case "primary":
        return cn(
          baseClasses,
          "text-white bg-primary-600 hover:bg-primary-700 focus:ring-primary-500",
          disabled && "hover:bg-primary-600"
        );
      case "danger":
        return cn(
          baseClasses,
          "text-white bg-red-600 hover:bg-red-700 focus:ring-red-500",
          disabled && "hover:bg-red-600"
        );
      default:
        return cn(
          baseClasses,
          "text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 focus:ring-primary-500"
        );
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Crown className="h-5 w-5 mr-2 text-primary-600" />
          Game Controls
        </h3>

        <div className="flex items-center space-x-2">
          <div
            className={cn(
              "px-2 py-1 rounded-full text-xs font-medium",
              gameState.status === "active" &&
                "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300",
              gameState.status === "checkmate" &&
                "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300",
              gameState.status === "stalemate" &&
                "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300",
              gameState.status === "draw" &&
                "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-300"
            )}
          >
            {gameState.status.charAt(0).toUpperCase() +
              gameState.status.slice(1)}
          </div>
        </div>
      </div>

      {/* Game Info */}
      <div className="grid grid-cols-2 gap-4 mb-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <div className="text-center">
          <div className="text-sm text-gray-600 dark:text-gray-400">Turn</div>
          <div className="font-semibold text-gray-900 dark:text-white">
            {gameState.turn === "white" ? "White" : "Black"}
          </div>
        </div>

        <div className="text-center">
          <div className="text-sm text-gray-600 dark:text-gray-400">Move</div>
          <div className="font-semibold text-gray-900 dark:text-white">
            {gameState.moveNumber}
          </div>
        </div>

        <div className="text-center">
          <div className="text-sm text-gray-600 dark:text-gray-400">Status</div>
          <div className="font-semibold text-gray-900 dark:text-white">
            {gameState.isCheck && "Check"}
            {gameState.isCheckmate && "Checkmate"}
            {gameState.isStalemate && "Stalemate"}
            {!gameState.isCheck &&
              !gameState.isCheckmate &&
              !gameState.isStalemate &&
              "Normal"}
          </div>
        </div>

        <div className="text-center">
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Halfmoves
          </div>
          <div className="font-semibold text-gray-900 dark:text-white">
            {gameState.halfmoveClockNumber}
          </div>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="space-y-4">
        <div>
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Game Controls
          </h4>
          <div className="grid grid-cols-2 gap-2">
            {controlButtons.map((button) => {
              const Icon = button.icon;
              return (
                <button
                  key={button.label}
                  onClick={button.onClick}
                  disabled={button.disabled}
                  className={getButtonClasses(button.variant, button.disabled)}
                  title={button.label}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {button.label}
                </button>
              );
            })}
          </div>
        </div>

        {/* Game Actions */}
        <div>
          <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
            Game Actions
          </h4>
          <div className="grid grid-cols-1 gap-2">
            {gameActions.map((action) => {
              const Icon = action.icon;
              return (
                <button
                  key={action.label}
                  onClick={action.onClick}
                  disabled={action.disabled}
                  className={getButtonClasses(action.variant, action.disabled)}
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {action.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Last Move Info */}
      {gameState.lastMove && (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900 rounded-lg">
          <h4 className="text-sm font-medium text-blue-900 dark:text-blue-300 mb-2">
            Last Move
          </h4>
          <div className="text-sm text-blue-800 dark:text-blue-200">
            <span className="font-mono">
              {gameState.lastMove.san} ({gameState.lastMove.from} →{" "}
              {gameState.lastMove.to})
            </span>
            {gameState.lastMove.captured && (
              <span className="ml-2 text-red-600 dark:text-red-400">
                captured {gameState.lastMove.captured}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Game Result */}
      {gameState.result && (
        <div className="mt-6 p-4 bg-yellow-50 dark:bg-yellow-900 rounded-lg">
          <h4 className="text-sm font-medium text-yellow-900 dark:text-yellow-300 mb-2">
            Game Result
          </h4>
          <div className="text-sm text-yellow-800 dark:text-yellow-200 font-semibold">
            {gameState.result}
          </div>
        </div>
      )}
    </div>
  );
};

export default GameControls;
