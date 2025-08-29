"""
Base strategy class for trading strategies.

This module defines the base interface that all trading strategies
must implement.
"""

import pandas as pd
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import logging


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    
    This class defines the interface that all trading strategies
    must implement. Subclasses should override the abstract methods
    to implement specific trading logic.
    """
    
    def __init__(self, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize the strategy.
        
        Args:
            parameters: Dictionary of strategy parameters
        """
        self.parameters = parameters or {}
        self.logger = logging.getLogger(self.__class__.__name__)
        self.name = self.__class__.__name__
        
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals from market data.
        
        This is the main method that subclasses must implement.
        It should analyze the input data and return a series of
        trading signals where:
        - 1 = Buy signal
        - -1 = Sell signal
        - 0 = Hold/no signal
        
        Args:
            data: DataFrame with OHLCV data and technical indicators
            
        Returns:
            Series of trading signals with same index as input data
        """
        pass
    
    def calculate_position_size(self, signal: int, portfolio_value: float) -> float:
        """
        Calculate the position size for a given signal.
        
        Args:
            signal: Trading signal (1, -1, or 0)
            portfolio_value: Current portfolio value
            
        Returns:
            Position size as a fraction of portfolio value
        """
        # Default implementation: use full portfolio for each trade
        if signal != 0:
            return 1.0
        return 0.0
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.
        
        Returns:
            True if parameters are valid, False otherwise
        """
        return True
    
    def get_parameter_summary(self) -> Dict[str, Any]:
        """
        Get a summary of strategy parameters.
        
        Returns:
            Dictionary with parameter names and values
        """
        return {
            'strategy_name': self.name,
            'parameters': self.parameters.copy()
        }
    
    def preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data for the strategy.
        
        This method can be overridden by subclasses to add
        strategy-specific data preprocessing.
        
        Args:
            data: Raw market data
            
        Returns:
            Preprocessed data
        """
        return data.copy()
    
    def should_trade(self, data: pd.DataFrame, index: int) -> bool:
        """
        Determine if a trade should be executed at the given index.
        
        This method can be overridden to add additional trading
        conditions (e.g., market hours, volatility filters).
        
        Args:
            data: Market data
            index: Current data index
            
        Returns:
            True if trading should occur, False otherwise
        """
        return True
    
    def __str__(self) -> str:
        """String representation of the strategy."""
        return f"{self.name}({self.parameters})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the strategy."""
        return f"{self.__class__.__name__}(parameters={self.parameters})"
