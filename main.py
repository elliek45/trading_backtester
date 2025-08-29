#!/usr/bin/env python3
"""
Trading Strategy Backtester - Main Entry Point

This module serves as the main entry point for the trading strategy backtester.
It provides a command-line interface to run backtests on different strategies
and analyze their performance.
"""

import argparse
import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backtester.engine import BacktestEngine
from backtester.data_loader import DataLoader
from strategies.strategy_loader import StrategyLoader
from analysis.performance_analyzer import PerformanceAnalyzer


def main():
    """Main entry point for the trading backtester."""
    parser = argparse.ArgumentParser(
        description="Trading Strategy Backtester",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --strategy moving_average --data data/AAPL.csv
  python main.py --strategy rsi --data data/SPY.csv --start-date 2020-01-01
  python main.py --list-strategies
        """
    )
    
    parser.add_argument(
        "--strategy", "-s",
        type=str,
        help="Name of the trading strategy to backtest"
    )
    
    parser.add_argument(
        "--data", "-d",
        type=str,
        help="Path to the historical data file (CSV format) or stock ticker symbol (e.g., AAPL)"
    )
    
    parser.add_argument(
        "--start-date",
        type=str,
        help="Start date for backtest (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--end-date",
        type=str,
        help="End date for backtest (YYYY-MM-DD)"
    )
    
    parser.add_argument(
        "--initial-capital",
        type=float,
        default=100000.0,
        help="Initial capital for backtest (default: 100000)"
    )
    
    parser.add_argument(
        "--commission",
        type=float,
        default=0.001,
        help="Commission rate per trade (default: 0.001)"
    )
    
    parser.add_argument(
        "--list-strategies",
        action="store_true",
        help="List all available strategies"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for results (JSON format)"
    )
    
    args = parser.parse_args()
    
    if args.list_strategies:
        strategy_loader = StrategyLoader()
        strategies = strategy_loader.list_strategies()
        print("Available strategies:")
        for strategy in strategies:
            print(f"  - {strategy}")
        return
    
    if not args.strategy or not args.data:
        parser.print_help()
        return
    
    try:
        # Initialize the backtest engine
        engine = BacktestEngine(
            initial_capital=args.initial_capital,
            commission=args.commission
        )
        
        # Load the strategy
        strategy_loader = StrategyLoader()
        strategy = strategy_loader.load_strategy(args.strategy)
        
        # Check if data is a stock ticker or file path
        is_ticker = not (args.data.endswith('.csv') or os.path.exists(args.data))
        
        if is_ticker:
            print(f"Running backtest for strategy: {args.strategy}")
            print(f"Stock ticker: {args.data}")
            print(f"Initial capital: ${args.initial_capital:,.2f}")
            print(f"Commission rate: {args.commission:.3f}")
            print("-" * 50)
            
            # Load data using ticker
            data_loader = DataLoader()
            data = data_loader.load_data(args.data, start_date=args.start_date, end_date=args.end_date)
            
            results = engine.run_backtest(
                strategy=strategy,
                data=data,
                start_date=args.start_date,
                end_date=args.end_date
            )
        else:
            print(f"Running backtest for strategy: {args.strategy}")
            print(f"Data file: {args.data}")
            print(f"Initial capital: ${args.initial_capital:,.2f}")
            print(f"Commission rate: {args.commission:.3f}")
            print("-" * 50)
            
            results = engine.run_backtest(
                strategy=strategy,
                data_file=args.data,
                start_date=args.start_date,
                end_date=args.end_date
            )
        
        # Analyze performance
        analyzer = PerformanceAnalyzer()
        analysis = analyzer.analyze(results)
        
        # Display results
        print("\n=== BACKTEST RESULTS ===")
        print(f"Total Return: {analysis['total_return']:.2%}")
        print(f"Annualized Return: {analysis['annualized_return']:.2%}")
        print(f"Sharpe Ratio: {analysis['sharpe_ratio']:.3f}")
        print(f"Max Drawdown: {analysis['max_drawdown']:.2%}")
        print(f"Total Trades: {analysis['total_trades']}")
        print(f"Win Rate: {analysis['win_rate']:.2%}")
        print(f"Final Portfolio Value: ${analysis['final_value']:,.2f}")
        
        # Generate visualizations
        print("\n=== GENERATING VISUALIZATIONS ===")
        from analysis.visualizer import Visualizer
        visualizer = Visualizer()
        
        # Create and save plots
        visualizer.plot_portfolio_performance(results)
        visualizer.plot_drawdown(results)
        if results['trades']:
            visualizer.plot_trade_analysis(results)
        visualizer.create_dashboard(results)
        
        print("Visualizations saved as PNG files in the current directory:")
        print("- portfolio_performance.png")
        print("- drawdown_analysis.png")
        print("- trade_analysis.png")
        print("- backtest_dashboard.png")
        
        # Generate comprehensive analysis report
        print("\n=== COMPREHENSIVE ANALYSIS ===")
        analysis_report = visualizer.generate_analysis_report(results)
        print(analysis_report)
        
        # Save analysis report to file
        analysis_file = "backtest_analysis_report.txt"
        with open(analysis_file, 'w') as f:
            f.write(analysis_report)
        print(f"\n📄 Analysis report saved to: {analysis_file}")
        
        # Save results if output file specified
        if args.output:
            import json
            with open(args.output, 'w') as f:
                json.dump(analysis, f, indent=2, default=str)
            print(f"\nResults saved to: {args.output}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
