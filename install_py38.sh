#!/bin/bash
# Installation script for Python 3.8 compatibility

echo "Installing Python 3.8 compatible packages..."
echo "============================================="

# Install core packages with specific versions for Python 3.8
echo "Installing pandas..."
pip3 install "pandas>=1.5.0,<2.0.0"

echo "Installing numpy..."
pip3 install "numpy>=1.21.0,<1.25.0"

echo "Installing matplotlib..."
pip3 install "matplotlib>=3.5.0,<3.8.0"

echo "Installing seaborn..."
pip3 install "seaborn>=0.11.0,<0.12.0"

echo "Installing plotly..."
pip3 install "plotly>=5.0.0,<5.16.0"

echo "Installing scipy..."
pip3 install "scipy>=1.7.0,<1.11.0"

echo "Installing yfinance (older version for Python 3.8)..."
pip3 install "yfinance>=0.1.87,<0.2.0"

echo "Installing testing packages..."
pip3 install "pytest>=6.0.0,<7.5.0"
pip3 install "pytest-cov>=3.0.0,<4.2.0"

echo ""
echo "Installation complete!"
echo "Now you can test the project with:"
echo "  python3 test_simple.py"
echo "  python3 main.py --list-strategies"
