#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color
from chess_engine.search.minimax import MinimaxEngine
from chess_engine.board.move_generator import MoveGenerator

def debug_search():
    board = ChessBoard()
    engine = MinimaxEngine(max_depth=2, time_limit=1.0)
    move_gen = MoveGenerator(board)
    
    print("Board:")
    print(board)
    print()
    
    print("Generating legal moves...")
    moves = move_gen.generate_legal_moves(Color.WHITE)
    print(f"Found {len(moves)} legal moves:")
    for i, move in enumerate(moves[:5]):  # Show first 5
        print(f"  {i+1}. {move}")
    
    print(f"\nTesting search with depth 2...")
    try:
        best_move, score = engine.search(board, depth=2)
        print(f"Search result: move={best_move}, score={score}")
        
        if best_move is None:
            print("ERROR: Search returned None move!")
            
            # Debug the search process
            print("\nDebugging search process...")
            
            # Test minimax directly
            result = engine._minimax(board, 2, float('-inf'), float('inf'), Color.WHITE, 0)
            print(f"Direct minimax result: {result}")
            
    except Exception as e:
        print(f"Search failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_search()