"""
Visualizer for creating charts and plots from backtest results.

This module provides various visualization tools for analyzing
backtest performance and results.
"""

import pandas as pd
import numpy as np
import matplotlib
# Set matplotlib to use non-interactive backend for saving plots
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, Any, List, Optional
import logging

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")


class Visualizer:
    """
    Visualizer for backtest results.
    
    This class provides various plotting functions for analyzing
    backtest performance and results.
    """
    
    def __init__(self):
        """Initialize the visualizer."""
        self.logger = logging.getLogger(__name__)
    
    def plot_portfolio_performance(self, results: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot portfolio performance over time.
        
        Args:
            results: Backtest results
            save_path: Optional path to save the plot
        """
        positions = results['positions']
        data = results['data']
        
        fig, axes = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot 1: Price and portfolio value
        ax1 = axes[0]
        ax1.plot(data.index, data['Close'], label='Asset Price', alpha=0.7)
        ax1.plot(positions.index, positions['total_value'], label='Portfolio Value', linewidth=2)
        ax1.set_title('Portfolio Performance vs Asset Price')
        ax1.set_ylabel('Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Cumulative returns
        ax2 = axes[1]
        if 'cumulative_returns' in positions.columns:
            ax2.plot(positions.index, positions['cumulative_returns'], label='Cumulative Returns', linewidth=2)
        ax2.axhline(y=1, color='black', linestyle='--', alpha=0.5, label='Initial Investment')
        ax2.set_title('Cumulative Returns')
        ax2.set_ylabel('Cumulative Return')
        ax2.set_xlabel('Date')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Portfolio performance plot saved to {save_path}")
        else:
            # Save to a default location if no path specified
            default_path = "portfolio_performance.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Portfolio performance plot saved to {default_path}")
        
        plt.close()  # Close the plot to free memory
    
    def plot_drawdown(self, results: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot drawdown analysis.
        
        Args:
            results: Backtest results
            save_path: Optional path to save the plot
        """
        positions = results['positions']
        
        if 'cumulative_returns' not in positions.columns:
            self.logger.warning("Cumulative returns not available for drawdown plot")
            return
        
        # Calculate drawdown
        cumulative_returns = positions['cumulative_returns']
        running_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - running_max) / running_max
        
        plt.figure(figsize=(12, 6))
        plt.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color='red')
        plt.plot(drawdown.index, drawdown.values, color='red', linewidth=1)
        plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
        plt.title('Portfolio Drawdown')
        plt.ylabel('Drawdown (%)')
        plt.xlabel('Date')
        plt.grid(True, alpha=0.3)
        
        # Add max drawdown annotation
        max_dd_idx = drawdown.idxmin()
        max_dd = drawdown.min()
        plt.annotate(f'Max Drawdown: {max_dd:.2%}', 
                    xy=(max_dd_idx, max_dd), 
                    xytext=(max_dd_idx, max_dd/2),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=10)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Drawdown plot saved to {save_path}")
        else:
            # Save to a default location if no path specified
            default_path = "drawdown_analysis.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Drawdown plot saved to {default_path}")
        
        plt.close()  # Close the plot to free memory
    
    def plot_trade_analysis(self, results: Dict[str, Any], save_path: Optional[str] = None):
        """
        Plot trade analysis.
        
        Args:
            results: Backtest results
            save_path: Optional path to save the plot
        """
        trades = results['trades']
        
        if not trades:
            self.logger.warning("No trades available for analysis")
            return
        
        # Convert trades to DataFrame
        trades_df = pd.DataFrame(trades)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Trade P&L distribution
        ax1 = axes[0, 0]
        ax1.hist(trades_df['pnl'], bins=20, alpha=0.7, edgecolor='black')
        ax1.axvline(x=0, color='red', linestyle='--', alpha=0.7)
        ax1.set_title('Trade P&L Distribution')
        ax1.set_xlabel('P&L ($)')
        ax1.set_ylabel('Frequency')
        
        # Plot 2: Cumulative P&L
        ax2 = axes[0, 1]
        cumulative_pnl = trades_df['pnl'].cumsum()
        ax2.plot(cumulative_pnl.index, cumulative_pnl.values, linewidth=2)
        ax2.set_title('Cumulative P&L')
        ax2.set_xlabel('Trade Number')
        ax2.set_ylabel('Cumulative P&L ($)')
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Trade size vs P&L
        ax3 = axes[1, 0]
        ax3.scatter(trades_df['trade_value'], trades_df['pnl'], alpha=0.6)
        ax3.set_title('Trade Size vs P&L')
        ax3.set_xlabel('Trade Value ($)')
        ax3.set_ylabel('P&L ($)')
        
        # Plot 4: Win/Loss ratio over time
        ax4 = axes[1, 1]
        winning_trades = (trades_df['pnl'] > 0).cumsum()
        total_trades = np.arange(1, len(trades_df) + 1)
        win_rate = winning_trades / total_trades
        ax4.plot(win_rate.index, win_rate.values, linewidth=2)
        ax4.set_title('Win Rate Over Time')
        ax4.set_xlabel('Trade Number')
        ax4.set_ylabel('Win Rate')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Trade analysis plot saved to {save_path}")
        else:
            # Save to a default location if no path specified
            default_path = "trade_analysis.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Trade analysis plot saved to {default_path}")
        
        plt.close()  # Close the plot to free memory
    
    def plot_strategy_comparison(self, results_list: List[Dict[str, Any]], 
                               strategy_names: List[str], 
                               save_path: Optional[str] = None):
        """
        Plot comparison of multiple strategies.
        
        Args:
            results_list: List of backtest results
            strategy_names: List of strategy names
            save_path: Optional path to save the plot
        """
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Plot 1: Cumulative returns comparison
        ax1 = axes[0, 0]
        for i, results in enumerate(results_list):
            positions = results['positions']
            if 'cumulative_returns' in positions.columns:
                ax1.plot(positions.index, positions['cumulative_returns'], 
                        label=strategy_names[i], linewidth=2)
        ax1.set_title('Cumulative Returns Comparison')
        ax1.set_ylabel('Cumulative Return')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Drawdown comparison
        ax2 = axes[0, 1]
        for i, results in enumerate(results_list):
            positions = results['positions']
            if 'cumulative_returns' in positions.columns:
                cumulative_returns = positions['cumulative_returns']
                running_max = cumulative_returns.expanding().max()
                drawdown = (cumulative_returns - running_max) / running_max
                ax2.plot(drawdown.index, drawdown.values, 
                        label=strategy_names[i], linewidth=2)
        ax2.set_title('Drawdown Comparison')
        ax2.set_ylabel('Drawdown (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Monthly returns heatmap
        ax3 = axes[1, 0]
        # This would require additional data processing for monthly returns
        ax3.text(0.5, 0.5, 'Monthly Returns Heatmap\n(Not implemented)', 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Monthly Returns Heatmap')
        
        # Plot 4: Risk-return scatter
        ax4 = axes[1, 1]
        returns = []
        volatilities = []
        for results in results_list:
            metrics = results['metrics']
            returns.append(metrics.get('annualized_return', 0))
            volatilities.append(metrics.get('volatility', 0))
        
        ax4.scatter(volatilities, returns, s=100, alpha=0.7)
        for i, name in enumerate(strategy_names):
            ax4.annotate(name, (volatilities[i], returns[i]), 
                        xytext=(5, 5), textcoords='offset points')
        ax4.set_title('Risk-Return Profile')
        ax4.set_xlabel('Volatility')
        ax4.set_ylabel('Annualized Return')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Strategy comparison plot saved to {save_path}")
        else:
            # Save to a default location if no path specified
            default_path = "strategy_comparison.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Strategy comparison plot saved to {default_path}")
        
        plt.close()  # Close the plot to free memory
    
    def create_dashboard(self, results: Dict[str, Any], save_path: Optional[str] = None):
        """
        Create a comprehensive dashboard with multiple plots.
        
        Args:
            results: Backtest results
            save_path: Optional path to save the dashboard
        """
        fig = plt.figure(figsize=(20, 12))
        
        # Create subplots
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Portfolio performance
        ax1 = fig.add_subplot(gs[0, :2])
        positions = results['positions']
        data = results['data']
        ax1.plot(data.index, data['Close'], label='Asset Price', alpha=0.7)
        ax1.plot(positions.index, positions['total_value'], label='Portfolio Value', linewidth=2)
        ax1.set_title('Portfolio Performance')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Drawdown
        ax2 = fig.add_subplot(gs[0, 2])
        if 'cumulative_returns' in positions.columns:
            cumulative_returns = positions['cumulative_returns']
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            ax2.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color='red')
            ax2.set_title('Drawdown')
            ax2.grid(True, alpha=0.3)
        
        # Trade P&L distribution
        ax3 = fig.add_subplot(gs[1, 0])
        trades = results['trades']
        if trades:
            trades_df = pd.DataFrame(trades)
            ax3.hist(trades_df['pnl'], bins=15, alpha=0.7, edgecolor='black')
            ax3.axvline(x=0, color='red', linestyle='--', alpha=0.7)
            ax3.set_title('Trade P&L Distribution')
        
        # Cumulative P&L
        ax4 = fig.add_subplot(gs[1, 1])
        if trades:
            cumulative_pnl = trades_df['pnl'].cumsum()
            ax4.plot(cumulative_pnl.index, cumulative_pnl.values, linewidth=2)
            ax4.set_title('Cumulative P&L')
            ax4.grid(True, alpha=0.3)
        
        # Win rate over time
        ax5 = fig.add_subplot(gs[1, 2])
        if trades:
            winning_trades = (trades_df['pnl'] > 0).cumsum()
            total_trades = np.arange(1, len(trades_df) + 1)
            win_rate = winning_trades / total_trades
            ax5.plot(win_rate.index, win_rate.values, linewidth=2)
            ax5.set_title('Win Rate Over Time')
            ax5.grid(True, alpha=0.3)
        
        # Performance metrics table
        ax6 = fig.add_subplot(gs[2, :])
        ax6.axis('off')
        metrics = results['metrics']
        
        # Create text for metrics
        metrics_text = f"""
        Performance Summary:
        Total Return: {metrics.get('total_return', 0):.2%}
        Annualized Return: {metrics.get('annualized_return', 0):.2%}
        Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.3f}
        Max Drawdown: {metrics.get('max_drawdown', 0):.2%}
        Total Trades: {metrics.get('total_trades', 0)}
        Win Rate: {metrics.get('win_rate', 0):.2%}
        Final Value: ${metrics.get('final_value', 0):,.2f}
        """
        
        ax6.text(0.1, 0.5, metrics_text, fontsize=12, verticalalignment='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Dashboard saved to {save_path}")
        else:
            # Save to a default location if no path specified
            default_path = "backtest_dashboard.png"
            plt.savefig(default_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"Dashboard saved to {default_path}")
        
        plt.close()  # Close the plot to free memory
    
    def generate_analysis_report(self, results: Dict[str, Any]) -> str:
        """
        Generate a comprehensive analysis report with insights and suggestions.
        
        Args:
            results: Backtest results
            
        Returns:
            Formatted analysis report
        """
        metrics = results['metrics']
        trades = results['trades']
        
        report = []
        report.append("=" * 60)
        report.append("COMPREHENSIVE ANALYSIS & RECOMMENDATIONS")
        report.append("=" * 60)
        report.append("")
        
        # Performance Analysis
        report.append("📊 PERFORMANCE ANALYSIS")
        report.append("-" * 30)
        
        total_return = metrics.get('total_return', 0)
        annualized_return = metrics.get('annualized_return', 0)
        sharpe_ratio = metrics.get('sharpe_ratio', 0)
        max_drawdown = metrics.get('max_drawdown', 0)
        win_rate = metrics.get('win_rate', 0)
        total_trades = metrics.get('total_trades', 0)
        profit_factor = metrics.get('profit_factor', 0)
        
        # Return Analysis
        if total_return > 0.2:
            report.append("✅ EXCELLENT: Strategy generated strong positive returns")
        elif total_return > 0.1:
            report.append("✅ GOOD: Strategy performed well with solid returns")
        elif total_return > 0:
            report.append("⚠️  MODERATE: Strategy generated modest positive returns")
        else:
            report.append("❌ POOR: Strategy resulted in losses")
        
        # Risk Analysis
        report.append("")
        report.append("🎯 RISK ANALYSIS")
        report.append("-" * 20)
        
        if sharpe_ratio > 1.5:
            report.append("✅ EXCELLENT: High risk-adjusted returns (Sharpe > 1.5)")
        elif sharpe_ratio > 1.0:
            report.append("✅ GOOD: Solid risk-adjusted returns (Sharpe > 1.0)")
        elif sharpe_ratio > 0.5:
            report.append("⚠️  MODERATE: Acceptable risk-adjusted returns")
        else:
            report.append("❌ POOR: Low risk-adjusted returns")
        
        if abs(max_drawdown) < 0.1:
            report.append("✅ EXCELLENT: Very low maximum drawdown (< 10%)")
        elif abs(max_drawdown) < 0.2:
            report.append("✅ GOOD: Reasonable maximum drawdown (< 20%)")
        elif abs(max_drawdown) < 0.3:
            report.append("⚠️  MODERATE: High maximum drawdown (20-30%)")
        else:
            report.append("❌ HIGH RISK: Very high maximum drawdown (> 30%)")
        
        # Trading Analysis
        report.append("")
        report.append("📈 TRADING ANALYSIS")
        report.append("-" * 20)
        
        if total_trades > 50:
            report.append("✅ GOOD: Sufficient number of trades for statistical significance")
        elif total_trades > 20:
            report.append("⚠️  MODERATE: Limited number of trades - results may not be reliable")
        else:
            report.append("❌ LOW: Very few trades - results are not statistically significant")
        
        if win_rate > 0.6:
            report.append("✅ EXCELLENT: High win rate (> 60%)")
        elif win_rate > 0.5:
            report.append("✅ GOOD: Positive win rate (> 50%)")
        elif win_rate > 0.4:
            report.append("⚠️  MODERATE: Below-average win rate")
        else:
            report.append("❌ POOR: Low win rate (< 40%)")
        
        if profit_factor > 2.0:
            report.append("✅ EXCELLENT: High profit factor (> 2.0)")
        elif profit_factor > 1.5:
            report.append("✅ GOOD: Solid profit factor (> 1.5)")
        elif profit_factor > 1.0:
            report.append("⚠️  MODERATE: Positive profit factor")
        else:
            report.append("❌ POOR: Low profit factor")
        
        # Strategy Insights
        report.append("")
        report.append("🧠 STRATEGY INSIGHTS")
        report.append("-" * 20)
        
        # Analyze trade patterns
        if trades:
            avg_trade_pnl = metrics.get('avg_trade_pnl', 0)
            max_consecutive_losses = metrics.get('max_consecutive_losses', 0)
            max_consecutive_wins = metrics.get('max_consecutive_wins', 0)
            
            if avg_trade_pnl > 0:
                report.append("✅ Strategy generates positive average trade P&L")
            else:
                report.append("❌ Strategy generates negative average trade P&L")
            
            if max_consecutive_losses > 5:
                report.append("⚠️  Strategy can have long losing streaks - consider risk management")
            else:
                report.append("✅ Strategy has reasonable losing streaks")
            
            if max_consecutive_wins > 5:
                report.append("✅ Strategy can have good winning streaks")
        
        # Market Conditions Analysis
        report.append("")
        report.append("🌍 MARKET CONDITIONS ANALYSIS")
        report.append("-" * 30)
        
        # Analyze volatility and market conditions
        if 'volatility' in metrics:
            volatility = metrics['volatility']
            if volatility > 0.3:
                report.append("⚠️  High market volatility detected - strategy may be more risky")
            elif volatility > 0.2:
                report.append("✅ Moderate market volatility - typical trading conditions")
            else:
                report.append("✅ Low market volatility - stable trading conditions")
        
        # Recommendations
        report.append("")
        report.append("💡 RECOMMENDATIONS")
        report.append("-" * 15)
        
        recommendations = []
        
        # Performance-based recommendations
        if total_return < 0:
            recommendations.append("• Consider adjusting strategy parameters or testing different time periods")
            recommendations.append("• Review entry/exit criteria for potential improvements")
        
        if sharpe_ratio < 1.0:
            recommendations.append("• Focus on improving risk-adjusted returns through better position sizing")
            recommendations.append("• Consider adding stop-loss mechanisms")
        
        if abs(max_drawdown) > 0.2:
            recommendations.append("• Implement stricter risk management rules")
            recommendations.append("• Consider reducing position sizes to limit drawdown")
        
        if total_trades < 20:
            recommendations.append("• Test strategy over longer time periods for more reliable results")
            recommendations.append("• Consider adjusting signal frequency parameters")
        
        if win_rate < 0.5:
            recommendations.append("• Review signal generation logic for accuracy improvements")
            recommendations.append("• Consider adding filters to reduce false signals")
        
        # General recommendations
        recommendations.append("• Always use proper position sizing and risk management")
        recommendations.append("• Consider transaction costs and slippage in live trading")
        recommendations.append("• Test strategy across different market conditions")
        recommendations.append("• Monitor strategy performance regularly and adjust as needed")
        
        for rec in recommendations:
            report.append(rec)
        
        # Risk Warnings
        report.append("")
        report.append("⚠️  RISK WARNINGS")
        report.append("-" * 15)
        report.append("• Past performance does not guarantee future results")
        report.append("• Backtesting results may not reflect live trading conditions")
        report.append("• Consider market impact and liquidity constraints")
        report.append("• Always use proper risk management in live trading")
        report.append("• Diversify across multiple strategies and assets")
        
        # Summary
        report.append("")
        report.append("📋 SUMMARY")
        report.append("-" * 8)
        
        if total_return > 0.1 and sharpe_ratio > 1.0 and abs(max_drawdown) < 0.2:
            report.append("🎉 OVERALL ASSESSMENT: STRONG PERFORMANCE")
            report.append("   This strategy shows promising results with good risk-adjusted returns.")
        elif total_return > 0 and sharpe_ratio > 0.5:
            report.append("✅ OVERALL ASSESSMENT: ACCEPTABLE PERFORMANCE")
            report.append("   Strategy shows potential but may benefit from optimization.")
        else:
            report.append("❌ OVERALL ASSESSMENT: NEEDS IMPROVEMENT")
            report.append("   Strategy requires significant adjustments before live trading.")
        
        return "\n".join(report)
