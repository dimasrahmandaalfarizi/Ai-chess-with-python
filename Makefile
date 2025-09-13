# Chess Engine Makefile

.PHONY: help install test demo clean format lint run-uci run-play run-train run-tune

# Default target
help:
	@echo "Chess Engine - Available Commands:"
	@echo "  install     Install dependencies"
	@echo "  test        Run all tests"
	@echo "  demo        Run demos"
	@echo "  clean       Clean temporary files"
	@echo "  format      Format code with black"
	@echo "  lint        Run linting with flake8"
	@echo "  run-uci     Run UCI interface"
	@echo "  run-play    Run interactive play mode"
	@echo "  run-train   Run training mode"
	@echo "  run-tune    Run weight tuning mode"

# Installation
install:
	pip install -r requirements.txt

# Testing
test:
	python run_tests.py --test all

test-board:
	python run_tests.py --test board

test-search:
	python run_tests.py --test search

test-eval:
	python run_tests.py --test eval

# Demos
demo:
	python run_demo.py --demo all

demo-quick:
	python run_demo.py --demo quick

demo-usage:
	python run_demo.py --demo usage

demo-training:
	python run_demo.py --demo training

demo-uci:
	python run_demo.py --demo uci

# Code quality
format:
	black chess_engine/ main.py run_tests.py run_demo.py examples/

lint:
	flake8 chess_engine/ main.py run_tests.py run_demo.py examples/

# Running the engine
run-uci:
	python main.py uci

run-play:
	python main.py play

run-train:
	python main.py train

run-tune:
	python main.py tune

# Cleanup
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name "*.egg-info" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/

# Development setup
dev-setup: install
	mkdir -p data
	mkdir -p logs
	@echo "Development environment setup complete!"

# Full test suite
test-full: lint test demo
	@echo "Full test suite completed successfully!"

# Build package
build:
	python setup.py sdist bdist_wheel

# Install in development mode
dev-install:
	pip install -e .

# Run specific examples
example-basic:
	python examples/basic_usage.py

example-training:
	python examples/training_example.py

example-uci:
	python examples/uci_example.py