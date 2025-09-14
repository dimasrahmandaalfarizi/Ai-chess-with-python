#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

from chess_engine.board.board import ChessBoard, Color

def debug_stalemate():
    board = ChessBoard()
    
    print("Board:")
    print(board)
    print()
    
    print("Testing stalemate detection for BLACK...")
    
    # Check if black is in check
    black_in_check = board.is_check(Color.BLACK)
    print(f"Black in check: {black_in_check}")
    
    if not black_in_check:
        print("Black is not in check, checking for legal moves...")
        
        # Check if black has legal moves
        has_legal_move = False
        
        for rank in range(8):
            for file in range(8):
                square = board.get_piece((file, rank))
                if square and not square.empty and square.color == Color.BLACK:
                    print(f"Found black piece at {chr(ord('a') + file)}{8-rank}: {square}")
                    
                    # Generate pseudo-legal moves for this piece
                    pseudo_moves = board._generate_pseudo_legal_moves_for_piece((file, rank), square)
                    print(f"  Pseudo-legal moves: {len(pseudo_moves)}")
                    
                    # Test if any move is legal
                    for i, move in enumerate(pseudo_moves):
                        print(f"    Testing move {i+1}: {move}")
                        board_copy = board.copy()
                        if board_copy.make_move(move):
                            if not board_copy.is_check(Color.BLACK):
                                print(f"      Move is LEGAL!")
                                has_legal_move = True
                                break
                            else:
                                print(f"      Move puts king in check - illegal")
                        else:
                            print(f"      Failed to make move")
                    
                    if has_legal_move:
                        break
            
            if has_legal_move:
                break
        
        print(f"Black has legal moves: {has_legal_move}")
        print(f"Stalemate result: {not has_legal_move}")
    
    # Test the actual function
    actual_stalemate = board.is_stalemate(Color.BLACK)
    print(f"Actual is_stalemate result: {actual_stalemate}")

if __name__ == "__main__":
    debug_stalemate()