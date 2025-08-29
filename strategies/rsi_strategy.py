"""
RSI (Relative Strength Index) Strategy.

This strategy generates buy/sell signals based on RSI overbought
and oversold conditions.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any
from .base_strategy import BaseStrategy


class RSIStrategy(BaseStrategy):
    """
    RSI-based Trading Strategy.
    
    This strategy generates signals when RSI crosses above/below
    overbought/oversold thresholds.
    """
    
    def __init__(self, parameters: Dict[str, Any] = None):
        """
        Initialize the RSI strategy.
        
        Args:
            parameters: Dictionary containing:
                - period: RSI calculation period (default: 14)
                - oversold: Oversold threshold (default: 30)
                - overbought: Overbought threshold (default: 70)
        """
        default_params = {
            'period': 14,
            'oversold': 30,
            'overbought': 70
        }
        
        if parameters:
            default_params.update(parameters)
        
        super().__init__(default_params)
        
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        """
        Generate trading signals based on RSI levels.
        
        Args:
            data: DataFrame with OHLCV data and RSI indicator
            
        Returns:
            Series of trading signals (1, -1, 0)
        """
        # Calculate RSI if not already present
        if 'RSI' not in data.columns:
            rsi = self._calculate_rsi(data['Close'], self.parameters['period'])
        else:
            rsi = data['RSI']
        
        # Generate signals
        signals = pd.Series(0, index=data.index)
        
        # Buy signal when RSI crosses above oversold threshold
        buy_signal = (rsi > self.parameters['oversold']) & (rsi.shift(1) <= self.parameters['oversold'])
        signals[buy_signal] = 1
        
        # Sell signal when RSI crosses below overbought threshold
        sell_signal = (rsi < self.parameters['overbought']) & (rsi.shift(1) >= self.parameters['overbought'])
        signals[sell_signal] = -1
        
        return signals
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> pd.Series:
        """
        Calculate RSI (Relative Strength Index).
        
        Args:
            prices: Price series
            period: RSI calculation period
            
        Returns:
            RSI series
        """
        # Calculate price changes
        delta = prices.diff()
        
        # Separate gains and losses
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        
        # Calculate average gains and losses
        avg_gains = gains.rolling(window=period).mean()
        avg_losses = losses.rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = avg_gains / avg_losses
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def validate_parameters(self) -> bool:
        """
        Validate strategy parameters.
        
        Returns:
            True if parameters are valid
        """
        period = self.parameters.get('period', 14)
        oversold = self.parameters.get('oversold', 30)
        overbought = self.parameters.get('overbought', 70)
        
        # Check that period is positive
        if period <= 0:
            self.logger.error("RSI period must be positive")
            return False
        
        # Check that oversold is less than overbought
        if oversold >= overbought:
            self.logger.error("Oversold threshold must be less than overbought threshold")
            return False
        
        # Check that thresholds are within valid range
        if oversold < 0 or oversold > 100 or overbought < 0 or overbought > 100:
            self.logger.error("RSI thresholds must be between 0 and 100")
            return False
        
        return True
