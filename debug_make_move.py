#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color, Move, PieceType

def debug_make_move():
    board = ChessBoard()
    
    print("Board:")
    print(board)
    print(f"Current player: {board.current_player}")
    print()
    
    # Try to make a simple pawn move for black
    move = Move((0, 1), (0, 2), PieceType.PAWN, Color.BLACK)  # a7-a6
    print(f"Trying to make move: {move}")
    print(f"Move color: {move.color}")
    print(f"Board current player: {board.current_player}")
    
    # Check piece at source
    piece = board.get_piece((0, 1))
    print(f"Piece at a7: {piece} (empty: {piece.empty if piece else 'None'})")
    if piece and not piece.empty:
        print(f"Piece color: {piece.color}")
        print(f"Piece type: {piece.piece_type}")
    
    # Try to make the move
    success = board.make_move(move)
    print(f"Move success: {success}")
    
    if not success:
        print("Move failed. Let's check why...")
        
        # Check if it's the right player's turn
        if move.color != board.current_player:
            print(f"ERROR: Wrong player! Move color: {move.color}, Current player: {board.current_player}")
        
        # Check if piece exists and is correct color
        piece = board.get_piece(move.from_square)
        if not piece or piece.empty:
            print(f"ERROR: No piece at source square {move.from_square}")
        elif piece.color != board.current_player:
            print(f"ERROR: Piece color {piece.color} doesn't match current player {board.current_player}")

if __name__ == "__main__":
    debug_make_move()