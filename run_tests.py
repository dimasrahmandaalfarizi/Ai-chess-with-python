"""
Test Runner for Chess Engine

This script runs all unit tests and provides a summary of results.
"""

import unittest
import sys
import os
import time

# Add the chess_engine directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'chess_engine'))

def run_all_tests():
    """Run all unit tests and return results"""
    print("Chess Engine - Test Suite")
    print("=" * 50)
    print()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = 'chess_engine/tests'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Print summary
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0

def run_specific_test(test_name):
    """Run a specific test module"""
    print(f"Running {test_name}...")
    print("-" * 30)
    
    # Import and run specific test
    if test_name == "board":
        from chess_engine.tests.test_board import TestChessBoard, TestSquare
        suite = unittest.TestLoader().loadTestsFromTestCase(TestChessBoard)
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestSquare))
    elif test_name == "search":
        from chess_engine.tests.test_search import TestMinimaxEngine, TestTranspositionTable, TestQuiescenceSearch
        suite = unittest.TestLoader().loadTestsFromTestCase(TestMinimaxEngine)
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestTranspositionTable))
        suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestQuiescenceSearch))
    elif test_name == "eval":
        from chess_engine.tests.test_eval import TestEvaluationEngine
        suite = unittest.TestLoader().loadTestsFromTestCase(TestEvaluationEngine)
    else:
        print(f"Unknown test: {test_name}")
        return False
    
    # Run test
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{test_name.title()} Tests:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    
    return len(result.failures) == 0 and len(result.errors) == 0

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Chess Engine tests")
    parser.add_argument("--test", choices=["board", "search", "eval", "all"], 
                       default="all", help="Specific test to run")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    
    args = parser.parse_args()
    
    if args.test == "all":
        success = run_all_tests()
    else:
        success = run_specific_test(args.test)
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()