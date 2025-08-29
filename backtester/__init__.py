"""
Backtester module for trading strategy evaluation.

This module contains the core backtesting engine and related utilities
for evaluating trading strategies on historical data.
"""

from .engine import BacktestEngine
from .portfolio import Portfolio
from .data_loader import DataLoader

__all__ = ['BacktestEngine', 'Portfolio', 'DataLoader']
