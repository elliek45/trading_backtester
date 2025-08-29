"""
Performance analyzer for calculating trading metrics.

This module provides comprehensive analysis of backtest results
including returns, risk metrics, and trade statistics.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
import logging


class PerformanceAnalyzer:
    """
    Performance analyzer for backtest results.
    
    This class calculates various performance metrics including:
    - Return metrics (total, annualized, etc.)
    - Risk metrics (Sharpe ratio, drawdown, etc.)
    - Trade statistics (win rate, average trade, etc.)
    """
    
    def __init__(self):
        """Initialize the performance analyzer."""
        self.logger = logging.getLogger(__name__)
    
    def analyze(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze backtest results and calculate performance metrics.
        
        Args:
            results: Backtest results from BacktestEngine
            
        Returns:
            Dictionary containing all performance metrics
        """
        positions = results['positions']
        trades = results['trades']
        metrics = results['metrics']
        
        # Calculate additional metrics
        additional_metrics = self._calculate_additional_metrics(positions, trades)
        
        # Combine all metrics
        all_metrics = {**metrics, **additional_metrics}
        
        return all_metrics
    
    def _calculate_additional_metrics(self, positions: pd.DataFrame, trades: List[Dict]) -> Dict[str, Any]:
        """
        Calculate additional performance metrics.
        
        Args:
            positions: Portfolio positions over time
            trades: List of executed trades
            
        Returns:
            Dictionary of additional metrics
        """
        metrics = {}
        
        # Calculate volatility
        if 'returns' in positions.columns:
            daily_returns = positions['returns'].dropna()
            metrics['volatility'] = daily_returns.std() * np.sqrt(252)
            metrics['daily_volatility'] = daily_returns.std()
        
        # Calculate maximum consecutive losses
        if trades:
            trade_pnls = [trade['pnl'] for trade in trades]
            metrics['max_consecutive_losses'] = self._calculate_max_consecutive_losses(trade_pnls)
            metrics['max_consecutive_wins'] = self._calculate_max_consecutive_wins(trade_pnls)
        
        # Calculate Calmar ratio
        if 'total_return' in metrics and 'max_drawdown' in metrics:
            if abs(metrics['max_drawdown']) > 0:
                metrics['calmar_ratio'] = metrics['annualized_return'] / abs(metrics['max_drawdown'])
            else:
                metrics['calmar_ratio'] = 0
        
        # Calculate Sortino ratio
        if 'returns' in positions.columns:
            daily_returns = positions['returns'].dropna()
            negative_returns = daily_returns[daily_returns < 0]
            if len(negative_returns) > 0:
                downside_deviation = negative_returns.std() * np.sqrt(252)
                if downside_deviation > 0:
                    metrics['sortino_ratio'] = (daily_returns.mean() * 252) / downside_deviation
                else:
                    metrics['sortino_ratio'] = 0
            else:
                metrics['sortino_ratio'] = float('inf')
        
        # Calculate profit factor
        if trades:
            winning_trades = [t for t in trades if t['pnl'] > 0]
            losing_trades = [t for t in trades if t['pnl'] < 0]
            
            total_profit = sum(t['pnl'] for t in winning_trades)
            total_loss = abs(sum(t['pnl'] for t in losing_trades))
            
            if total_loss > 0:
                metrics['profit_factor'] = total_profit / total_loss
            else:
                metrics['profit_factor'] = float('inf')
        
        # Calculate average trade duration
        if trades:
            durations = []
            for trade in trades:
                if 'entry_date' in trade and 'exit_date' in trade:
                    duration = (pd.to_datetime(trade['exit_date']) - pd.to_datetime(trade['entry_date'])).days
                    durations.append(duration)
            
            if durations:
                metrics['avg_trade_duration'] = np.mean(durations)
        
        return metrics
    
    def _calculate_max_consecutive_losses(self, trade_pnls: List[float]) -> int:
        """Calculate maximum consecutive losses."""
        max_consecutive = 0
        current_consecutive = 0
        
        for pnl in trade_pnls:
            if pnl < 0:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def _calculate_max_consecutive_wins(self, trade_pnls: List[float]) -> int:
        """Calculate maximum consecutive wins."""
        max_consecutive = 0
        current_consecutive = 0
        
        for pnl in trade_pnls:
            if pnl > 0:
                current_consecutive += 1
                max_consecutive = max(max_consecutive, current_consecutive)
            else:
                current_consecutive = 0
        
        return max_consecutive
    
    def compare_strategies(self, results_list: List[Dict[str, Any]], strategy_names: List[str] = None) -> pd.DataFrame:
        """
        Compare multiple strategies.
        
        Args:
            results_list: List of backtest results
            strategy_names: List of strategy names
            
        Returns:
            DataFrame with comparison metrics
        """
        if strategy_names is None:
            strategy_names = [f"Strategy_{i+1}" for i in range(len(results_list))]
        
        comparison_data = []
        
        for i, results in enumerate(results_list):
            metrics = self.analyze(results)
            metrics['strategy_name'] = strategy_names[i]
            comparison_data.append(metrics)
        
        return pd.DataFrame(comparison_data)
    
    def generate_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a text report of the analysis.
        
        Args:
            results: Backtest results
            
        Returns:
            Formatted text report
        """
        metrics = self.analyze(results)
        
        report = []
        report.append("=" * 50)
        report.append("BACKTEST PERFORMANCE REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Return metrics
        report.append("RETURN METRICS:")
        report.append(f"  Total Return: {metrics.get('total_return', 0):.2%}")
        report.append(f"  Annualized Return: {metrics.get('annualized_return', 0):.2%}")
        report.append(f"  Volatility: {metrics.get('volatility', 0):.2%}")
        report.append("")
        
        # Risk metrics
        report.append("RISK METRICS:")
        report.append(f"  Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}")
        report.append(f"  Sortino Ratio: {metrics.get('sortino_ratio', 0):.3f}")
        report.append(f"  Calmar Ratio: {metrics.get('calmar_ratio', 0):.3f}")
        report.append(f"  Maximum Drawdown: {metrics.get('max_drawdown', 0):.2%}")
        report.append("")
        
        # Trade metrics
        report.append("TRADE METRICS:")
        report.append(f"  Total Trades: {metrics.get('total_trades', 0)}")
        report.append(f"  Win Rate: {metrics.get('win_rate', 0):.2%}")
        report.append(f"  Profit Factor: {metrics.get('profit_factor', 0):.3f}")
        report.append(f"  Average Trade P&L: ${metrics.get('avg_trade_pnl', 0):,.2f}")
        report.append("")
        
        # Portfolio metrics
        report.append("PORTFOLIO METRICS:")
        report.append(f"  Initial Capital: ${metrics.get('initial_capital', 0):,.2f}")
        report.append(f"  Final Value: ${metrics.get('final_value', 0):,.2f}")
        report.append(f"  Total Commission Paid: ${metrics.get('commission_paid', 0):,.2f}")
        
        return "\n".join(report)
