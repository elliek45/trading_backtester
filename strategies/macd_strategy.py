"""
MACD (Moving Average Convergence Divergence) Strategy.

This strategy generates buy/sell signals based on MACD line
crossovers with the signal line.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import BaseStrategy


class MACDStrategy(BaseStrategy):
    """
    MACD-based Trading Strategy.
    
    This strategy generates signals when the MACD line crosses
    above or below the signal line.
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        """
        Initialize the MACD strategy.
        
        Args:
            parameters: Dictionary containing:
                - fast_period: Fast EMA period (default: 12)
                - slow_period: Slow EMA period (default: 26)
                - signal_period: Signal line period (default: 9)
        """
        default_params = {
            'fast_period': 12,
            'slow_period': 26,
            'signal_period': 9
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(default_params)
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on MACD crossovers.
        
        Args:
            data: DataFrame with OHLCV data and MACD indicators
            
        Returns:
            Series of trading signals (1, -1, 0)
        """
        # Calculate MACD if not already present
        if 'MACD' not in data.columns or 'MACD_Signal' not in data.columns:
            macd, signal = self._calculate_macd(data['Close'])
        else:
            macd = data['MACD']
            signal = data['MACD_Signal']
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        
        # Buy signal when MACD crosses above signal line
        buy_signal = (macd > signal) & (macd.shift(1) <= signal.shift(1))
        signals[buy_signal] = 1
        
        # Sell signal when MACD crosses below signal line
        sell_signal = (macd < signal) & (macd.shift(1) >= signal.shift(1))
        signals[sell_signal] = -1
        
        return signals
    
    def _calculate_macd(self, prices: pd.Series) -> tuple:
        """
        Calculate MACD and signal line.
        
        Args:
            prices: Price series
            
        Returns:
            Tuple of (MACD line, Signal line)
        """
        fast_period = self.parameters['fast_period']
        slow_period = self.parameters['slow_period']
        signal_period = self.parameters['signal_period']
        
        # Calculate fast and slow EMAs
        fast_ema = prices.ewm(span=fast_period).mean()
        slow_ema = prices.ewm(span=slow_period).mean()
        
        # Calculate MACD line
        macd_line = fast_ema - slow_ema
        
        # Calculate signal line
        signal_line = macd_line.ewm(span=signal_period).mean()
        
        return macd_line, signal_line
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.
        
        Returns:
            True if parameters are valid
        """
        fast_period = self.parameters.get('fast_period', 12)
        slow_period = self.parameters.get('slow_period', 26)
        signal_period = self.parameters.get('signal_period', 9)
        
        # Check that fast period is less than slow period
        if fast_period >= slow_period:
            self.logger.error("Fast period must be less than slow period")
            return False
        
        # Check that all periods are positive
        if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
            self.logger.error("All MACD periods must be positive")
            return False
        
        return True
