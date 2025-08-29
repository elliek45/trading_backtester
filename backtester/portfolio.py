"""
Portfolio management for the backtesting engine.

This module handles portfolio operations including position management,
trade execution, and value tracking.
"""

import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
import logging


class Portfolio:
    """
    Portfolio management class for tracking positions and executing trades.
    
    This class handles:
    - Cash and position management
    - Trade execution with commission handling
    - Portfolio value tracking
    - Position sizing calculations
    """
    
    def __init__(self, initial_capital: float, commission: float = 0.001):
        """
        Initialize the portfolio.
        
        Args:
            initial_capital: Starting cash amount
            commission: Commission rate per trade (as a decimal)
        """
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.shares = 0.0
        self.commission = commission
        self.current_price = 0.0
        self.logger = logging.getLogger(__name__)
        
        # Track portfolio history
        self.history = []
        
    def execute_trade(
        self,
        date: datetime,
        price: float,
        signal: int,
        volume: Optional[float] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Execute a trade based on the signal.
        
        Args:
            date: Trade date
            price: Current price
            signal: Trade signal (1 for buy, -1 for sell, 0 for hold)
            volume: Trading volume (optional)
            
        Returns:
            Trade record if trade was executed, None otherwise
        """
        if signal == 0:
            return None
            
        self.current_price = price
        trade_record = {
            'date': date,
            'price': price,
            'signal': signal,
            'shares_before': self.shares,
            'cash_before': self.cash,
            'commission': 0.0,
            'pnl': 0.0
        }
        
        if signal == 1:  # Buy signal
            trade_record = self._execute_buy(trade_record)
        elif signal == -1:  # Sell signal
            trade_record = self._execute_sell(trade_record)
            
        if trade_record['shares_traded'] > 0:
            self.logger.info(f"Trade executed: {signal} {trade_record['shares_traded']:.2f} shares at ${price:.2f}")
            return trade_record
            
        return None
    
    def _execute_buy(self, trade_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a buy trade."""
        # Calculate position size (use all available cash)
        max_shares = self.cash / (self.current_price * (1 + self.commission))
        shares_to_buy = max_shares
        
        if shares_to_buy > 0:
            # Calculate costs
            trade_value = shares_to_buy * self.current_price
            commission_cost = trade_value * self.commission
            total_cost = trade_value + commission_cost
            
            # Update portfolio
            self.cash -= total_cost
            self.shares += shares_to_buy
            
            # Update trade record
            trade_record.update({
                'shares_traded': shares_to_buy,
                'trade_value': trade_value,
                'commission': commission_cost,
                'shares_after': self.shares,
                'cash_after': self.cash
            })
        else:
            trade_record['shares_traded'] = 0
            
        return trade_record
    
    def _execute_sell(self, trade_record: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a sell trade."""
        if self.shares <= 0:
            trade_record['shares_traded'] = 0
            return trade_record
            
        # Sell all shares
        shares_to_sell = self.shares
        
        # Calculate proceeds
        trade_value = shares_to_sell * self.current_price
        commission_cost = trade_value * self.commission
        net_proceeds = trade_value - commission_cost
        
        # Update portfolio
        self.cash += net_proceeds
        self.shares -= shares_to_sell
        
        # Calculate P&L
        pnl = net_proceeds - (shares_to_sell * self.current_price)
        
        # Update trade record
        trade_record.update({
            'shares_traded': shares_to_sell,
            'trade_value': trade_value,
            'commission': commission_cost,
            'pnl': pnl,
            'shares_after': self.shares,
            'cash_after': self.cash
        })
        
        return trade_record
    
    def update_value(self, date: datetime, price: float):
        """Update portfolio value for tracking."""
        self.current_price = price
        total_value = self.get_total_value(price)
        
        self.history.append({
            'date': date,
            'price': price,
            'cash': self.cash,
            'shares': self.shares,
            'total_value': total_value,
            'position_value': self.get_position_value(price)
        })
    
    def get_total_value(self, price: float) -> float:
        """Calculate total portfolio value."""
        return self.cash + (self.shares * price)
    
    def get_position_value(self, price: float) -> float:
        """Calculate current position value."""
        return self.shares * price
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get current portfolio summary."""
        return {
            'cash': self.cash,
            'shares': self.shares,
            'current_price': self.current_price,
            'position_value': self.get_position_value(self.current_price),
            'total_value': self.get_total_value(self.current_price),
            'total_return': (self.get_total_value(self.current_price) / self.initial_capital) - 1
        }
    
    def get_history(self) -> pd.DataFrame:
        """Get portfolio history as DataFrame."""
        if not self.history:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.history)
        df.set_index('date', inplace=True)
        return df
