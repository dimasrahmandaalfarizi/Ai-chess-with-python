#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.board.move_generator import MoveGenerator

def debug_moves():
    board = ChessBoard()
    move_gen = MoveGenerator(board)
    
    print("Board:")
    print(board)
    print()
    
    print("Generating pseudo-legal moves...")
    moves = []
    
    # Generate moves for each piece manually
    for rank in range(8):
        for file in range(8):
            square = board.get_piece((file, rank))
            if square and not square.empty and square.color == Color.WHITE:
                print(f"Piece at {chr(ord('a') + file)}{8-rank}: {square}")
                piece_moves = move_gen._generate_piece_moves((file, rank), square)
                print(f"  Generated {len(piece_moves)} moves: {[str(m) for m in piece_moves]}")
                moves.extend(piece_moves)
    
    print(f"\nTotal pseudo-legal moves: {len(moves)}")
    
    print("\nTesting legal move validation...")
    legal_moves = []
    for i, move in enumerate(moves):
        print(f"Testing move {i+1}/{len(moves)}: {move}")
        
        # Create a copy of the board to test the move
        board_copy = board.copy()
        
        # Try to make the move on the copy
        if board_copy.make_move(move):
            print(f"  Move made successfully")
            # Check if this move puts own king in check
            if not board_copy.is_check(Color.WHITE):
                print(f"  Move is legal")
                legal_moves.append(move)
            else:
                print(f"  Move puts king in check - illegal")
            board_copy.undo_move()
        else:
            print(f"  Failed to make move")
    
    print(f"\nTotal legal moves: {len(legal_moves)}")
    for move in legal_moves:
        print(f"  {move}")

if __name__ == "__main__":
    debug_moves()