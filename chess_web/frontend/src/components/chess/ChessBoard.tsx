import React, { useState, useCallback, useEffect } from "react";
import { useDrop } from "react-dnd";
import { ChessBoardProps, Square, PieceColor, ChessMove } from "@types/index";
import { chessUtils, cn } from "@utils/index";
import { useThemeStore } from "@store/themeStore";
import ChessSquare from "./ChessSquare";
import ChessPiece from "./ChessPiece";

const ChessBoard: React.FC<ChessBoardProps> = ({
  position,
  onMove,
  orientation = "white",
  showCoordinates = true,
  showLegalMoves = true,
  disabled = false,
  highlightedSquares = [],
  theme,
  pieceSet,
}) => {
  const { currentTheme, currentPieceSet, preferences } = useThemeStore();
  const [selectedSquare, setSelectedSquare] = useState<Square | null>(null);
  const [legalMoves, setLegalMoves] = useState<Square[]>([]);
  const [lastMove, setLastMove] = useState<{ from: Square; to: Square } | null>(
    null
  );

  const boardTheme = theme || currentTheme;
  const pieces = pieceSet || currentPieceSet;
  const showCoords = showCoordinates && preferences.showCoordinates;
  const showLegal = showLegalMoves && preferences.showLegalMoves;

  // Parse FEN to get piece positions
  const parseFEN = useCallback((fen: string) => {
    const pieces: Record<Square, { type: string; color: PieceColor }> = {};
    const [boardPart] = fen.split(" ");
    const ranks = boardPart.split("/");

    ranks.forEach((rank, rankIndex) => {
      let fileIndex = 0;
      for (const char of rank) {
        if (char >= "1" && char <= "8") {
          fileIndex += parseInt(char);
        } else {
          const file = String.fromCharCode("a".charCodeAt(0) + fileIndex);
          const rankNum = 8 - rankIndex;
          const square = `${file}${rankNum}` as Square;

          const isWhite = char === char.toUpperCase();
          const pieceType = char.toLowerCase();

          pieces[square] = {
            type: pieceType,
            color: isWhite ? "white" : "black",
          };
          fileIndex++;
        }
      }
    });

    return pieces;
  }, []);

  const piecePositions = parseFEN(position.fen);

  // Generate squares based on orientation
  const generateSquares = useCallback(() => {
    const squares: Square[] = [];
    const files = orientation === "white" ? "abcdefgh" : "hgfedcba";
    const ranks = orientation === "white" ? "87654321" : "12345678";

    for (const rank of ranks) {
      for (const file of files) {
        squares.push(`${file}${rank}` as Square);
      }
    }

    return squares;
  }, [orientation]);

  const squares = generateSquares();

  // Handle square click
  const handleSquareClick = useCallback(
    (square: Square) => {
      if (disabled) return;

      if (selectedSquare) {
        if (selectedSquare === square) {
          // Deselect
          setSelectedSquare(null);
          setLegalMoves([]);
        } else if (legalMoves.includes(square)) {
          // Make move
          const move: ChessMove = {
            from: selectedSquare,
            to: square,
            piece: piecePositions[selectedSquare]?.type || "",
            captured: piecePositions[square]?.type,
            san: `${selectedSquare}${square}`, // Simplified
            uci: `${selectedSquare}${square}`,
            isCheck: false,
            isCheckmate: false,
            isCastling: false,
            isEnPassant: false,
          };

          onMove(move);
          setSelectedSquare(null);
          setLegalMoves([]);
          setLastMove({ from: selectedSquare, to: square });
        } else {
          // Select new square
          const piece = piecePositions[square];
          if (piece && piece.color === position.turn) {
            setSelectedSquare(square);
            // TODO: Get legal moves from chess engine
            setLegalMoves([]); // Placeholder
          } else {
            setSelectedSquare(null);
            setLegalMoves([]);
          }
        }
      } else {
        // Select square
        const piece = piecePositions[square];
        if (piece && piece.color === position.turn) {
          setSelectedSquare(square);
          // TODO: Get legal moves from chess engine
          setLegalMoves([]); // Placeholder
        }
      }
    },
    [
      selectedSquare,
      legalMoves,
      piecePositions,
      position.turn,
      disabled,
      onMove,
    ]
  );

  // Handle piece drop
  const handlePieceDrop = useCallback(
    (fromSquare: Square, toSquare: Square) => {
      if (disabled) return;

      const move: ChessMove = {
        from: fromSquare,
        to: toSquare,
        piece: piecePositions[fromSquare]?.type || "",
        captured: piecePositions[toSquare]?.type,
        san: `${fromSquare}${toSquare}`, // Simplified
        uci: `${fromSquare}${toSquare}`,
        isCheck: false,
        isCheckmate: false,
        isCastling: false,
        isEnPassant: false,
      };

      onMove(move);
      setSelectedSquare(null);
      setLegalMoves([]);
      setLastMove({ from: fromSquare, to: toSquare });
    },
    [piecePositions, disabled, onMove]
  );

  // Board drop target
  const [{ isOver }, drop] = useDrop({
    accept: "piece",
    drop: (item: { square: Square }, monitor) => {
      const targetElement = monitor.getDropResult();
      if (targetElement && targetElement.square) {
        handlePieceDrop(item.square, targetElement.square);
      }
    },
    collect: (monitor) => ({
      isOver: monitor.isOver(),
    }),
  });

  return (
    <div className="flex flex-col items-center">
      {/* Board */}
      <div
        ref={drop}
        className={cn(
          "chess-board relative",
          isOver && "ring-2 ring-primary-500"
        )}
        style={{
          backgroundColor: boardTheme.border,
        }}
      >
        {squares.map((square, index) => {
          const piece = piecePositions[square];
          const isSelected = selectedSquare === square;
          const isLegalMove = showLegal && legalMoves.includes(square);
          const isHighlighted = highlightedSquares.includes(square);
          const isLastMove =
            lastMove && (lastMove.from === square || lastMove.to === square);
          const isCheck =
            position.isCheck &&
            piece?.type === "king" &&
            piece.color === position.turn;

          return (
            <ChessSquare
              key={square}
              square={square}
              piece={piece}
              theme={boardTheme}
              pieceSet={pieces}
              isSelected={isSelected}
              isLegalMove={isLegalMove}
              isHighlighted={isHighlighted}
              isLastMove={isLastMove}
              isCheck={isCheck}
              showCoordinates={showCoords}
              onClick={handleSquareClick}
              disabled={disabled}
            />
          );
        })}
      </div>

      {/* Status */}
      <div className="mt-4 text-center">
        <div className="text-sm text-gray-600 dark:text-gray-400">
          {position.isCheckmate && (
            <span className="text-red-600 font-semibold">Checkmate!</span>
          )}
          {position.isStalemate && (
            <span className="text-yellow-600 font-semibold">Stalemate!</span>
          )}
          {position.isDraw && (
            <span className="text-gray-600 font-semibold">Draw!</span>
          )}
          {position.isCheck && !position.isCheckmate && (
            <span className="text-orange-600 font-semibold">Check!</span>
          )}
          {!position.isCheckmate &&
            !position.isStalemate &&
            !position.isDraw && (
              <span>
                {position.turn === "white" ? "White" : "Black"} to move
              </span>
            )}
        </div>

        <div className="text-xs text-gray-500 dark:text-gray-500 mt-1">
          Move {position.moveNumber} • {position.fen.split(" ")[5]} moves
        </div>
      </div>
    </div>
  );
};

export default ChessBoard;
