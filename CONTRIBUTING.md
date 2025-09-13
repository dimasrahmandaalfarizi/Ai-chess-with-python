# Contributing to Chess Engine

Thank you for your interest in contributing to the Chess Engine project! This document provides guidelines for contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of chess programming concepts
- Familiarity with Python development

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/yourusername/chess-engine.git
   cd chess-engine
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/original/chess-engine.git
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -e .
pip install -r requirements.txt[dev]
```

### 3. Install Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

### 4. Run Tests

```bash
python run_tests.py
```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

1. **Bug Fixes**: Fix bugs and issues
2. **Features**: Add new functionality
3. **Documentation**: Improve documentation
4. **Tests**: Add or improve tests
5. **Performance**: Optimize existing code
6. **Refactoring**: Improve code structure

### Areas for Contribution

#### High Priority
- **Move Generation**: Improve move generation algorithms
- **Search Algorithms**: Enhance search performance
- **Evaluation Functions**: Add new evaluation features
- **UCI Protocol**: Improve UCI compatibility
- **Neural Networks**: Enhance ML capabilities

#### Medium Priority
- **Documentation**: Improve guides and examples
- **Testing**: Add more comprehensive tests
- **Performance**: Optimize critical paths
- **UI/UX**: Improve command-line interface

#### Low Priority
- **Code Style**: Improve code formatting
- **Comments**: Add better documentation
- **Examples**: Add more usage examples

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Imports**: Sorted and grouped
- **Naming**: snake_case for variables, PascalCase for classes

### Code Formatting

We use Black for code formatting:

```bash
black chess_engine/ main.py run_tests.py run_demo.py examples/
```

### Linting

We use flake8 for linting:

```bash
flake8 chess_engine/ main.py run_tests.py run_demo.py examples/
```

### Type Hints

Use type hints for function parameters and return values:

```python
def evaluate_position(self, board: ChessBoard, color: Color) -> float:
    """Evaluate chess position"""
    # Implementation
    return score
```

### Docstrings

Use Google-style docstrings:

```python
def search(self, board: ChessBoard, depth: Optional[int] = None) -> Tuple[Move, float]:
    """Search for best move using minimax with alpha-beta pruning.
    
    Args:
        board: Current chess position
        depth: Search depth (uses max_depth if None)
        
    Returns:
        Tuple of (best_move, evaluation_score)
    """
    # Implementation
```

## Testing

### Running Tests

```bash
# Run all tests
python run_tests.py

# Run specific test modules
python run_tests.py --test board
python run_tests.py --test search
python run_tests.py --test eval

# Run with verbose output
python run_tests.py --verbose
```

### Writing Tests

#### Test Structure

```python
import unittest
from chess_engine.board.board import ChessBoard

class TestNewFeature(unittest.TestCase):
    """Test cases for new feature"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.board = ChessBoard()
    
    def test_basic_functionality(self):
        """Test basic functionality"""
        # Test implementation
        self.assertTrue(condition)
    
    def test_edge_cases(self):
        """Test edge cases"""
        # Test edge cases
        self.assertRaises(ValueError, function, invalid_input)
```

#### Test Guidelines

1. **Test Coverage**: Aim for high test coverage
2. **Test Names**: Use descriptive test names
3. **Test Isolation**: Each test should be independent
4. **Edge Cases**: Test boundary conditions and error cases
5. **Performance**: Test performance-critical functions

### Test Data

Use the `test_data/` directory for test files:

```
test_data/
├── positions/
│   ├── opening.pgn
│   ├── middlegame.pgn
│   └── endgame.pgn
├── weights/
│   ├── test_weights.json
│   └── optimized_weights.json
└── models/
    ├── test_model.pth
    └── trained_model.pth
```

## Pull Request Process

### Before Submitting

1. **Sync with upstream**:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make changes**:
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation if needed

4. **Run tests**:
   ```bash
   python run_tests.py
   ```

5. **Format code**:
   ```bash
   black chess_engine/ main.py run_tests.py run_demo.py examples/
   ```

6. **Check linting**:
   ```bash
   flake8 chess_engine/ main.py run_tests.py run_demo.py examples/
   ```

### Submitting Pull Request

1. **Commit changes**:
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

2. **Push to fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**:
   - Use descriptive title
   - Provide detailed description
   - Link related issues
   - Include screenshots if applicable

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes
```

## Issue Reporting

### Before Creating Issue

1. **Search existing issues**: Check if issue already exists
2. **Check documentation**: Look for solutions in docs
3. **Reproduce issue**: Ensure issue is reproducible

### Issue Template

```markdown
## Bug Report

### Description
Clear description of the bug

### Steps to Reproduce
1. Step one
2. Step two
3. Step three

### Expected Behavior
What should happen

### Actual Behavior
What actually happens

### Environment
- OS: [e.g., Windows 10, macOS 11, Ubuntu 20.04]
- Python Version: [e.g., 3.9.0]
- Chess Engine Version: [e.g., 1.0.0]

### Additional Context
Any other relevant information
```

### Feature Request Template

```markdown
## Feature Request

### Description
Clear description of the feature

### Use Case
Why is this feature needed?

### Proposed Solution
How should this feature work?

### Alternatives
Other solutions considered

### Additional Context
Any other relevant information
```

## Code Review Process

### Review Guidelines

1. **Be constructive**: Provide helpful feedback
2. **Be specific**: Point out exact issues
3. **Be respectful**: Maintain professional tone
4. **Be thorough**: Check all aspects of the code

### Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are adequate
- [ ] Documentation is updated
- [ ] Performance is acceptable
- [ ] Security considerations addressed
- [ ] No breaking changes

## Release Process

### Version Numbering

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared

## Community Guidelines

### Code of Conduct

1. **Be respectful**: Treat everyone with respect
2. **Be inclusive**: Welcome contributors from all backgrounds
3. **Be constructive**: Provide helpful feedback
4. **Be patient**: Remember that everyone is learning

### Communication

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub discussions for general questions
- **Pull Requests**: Use PR comments for code review

## Getting Help

### Resources

1. **Documentation**: Check the `docs/` directory
2. **Examples**: Look at the `examples/` directory
3. **Tests**: Study test cases for usage examples
4. **Issues**: Search existing issues for solutions

### Questions

- **General questions**: Use GitHub discussions
- **Bug reports**: Create GitHub issues
- **Feature requests**: Create GitHub issues
- **Code questions**: Use PR comments

## Recognition

### Contributors

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

### Types of Recognition

- **Code contributions**: Code, tests, documentation
- **Bug reports**: Identifying and reporting bugs
- **Feature suggestions**: Proposing new features
- **Community help**: Helping other users

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

## Contact

For questions about contributing:
- Create a GitHub issue
- Start a GitHub discussion
- Contact the maintainers

Thank you for contributing to the Chess Engine project!