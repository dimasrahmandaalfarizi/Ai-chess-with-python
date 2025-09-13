"""
UCI Interface Example for Chess Engine

This file demonstrates how to use the UCI interface for chess GUIs.
"""

import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from chess_engine.uci.uci_interface import UCIInterface

def example_uci_commands():
    """Example: UCI command handling"""
    print("=== UCI Command Examples ===")
    
    uci = UCIInterface()
    
    print("UCI Interface initialized")
    print("Available commands:")
    print()
    
    # Test UCI command
    print("1. Testing 'uci' command:")
    response = uci.process_command("uci")
    print("Response:")
    print(response)
    print()
    
    # Test isready command
    print("2. Testing 'isready' command:")
    response = uci.process_command("isready")
    print("Response:")
    print(response)
    print()
    
    # Test position command
    print("3. Testing 'position startpos' command:")
    response = uci.process_command("position startpos")
    print("Response:")
    print(response if response else "No response (command processed)")
    print()
    
    # Test go command
    print("4. Testing 'go depth 2' command:")
    response = uci.process_command("go depth 2")
    print("Response:")
    print(response if response else "No response (command processed)")
    print()

def example_uci_options():
    """Example: UCI options handling"""
    print("=== UCI Options Example ===")
    
    uci = UCIInterface()
    
    print("Available UCI options:")
    for name, option in uci.options.items():
        print(f"  {name}: {option['type']} (default: {option['default']})")
    print()
    
    # Test setting options
    print("Setting options:")
    
    # Set depth
    print("1. Setting depth to 6:")
    response = uci.process_command("setoption name Depth value 6")
    print(f"Response: {response if response else 'No response (option set)'}")
    print(f"Current depth: {uci.search_depth}")
    print()
    
    # Set time
    print("2. Setting time to 10 seconds:")
    response = uci.process_command("setoption name Time value 10")
    print(f"Response: {response if response else 'No response (option set)'}")
    print(f"Current time: {uci.search_time}")
    print()
    
    # Set hash size
    print("3. Setting hash size to 128 MB:")
    response = uci.process_command("setoption name Hash value 128")
    print(f"Response: {response if response else 'No response (option set)'}")
    print()

def example_uci_protocol_flow():
    """Example: Complete UCI protocol flow"""
    print("=== UCI Protocol Flow Example ===")
    
    uci = UCIInterface()
    
    print("Simulating complete UCI protocol flow:")
    print()
    
    # 1. UCI identification
    print("1. UCI identification:")
    response = uci.process_command("uci")
    print("Engine response:")
    print(response)
    print()
    
    # 2. Ready check
    print("2. Ready check:")
    response = uci.process_command("isready")
    print("Engine response:")
    print(response)
    print()
    
    # 3. New game
    print("3. New game:")
    response = uci.process_command("ucinewgame")
    print("Engine response:")
    print(response if response else "No response (game started)")
    print()
    
    # 4. Set position
    print("4. Set position (starting position):")
    response = uci.process_command("position startpos")
    print("Engine response:")
    print(response if response else "No response (position set)")
    print()
    
    # 5. Search for move
    print("5. Search for best move:")
    response = uci.process_command("go depth 2")
    print("Engine response:")
    print(response if response else "No response (search started)")
    print()
    
    # 6. Stop search
    print("6. Stop search:")
    response = uci.process_command("stop")
    print("Engine response:")
    print(response if response else "No response (search stopped)")
    print()

def example_uci_gui_integration():
    """Example: GUI integration instructions"""
    print("=== UCI GUI Integration ===")
    
    print("To use this engine with chess GUIs:")
    print()
    
    print("1. Arena Chess GUI:")
    print("   - Download Arena from: http://www.playwitharena.com/")
    print("   - Go to Engine -> Install New Engine")
    print("   - Select: python main.py uci")
    print("   - Set working directory to this project folder")
    print()
    
    print("2. CuteChess GUI:")
    print("   - Download CuteChess from: https://cutechess.com/")
    print("   - Go to Engine -> New Engine")
    print("   - Command: python main.py uci")
    print("   - Working directory: this project folder")
    print()
    
    print("3. ChessBase:")
    print("   - Go to Engine -> Install Engine")
    print("   - Select: python main.py uci")
    print("   - Set working directory to this project folder")
    print()
    
    print("4. Command line testing:")
    print("   - Run: python main.py uci")
    print("   - Type UCI commands manually")
    print("   - Example commands:")
    print("     uci")
    print("     isready")
    print("     position startpos")
    print("     go depth 3")
    print("     quit")
    print()

def example_uci_debugging():
    """Example: UCI debugging and testing"""
    print("=== UCI Debugging Example ===")
    
    print("Debugging UCI interface:")
    print()
    
    print("1. Enable verbose output:")
    print("   - Modify UCIInterface to add print statements")
    print("   - Log all incoming commands")
    print("   - Log all outgoing responses")
    print()
    
    print("2. Test individual commands:")
    print("   - Create test cases for each UCI command")
    print("   - Verify correct responses")
    print("   - Check error handling")
    print()
    
    print("3. Performance testing:")
    print("   - Measure response times")
    print("   - Test with different positions")
    print("   - Verify search quality")
    print()
    
    print("4. Compatibility testing:")
    print("   - Test with different GUIs")
    print("   - Verify UCI protocol compliance")
    print("   - Check option handling")
    print()

if __name__ == "__main__":
    print("Chess Engine - UCI Interface Examples\n")
    
    try:
        example_uci_commands()
        example_uci_options()
        example_uci_protocol_flow()
        example_uci_gui_integration()
        example_uci_debugging()
        
        print("All UCI examples completed!")
        print("\nTo run the UCI interface:")
        print("  python main.py uci")
        print("\nTo test with a chess GUI:")
        print("  1. Install a chess GUI (Arena, CuteChess, etc.)")
        print("  2. Add engine: python main.py uci")
        print("  3. Set working directory to this project folder")
        
    except Exception as e:
        print(f"Example failed with error: {e}")
        print("This might be due to missing dependencies or incomplete implementation.")
        print("Please check the requirements.txt and install necessary packages.")