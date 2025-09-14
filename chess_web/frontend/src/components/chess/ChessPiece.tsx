import React from "react";
import { useDrag } from "react-dnd";
import { Square, PieceColor, PieceSet } from "@types/index";
import { cn } from "@utils/index";

interface ChessPieceProps {
  type: string;
  color: PieceColor;
  square: Square;
  pieceSet: PieceSet;
  disabled?: boolean;
}

const ChessPiece: React.FC<ChessPieceProps> = ({
  type,
  color,
  square,
  pieceSet,
  disabled = false,
}) => {
  // Drag functionality
  const [{ isDragging }, drag] = useDrag({
    type: "piece",
    item: { square, type, color },
    canDrag: !disabled,
    collect: (monitor) => ({
      isDragging: monitor.isDragging(),
    }),
  });

  // Get piece symbol from piece set
  const getPieceSymbol = () => {
    const pieceKey = `${color}-${type}`;
    return pieceSet.pieces[pieceKey] || "?";
  };

  const symbol = getPieceSymbol();

  return (
    <div
      ref={drag}
      className={cn(
        "chess-piece text-4xl leading-none transition-all duration-200 cursor-grab active:cursor-grabbing",
        color === "white" ? "text-white" : "text-gray-900",
        isDragging && "opacity-50 scale-110 z-50",
        disabled && "cursor-not-allowed opacity-50",
        !disabled && "hover:scale-110 hover:drop-shadow-lg"
      )}
      style={{
        textShadow:
          color === "white"
            ? "1px 1px 2px rgba(0, 0, 0, 0.8)"
            : "1px 1px 2px rgba(255, 255, 255, 0.3)",
        userSelect: "none",
        WebkitUserSelect: "none",
        MozUserSelect: "none",
        msUserSelect: "none",
      }}
    >
      {symbol}
    </div>
  );
};

export default ChessPiece;
