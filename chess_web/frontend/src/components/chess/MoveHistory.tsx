import React, { useRef, useEffect } from "react";
import { Clock, Download, Copy, RotateCcw } from "lucide-react";
import { MoveHistoryProps, ChessMove } from "@types/index";
import { timeUtils, urlUtils, cn } from "@utils/index";
import toast from "react-hot-toast";

const MoveHistory: React.FC<MoveHistoryProps> = ({
  moves,
  currentMoveIndex,
  onMoveSelect,
}) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to current move
  useEffect(() => {
    if (scrollRef.current && currentMoveIndex >= 0) {
      const moveElement = scrollRef.current.querySelector(
        `[data-move-index="${currentMoveIndex}"]`
      );
      if (moveElement) {
        moveElement.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    }
  }, [currentMoveIndex]);

  // Generate PGN string
  const generatePGN = () => {
    if (moves.length === 0) return "";

    let pgn = "";
    for (let i = 0; i < moves.length; i += 2) {
      const moveNumber = Math.floor(i / 2) + 1;
      const whiteMove = moves[i];
      const blackMove = moves[i + 1];

      pgn += `${moveNumber}. ${whiteMove.san}`;
      if (blackMove) {
        pgn += ` ${blackMove.san} `;
      }
    }

    return pgn.trim();
  };

  // Export PGN
  const handleExportPGN = () => {
    const pgn = generatePGN();
    if (!pgn) {
      toast.error("No moves to export");
      return;
    }

    const blob = new Blob([pgn], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chess-game-${new Date().toISOString().split("T")[0]}.pgn`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);

    toast.success("PGN exported successfully");
  };

  // Copy PGN to clipboard
  const handleCopyPGN = async () => {
    const pgn = generatePGN();
    if (!pgn) {
      toast.error("No moves to copy");
      return;
    }

    const success = await urlUtils.copyToClipboard(pgn);
    if (success) {
      toast.success("PGN copied to clipboard");
    } else {
      toast.error("Failed to copy PGN");
    }
  };

  // Group moves by pairs (white, black)
  const movePairs = [];
  for (let i = 0; i < moves.length; i += 2) {
    movePairs.push({
      moveNumber: Math.floor(i / 2) + 1,
      white: moves[i],
      black: moves[i + 1] || null,
      whiteIndex: i,
      blackIndex: i + 1 < moves.length ? i + 1 : -1,
    });
  }

  return (
    <div className="move-history">
      {/* Header */}
      <div className="card-header flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
          <Clock className="h-5 w-5 mr-2 text-primary-600" />
          Move History
        </h3>

        <div className="flex items-center space-x-2">
          <button
            onClick={handleCopyPGN}
            className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            title="Copy PGN"
          >
            <Copy className="h-4 w-4" />
          </button>

          <button
            onClick={handleExportPGN}
            className="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-md transition-colors"
            title="Export PGN"
          >
            <Download className="h-4 w-4" />
          </button>
        </div>
      </div>

      {/* Move List */}
      <div className="card-body p-0">
        {moves.length === 0 ? (
          <div className="p-6 text-center text-gray-500 dark:text-gray-400">
            <Clock className="h-8 w-8 mx-auto mb-2 opacity-50" />
            <p>No moves yet</p>
            <p className="text-sm">
              Moves will appear here as the game progresses
            </p>
          </div>
        ) : (
          <div ref={scrollRef} className="max-h-96 overflow-y-auto">
            <div className="p-2 space-y-1">
              {movePairs.map((pair) => (
                <div
                  key={pair.moveNumber}
                  className="flex items-center space-x-2 py-1 px-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                >
                  {/* Move Number */}
                  <div className="w-8 text-xs font-semibold text-gray-500 dark:text-gray-400 text-right">
                    {pair.moveNumber}.
                  </div>

                  {/* White Move */}
                  <button
                    data-move-index={pair.whiteIndex}
                    onClick={() => onMoveSelect(pair.whiteIndex)}
                    className={cn(
                      "flex-1 text-left px-2 py-1 rounded text-sm font-mono transition-colors",
                      currentMoveIndex === pair.whiteIndex
                        ? "bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300"
                        : "hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100"
                    )}
                  >
                    {pair.white.san}
                    {pair.white.isCheck && !pair.white.isCheckmate && "+"}
                    {pair.white.isCheckmate && "#"}
                  </button>

                  {/* Black Move */}
                  {pair.black ? (
                    <button
                      data-move-index={pair.blackIndex}
                      onClick={() => onMoveSelect(pair.blackIndex)}
                      className={cn(
                        "flex-1 text-left px-2 py-1 rounded text-sm font-mono transition-colors",
                        currentMoveIndex === pair.blackIndex
                          ? "bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-300"
                          : "hover:bg-gray-100 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100"
                      )}
                    >
                      {pair.black.san}
                      {pair.black.isCheck && !pair.black.isCheckmate && "+"}
                      {pair.black.isCheckmate && "#"}
                    </button>
                  ) : (
                    <div className="flex-1" />
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer with game info */}
      {moves.length > 0 && (
        <div className="card-footer text-xs text-gray-500 dark:text-gray-400">
          <div className="flex justify-between items-center">
            <span>{moves.length} moves</span>
            <span>Last move: {moves[moves.length - 1]?.san}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default MoveHistory;
