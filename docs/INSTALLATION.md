# Installation Guide

This guide provides detailed installation instructions for the Chess Engine.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Detailed Installation](#detailed-installation)
- [Docker Installation](#docker-installation)
- [Development Setup](#development-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 512 MB
- **Disk Space**: 100 MB
- **OS**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)

### Recommended Requirements
- **Python**: 3.10 or higher
- **RAM**: 2 GB or more
- **Disk Space**: 500 MB
- **GPU**: NVIDIA GPU with CUDA support (for neural network training)

## Quick Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd chess-engine
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Tests
```bash
python run_tests.py
```

### 4. Run Demo
```bash
python run_demo.py
```

## Detailed Installation

### Step 1: Python Installation

#### Windows
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH"
3. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### macOS
```bash
# Using Homebrew
brew install python

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv chess-engine-env

# Activate virtual environment
# Windows
chess-engine-env\Scripts\activate

# macOS/Linux
source chess-engine-env/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install -r requirements.txt[dev]

# Install with all optional dependencies
pip install -r requirements.txt[dev,plot,ml]
```

### Step 4: Verify Installation

```bash
# Run tests
python run_tests.py

# Run demo
python run_demo.py --demo quick

# Test UCI interface
python main.py uci
```

## Docker Installation

### Prerequisites
- Docker installed on your system
- Docker Compose (optional)

### Method 1: Using Docker Compose

```bash
# Clone repository
git clone <repository-url>
cd chess-engine

# Build and run
docker-compose up chess-engine

# Run in play mode
docker-compose up chess-engine-play

# Run training
docker-compose up chess-engine-train
```

### Method 2: Using Docker Directly

```bash
# Build image
docker build -t chess-engine .

# Run UCI interface
docker run -it chess-engine

# Run in play mode
docker run -it chess-engine python main.py play

# Run with volume mount for data
docker run -it -v $(pwd)/data:/app/data chess-engine
```

## Development Setup

### 1. Clone Repository
```bash
git clone <repository-url>
cd chess-engine
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Development Dependencies
```bash
pip install -e .
pip install -r requirements.txt[dev]
```

### 4. Set Up Pre-commit Hooks (Optional)
```bash
pip install pre-commit
pre-commit install
```

### 5. Create Data Directory
```bash
mkdir -p data logs
```

### 6. Run Development Tests
```bash
# Run all tests
make test

# Run specific tests
make test-board
make test-search
make test-eval

# Run demos
make demo
```

## Verification

### Basic Functionality Test
```bash
python run_demo.py --demo quick
```

Expected output:
```
Chess Engine - Demo Runner
Running Quick Test...
=============================
1. Testing board creation...
   ✓ Board created successfully
2. Testing move generation...
   ✓ Generated 20 legal moves
3. Testing position evaluation...
   ✓ Position evaluation: 0.00
4. Testing search algorithm...
   ✓ Search completed: [move] (score: [score])

✅ Quick test passed!
```

### UCI Interface Test
```bash
python main.py uci
```

Then type:
```
uci
isready
position startpos
go depth 2
quit
```

### Interactive Play Test
```bash
python main.py play
```

Then try:
```
engine
eval
new
quit
```

## Troubleshooting

### Common Issues

#### 1. Python Version Error
**Error**: `Python 3.8+ is required`

**Solution**: Upgrade Python or use pyenv:
```bash
# Using pyenv
pyenv install 3.10.0
pyenv local 3.10.0
```

#### 2. Module Import Error
**Error**: `ModuleNotFoundError: No module named 'chess_engine'`

**Solution**: Run from project root directory:
```bash
cd chess-engine
python main.py
```

#### 3. Permission Denied
**Error**: Permission denied when installing packages

**Solution**: Use virtual environment or install with user flag:
```bash
pip install --user -r requirements.txt
```

#### 4. CUDA/GPU Issues
**Error**: CUDA out of memory or GPU not found

**Solution**: Use CPU-only version or reduce batch size:
```bash
# Install CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Or use CPU in training
python main.py train --batch-size 8
```

#### 5. Memory Issues
**Error**: Out of memory during search or training

**Solution**: Reduce search depth or batch size:
```bash
# Reduce search depth
python main.py play --depth 2

# Reduce training batch size
python main.py train --batch-size 16
```

### Platform-Specific Issues

#### Windows
- Ensure Python is added to PATH
- Use Command Prompt as Administrator if needed
- Install Visual C++ Build Tools for some packages

#### macOS
- Use `python3` instead of `python` if both versions are installed
- Install Xcode Command Line Tools: `xcode-select --install`

#### Linux
- Install build essentials: `sudo apt install build-essential`
- Install Python development headers: `sudo apt install python3-dev`

### Getting Help

If you encounter issues not covered here:

1. Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
2. Run tests to identify specific problems
3. Check Python and package versions
4. Verify file permissions and paths
5. Create an issue with detailed error information

### Performance Optimization

#### For Better Search Performance
```bash
# Use higher search depth
python main.py play --depth 6

# Increase time limit
python main.py play --time 10
```

#### For Training Performance
```bash
# Use GPU if available
python main.py train --epochs 100

# Use larger batch size
python main.py train --batch-size 64
```

#### For Memory Optimization
```bash
# Clear caches regularly
python -c "from chess_engine.search.minimax import MinimaxEngine; engine = MinimaxEngine(); engine.clear_tables()"
```

## Next Steps

After successful installation:

1. **Read the [User Guide](USER_GUIDE.md)** for basic usage
2. **Check the [API Documentation](API.md)** for advanced features
3. **Run the [Examples](examples/)** to learn different use cases
4. **Explore the [Training Guide](TRAINING.md)** for machine learning features
5. **Join the community** for support and contributions

## Uninstallation

To remove the Chess Engine:

```bash
# Remove virtual environment
rm -rf chess-engine-env

# Remove installed packages
pip uninstall chess-engine

# Remove project directory
rm -rf chess-engine
```

## Support

For additional help:
- Check the documentation in the `docs/` directory
- Run `python main.py --help` for command-line options
- Create an issue on the project repository
- Join the community discussions