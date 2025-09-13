"""
UCI Interface - Universal Chess Interface implementation

This module implements:
- UCI protocol for communication with chess GUIs
- Engine identification and capabilities
- Position setting and move calculation
- Engine options and configuration
"""

import sys
import time
from typing import Dict, List, Optional, Any
from ..board.board import ChessBoard, Color
from ..search.minimax import MinimaxEngine
from ..eval.evaluation import EvaluationEngine

class UCIInterface:
    """UCI protocol interface for chess engine"""
    
    def __init__(self):
        """Initialize UCI interface"""
        self.board = ChessBoard()
        self.engine = MinimaxEngine()
        self.evaluation_engine = EvaluationEngine()
        self.is_ready = False
        self.search_time = 5.0
        self.search_depth = 4
        
        # UCI options
        self.options = {
            "Hash": {"type": "spin", "default": 64, "min": 1, "max": 1024, "value": 64},
            "Depth": {"type": "spin", "default": 4, "min": 1, "max": 20, "value": 4},
            "Time": {"type": "spin", "default": 5, "min": 1, "max": 300, "value": 5},
            "Threads": {"type": "spin", "default": 1, "min": 1, "max": 8, "value": 1},
            "OwnBook": {"type": "check", "default": "false", "value": "false"},
            "Ponder": {"type": "check", "default": "false", "value": "false"}
        }
    
    def run(self):
        """Main UCI loop"""
        while True:
            try:
                line = input().strip()
                if not line:
                    continue
                
                response = self.process_command(line)
                if response:
                    print(response)
                    sys.stdout.flush()
                    
            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                sys.stdout.flush()
    
    def process_command(self, command: str) -> Optional[str]:
        """
        Process UCI command
        
        Args:
            command: UCI command string
            
        Returns:
            Response string (None if no response needed)
        """
        parts = command.split()
        if not parts:
            return None
        
        cmd = parts[0].lower()
        
        if cmd == "uci":
            return self.handle_uci()
        elif cmd == "isready":
            return self.handle_isready()
        elif cmd == "ucinewgame":
            return self.handle_ucinewgame()
        elif cmd == "position":
            return self.handle_position(parts[1:])
        elif cmd == "go":
            return self.handle_go(parts[1:])
        elif cmd == "stop":
            return self.handle_stop()
        elif cmd == "quit":
            return self.handle_quit()
        elif cmd == "setoption":
            return self.handle_setoption(parts[1:])
        elif cmd == "debug":
            return self.handle_debug(parts[1:])
        elif cmd == "register":
            return self.handle_register(parts[1:])
        else:
            return f"Unknown command: {command}"
    
    def handle_uci(self) -> str:
        """Handle UCI command"""
        response = []
        response.append("id name ChessEngine 1.0")
        response.append("id author Chess Engine Team")
        
        # Engine options
        for name, option in self.options.items():
            option_str = f"option name {name} type {option['type']}"
            
            if option["type"] == "spin":
                option_str += f" default {option['default']} min {option['min']} max {option['max']}"
            elif option["type"] == "check":
                option_str += f" default {option['default']}"
            elif option["type"] == "string":
                option_str += f" default {option['default']}"
            elif option["type"] == "combo":
                option_str += f" default {option['default']}"
                for var in option.get("var", []):
                    option_str += f" var {var}"
            
            response.append(option_str)
        
        response.append("uciok")
        return "\n".join(response)
    
    def handle_isready(self) -> str:
        """Handle isready command"""
        self.is_ready = True
        return "readyok"
    
    def handle_ucinewgame(self) -> str:
        """Handle ucinewgame command"""
        self.board = ChessBoard()
        self.engine.clear_tables()
        return None
    
    def handle_position(self, args: List[str]) -> str:
        """Handle position command"""
        if not args:
            return "Error: position command requires arguments"
        
        # Parse position command
        if args[0] == "startpos":
            self.board = ChessBoard()
            moves_start = 1
        elif args[0] == "fen":
            # Parse FEN string
            fen_parts = []
            i = 1
            while i < len(args) and args[i] != "moves":
                fen_parts.append(args[i])
                i += 1
            fen = " ".join(fen_parts)
            self.board = ChessBoard(fen)
            moves_start = i + 1 if i < len(args) and args[i] == "moves" else len(args)
        else:
            return "Error: Invalid position command"
        
        # Apply moves
        if moves_start < len(args):
            for move_str in args[moves_start:]:
                move = self._parse_move(move_str)
                if move and not self.board.make_move(move):
                    return f"Error: Invalid move {move_str}"
        
        return None
    
    def handle_go(self, args: List[str]) -> str:
        """Handle go command"""
        if not self.is_ready:
            return "Error: Engine not ready"
        
        # Parse go parameters
        search_time = self.search_time
        search_depth = self.search_depth
        infinite = False
        
        i = 0
        while i < len(args):
            if args[i] == "wtime" and i + 1 < len(args):
                # White time in milliseconds
                search_time = int(args[i + 1]) / 1000.0
                i += 2
            elif args[i] == "btime" and i + 1 < len(args):
                # Black time in milliseconds
                search_time = int(args[i + 1]) / 1000.0
                i += 2
            elif args[i] == "winc" and i + 1 < len(args):
                # White increment
                i += 2
            elif args[i] == "binc" and i + 1 < len(args):
                # Black increment
                i += 2
            elif args[i] == "movetime" and i + 1 < len(args):
                # Fixed time per move
                search_time = int(args[i + 1]) / 1000.0
                i += 2
            elif args[i] == "depth" and i + 1 < len(args):
                search_depth = int(args[i + 1])
                i += 2
            elif args[i] == "infinite":
                infinite = True
                i += 1
            else:
                i += 1
        
        # Start search
        self._start_search(search_time, search_depth, infinite)
        return None
    
    def handle_stop(self) -> str:
        """Handle stop command"""
        # TODO: Implement search stopping
        return None
    
    def handle_quit(self) -> str:
        """Handle quit command"""
        sys.exit(0)
    
    def handle_setoption(self, args: List[str]) -> str:
        """Handle setoption command"""
        if len(args) < 4 or args[0] != "name" or args[2] != "value":
            return "Error: Invalid setoption command"
        
        option_name = args[1]
        option_value = args[3]
        
        if option_name in self.options:
            if self.options[option_name]["type"] == "spin":
                try:
                    value = int(option_value)
                    if self.options[option_name]["min"] <= value <= self.options[option_name]["max"]:
                        self.options[option_name]["value"] = value
                        
                        # Apply option
                        if option_name == "Depth":
                            self.search_depth = value
                        elif option_name == "Time":
                            self.search_time = value
                            
                except ValueError:
                    return f"Error: Invalid value for {option_name}"
            elif self.options[option_name]["type"] == "check":
                if option_value in ["true", "false"]:
                    self.options[option_name]["value"] = option_value
                else:
                    return f"Error: Invalid value for {option_name}"
            else:
                self.options[option_name]["value"] = option_value
        else:
            return f"Error: Unknown option {option_name}"
        
        return None
    
    def handle_debug(self, args: List[str]) -> str:
        """Handle debug command"""
        # TODO: Implement debug mode
        return None
    
    def handle_register(self, args: List[str]) -> str:
        """Handle register command"""
        # TODO: Implement registration
        return None
    
    def _parse_move(self, move_str: str):
        """Parse UCI move string"""
        # TODO: Implement UCI move parsing
        # Convert from UCI format (e.g., "e2e4") to internal Move object
        return None
    
    def _start_search(self, search_time: float, search_depth: int, infinite: bool):
        """Start search and return best move"""
        # Set engine parameters
        self.engine.max_depth = search_depth
        self.engine.time_limit = search_time
        
        # Start search
        start_time = time.time()
        best_move, score = self.engine.search(self.board)
        search_time_used = time.time() - start_time
        
        # Send best move
        if best_move:
            move_str = self._format_move(best_move)
            print(f"bestmove {move_str}")
        else:
            print("bestmove 0000")  # No legal moves
        
        sys.stdout.flush()
    
    def _format_move(self, move) -> str:
        """Format move as UCI string"""
        # TODO: Implement move formatting
        # Convert internal Move object to UCI format (e.g., "e2e4")
        return "e2e4"  # Placeholder