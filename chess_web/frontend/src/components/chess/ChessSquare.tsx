import React from "react";
import { useDrop } from "react-dnd";
import { Square, PieceColor, BoardTheme, PieceSet } from "@types/index";
import { chessUtils, cn } from "@utils/index";
import ChessPiece from "./ChessPiece";

interface ChessSquareProps {
  square: Square;
  piece?: { type: string; color: PieceColor };
  theme: BoardTheme;
  pieceSet: PieceSet;
  isSelected?: boolean;
  isLegalMove?: boolean;
  isHighlighted?: boolean;
  isLastMove?: boolean;
  isCheck?: boolean;
  showCoordinates?: boolean;
  onClick: (square: Square) => void;
  disabled?: boolean;
}

const ChessSquare: React.FC<ChessSquareProps> = ({
  square,
  piece,
  theme,
  pieceSet,
  isSelected = false,
  isLegalMove = false,
  isHighlighted = false,
  isLastMove = false,
  isCheck = false,
  showCoordinates = true,
  onClick,
  disabled = false,
}) => {
  const squareColor = chessUtils.getSquareColor(square);
  const coordinates = chessUtils.squareToCoordinates(square);
  const isBottomRank = coordinates.rank === "1";
  const isRightFile = coordinates.file === "h";

  // Drop target for pieces
  const [{ isOver, canDrop }, drop] = useDrop({
    accept: "piece",
    drop: () => ({ square }),
    canDrop: () => !disabled,
    collect: (monitor) => ({
      isOver: monitor.isOver(),
      canDrop: monitor.canDrop(),
    }),
  });

  const handleClick = () => {
    if (!disabled) {
      onClick(square);
    }
  };

  // Determine square background color
  const getSquareStyle = () => {
    if (isCheck) {
      return { backgroundColor: "#ff6b6b" };
    }
    if (isSelected) {
      return { backgroundColor: "#20b2aa" };
    }
    if (isHighlighted) {
      return { backgroundColor: "#ffff00" };
    }
    if (isLastMove) {
      return { backgroundColor: "#ffd700", opacity: 0.7 };
    }
    if (isOver && canDrop) {
      return { backgroundColor: "#90ee90", opacity: 0.8 };
    }

    return {
      backgroundColor:
        squareColor === "light" ? theme.lightSquares : theme.darkSquares,
    };
  };

  return (
    <div
      ref={drop}
      className={cn(
        "chess-square relative flex items-center justify-center cursor-pointer select-none transition-all duration-200",
        disabled && "cursor-not-allowed opacity-50",
        isOver && canDrop && "ring-2 ring-green-400",
        isCheck && "animate-check-flash"
      )}
      style={getSquareStyle()}
      onClick={handleClick}
    >
      {/* Piece */}
      {piece && (
        <ChessPiece
          type={piece.type}
          color={piece.color}
          square={square}
          pieceSet={pieceSet}
          disabled={disabled}
        />
      )}

      {/* Legal move indicator */}
      {isLegalMove && !piece && (
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="w-3 h-3 bg-gray-600 dark:bg-gray-400 rounded-full opacity-60" />
        </div>
      )}

      {/* Legal capture indicator */}
      {isLegalMove && piece && (
        <div className="absolute inset-0 border-4 border-red-500 rounded-full opacity-60" />
      )}

      {/* Coordinates */}
      {showCoordinates && (
        <>
          {/* File labels (bottom rank) */}
          {isBottomRank && (
            <div
              className="coordinate-label file text-xs font-semibold absolute bottom-1 right-1"
              style={{ color: theme.coordinates }}
            >
              {coordinates.file}
            </div>
          )}

          {/* Rank labels (left file) */}
          {isRightFile && (
            <div
              className="coordinate-label rank text-xs font-semibold absolute top-1 left-1"
              style={{ color: theme.coordinates }}
            >
              {coordinates.rank}
            </div>
          )}
        </>
      )}

      {/* Selection highlight */}
      {isSelected && (
        <div className="absolute inset-0 border-4 border-blue-500 rounded-lg opacity-80" />
      )}
    </div>
  );
};

export default ChessSquare;
