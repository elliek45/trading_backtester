"""
Core backtesting engine for evaluating trading strategies.

This module contains the main BacktestEngine class that orchestrates
the backtesting process, including data loading, strategy execution,
and result collection.
"""

import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime
import logging

from .portfolio import Portfolio
from .data_loader import DataLoader
from strategies.base_strategy import BaseStrategy


class BacktestEngine:
    """
    Main backtesting engine for evaluating trading strategies.
    
    This class orchestrates the entire backtesting process, including:
    - Loading and preprocessing historical data
    - Executing trading strategies
    - Managing portfolio positions
    - Tracking performance metrics
    """
    
    def __init__(self, initial_capital: float = 100000.0, commission: float = 0.001):
        """
        Initialize the backtesting engine.
        
        Args:
            initial_capital: Starting capital for the backtest
            commission: Commission rate per trade (as a decimal)
        """
        self.initial_capital = initial_capital
        self.commission = commission
        self.data_loader = DataLoader()
        self.logger = logging.getLogger(__name__)
        
    def run_backtest(
        self,
        strategy: BaseStrategy,
        data_file: str = None,
        data: pd.DataFrame = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run a complete backtest for the given strategy and data.
        
        Args:
            strategy: Trading strategy to test
            data_file: Path to the historical data file
            start_date: Start date for backtest (YYYY-MM-DD)
            end_date: End date for backtest (YYYY-MM-DD)
            
        Returns:
            Dictionary containing backtest results and metrics
        """
        self.logger.info(f"Starting backtest for strategy: {strategy.__class__.__name__}")
        
        # Load and preprocess data
        if data is None:
            data = self.data_loader.load_data(data_file, start_date, end_date)
        self.logger.info(f"Loaded {len(data)} data points")
        
        # Initialize portfolio
        portfolio = Portfolio(self.initial_capital, self.commission)
        
        # Generate strategy signals
        signals = strategy.generate_signals(data)
        
        # Execute trades based on signals
        trades = []
        positions = []
        
        for i, (date, row) in enumerate(data.iterrows()):
            signal = signals.iloc[i] if i < len(signals) else 0
            
            # Execute trade if signal exists
            if signal != 0:
                trade = portfolio.execute_trade(
                    date=date,
                    price=row['Close'],
                    signal=signal,
                    volume=row['Volume']
                )
                if trade:
                    trades.append(trade)
            
            # Update portfolio value
            portfolio.update_value(date, row['Close'])
            positions.append({
                'date': date,
                'cash': portfolio.cash,
                'shares': portfolio.shares,
                'total_value': portfolio.get_total_value(row['Close']),
                'position_value': portfolio.get_position_value(row['Close'])
            })
        
        # Calculate final results
        results = self._calculate_results(data, trades, positions, portfolio)
        
        self.logger.info("Backtest completed successfully")
        return results
    
    def _calculate_results(
        self,
        data: pd.DataFrame,
        trades: list,
        positions: list,
        portfolio: Portfolio
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive backtest results and metrics.
        
        Args:
            data: Historical price data
            trades: List of executed trades
            positions: Portfolio positions over time
            portfolio: Final portfolio state
            
        Returns:
            Dictionary containing all backtest results
        """
        # Convert positions to DataFrame
        positions_df = pd.DataFrame(positions)
        positions_df.set_index('date', inplace=True)
        
        # Calculate returns
        positions_df['returns'] = positions_df['total_value'].pct_change()
        positions_df['cumulative_returns'] = (1 + positions_df['returns']).cumprod()
        
        # Calculate key metrics
        total_return = (positions_df['total_value'].iloc[-1] / self.initial_capital) - 1
        
        # Annualized return
        days = (data.index[-1] - data.index[0]).days
        annualized_return = ((1 + total_return) ** (365 / days)) - 1 if days > 0 else 0
        
        # Sharpe ratio (assuming risk-free rate of 0)
        daily_returns = positions_df['returns'].dropna()
        sharpe_ratio = (daily_returns.mean() / daily_returns.std()) * (252 ** 0.5) if daily_returns.std() > 0 else 0
        
        # Maximum drawdown
        cumulative_returns = positions_df['cumulative_returns']
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdown.min()
        
        # Trade statistics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['pnl'] > 0])
        win_rate = winning_trades / total_trades if total_trades > 0 else 0
        
        # Calculate trade P&L
        total_pnl = sum(trade['pnl'] for trade in trades)
        avg_trade_pnl = total_pnl / total_trades if total_trades > 0 else 0
        
        return {
            'data': data,
            'trades': trades,
            'positions': positions_df,
            'portfolio': portfolio,
            'metrics': {
                'total_return': total_return,
                'annualized_return': annualized_return,
                'sharpe_ratio': sharpe_ratio,
                'max_drawdown': max_drawdown,
                'total_trades': total_trades,
                'winning_trades': winning_trades,
                'win_rate': win_rate,
                'total_pnl': total_pnl,
                'avg_trade_pnl': avg_trade_pnl,
                'final_value': positions_df['total_value'].iloc[-1],
                'initial_capital': self.initial_capital,
                'commission_paid': sum(trade['commission'] for trade in trades)
            }
        }
