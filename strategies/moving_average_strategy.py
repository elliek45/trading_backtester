"""
Moving Average Crossover Strategy.

This strategy generates buy/sell signals based on the crossover
of two moving averages (typically a fast and slow moving average).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import BaseStrategy


class MovingAverageStrategy(BaseStrategy):
    """
    Moving Average Crossover Strategy.
    
    This strategy generates signals when a fast moving average
    crosses above or below a slow moving average.
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        """
        Initialize the Moving Average strategy.
        
        Args:
            parameters: Dictionary containing:
                - fast_period: Period for fast moving average (default: 20)
                - slow_period: Period for slow moving average (default: 50)
                - ma_type: Type of moving average ('sma' or 'ema', default: 'sma')
        """
        default_params = {
            'fast_period': 20,
            'slow_period': 50,
            'ma_type': 'sma'
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(default_params)
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on moving average crossovers.
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Series of trading signals (1, -1, 0)
        """
        # Calculate moving averages
        fast_ma = self._calculate_moving_average(data['Close'], self.parameters['fast_period'])
        slow_ma = self._calculate_moving_average(data['Close'], self.parameters['slow_period'])
        
        # Generate signals based on crossovers
        signals = pd.Series(0, index=data.index)
        
        # Buy signal when fast MA crosses above slow MA
        buy_signal = (fast_ma > slow_ma) & (fast_ma.shift(1) <= slow_ma.shift(1))
        signals[buy_signal] = 1
        
        # Sell signal when fast MA crosses below slow MA
        sell_signal = (fast_ma < slow_ma) & (fast_ma.shift(1) >= slow_ma.shift(1))
        signals[sell_signal] = -1
        
        return signals
    
    def _calculate_moving_average(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate moving average based on strategy parameters.
        
        Args:
            prices: Price series
            period: Moving average period
            
        Returns:
            Moving average series
        """
        if self.parameters['ma_type'].lower() == 'ema':
            return prices.ewm(span=period).mean()
        else:  # Default to SMA
            return prices.rolling(window=period).mean()
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.
        
        Returns:
            True if parameters are valid
        """
        fast_period = self.parameters.get('fast_period', 20)
        slow_period = self.parameters.get('slow_period', 50)
        ma_type = self.parameters.get('ma_type', 'sma')
        
        # Check that fast period is less than slow period
        if fast_period >= slow_period:
            self.logger.error("Fast period must be less than slow period")
            return False
        
        # Check that periods are positive
        if fast_period <= 0 or slow_period <= 0:
            self.logger.error("Moving average periods must be positive")
            return False
        
        # Check moving average type
        if ma_type.lower() not in ['sma', 'ema']:
            self.logger.error("Moving average type must be 'sma' or 'ema'")
            return False
        
        return True
