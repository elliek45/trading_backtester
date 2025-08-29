#!/usr/bin/env python3
"""
Stock Analysis Script - Analyze any stock with automatic backtesting and analysis.
This script allows users to input a stock ticker and automatically runs backtests
with multiple strategies to provide comprehensive analysis.
"""

import sys
import os
sys.path.append('.')

def main():
    """Analyze a stock with automatic backtesting and comprehensive analysis."""
    print("📈 Stock Analysis with Trading Backtester")
    print("=" * 50)
    
    try:
        # Get stock ticker from user
        ticker = input("Enter stock ticker (e.g., AAPL, MSFT, TSLA): ").strip().upper()
        if not ticker:
            print("❌ No ticker provided. Exiting.")
            return False
        
        # Get date range
        print("\n📅 Date Range (optional - press Enter for defaults):")
        start_date = input("Start date (YYYY-MM-DD, default: 2020-01-01): ").strip()
        end_date = input("End date (YYYY-MM-DD, default: today): ").strip()
        
        if not start_date:
            start_date = "2020-01-01"
        if not end_date:
            end_date = None
        
        # Get initial capital
        capital_input = input("Initial capital (default: $100,000): ").strip()
        initial_capital = float(capital_input) if capital_input else 100000.0
        
        print(f"\n🚀 Analyzing {ticker} from {start_date} to {end_date or 'today'}")
        print(f"💰 Initial capital: ${initial_capital:,.2f}")
        
        # Import required modules
        from backtester.engine import BacktestEngine
        from strategies.strategy_loader import StrategyLoader
        from analysis.performance_analyzer import PerformanceAnalyzer
        from analysis.visualizer import Visualizer
        from backtester.data_loader import DataLoader
        
        print("\n📊 Loading stock data...")
        data_loader = DataLoader()
        data = data_loader.load_data(ticker, start_date=start_date, end_date=end_date)
        print(f"✓ Loaded {len(data)} data points for {ticker}")
        
        # Initialize components
        engine = BacktestEngine(initial_capital=initial_capital, commission=0.001)
        strategy_loader = StrategyLoader()
        analyzer = PerformanceAnalyzer()
        visualizer = Visualizer()
        
        # Test multiple strategies
        strategies_to_test = [
            ('moving_average', {'fast_period': 20, 'slow_period': 50}),
            ('rsi', {'period': 14, 'oversold': 30, 'overbought': 70}),
            ('macd', {'fast_period': 12, 'slow_period': 26, 'signal_period': 9})
        ]
        
        results_list = []
        strategy_names = []
        
        print(f"\n🔄 Testing {len(strategies_to_test)} strategies...")
        
        for strategy_name, params in strategies_to_test:
            print(f"  - Testing {strategy_name} strategy...")
            try:
                strategy = strategy_loader.load_strategy(strategy_name, params)
                results = engine.run_backtest(strategy, data)
                results_list.append(results)
                strategy_names.append(f"{strategy_name}_{params}")
                print(f"    ✓ Completed with {len(results['trades'])} trades")
            except Exception as e:
                print(f"    ❌ Failed: {e}")
                continue
        
        if not results_list:
            print("❌ No strategies completed successfully. Exiting.")
            return False
        
        # Find best performing strategy
        best_idx = 0
        best_return = -float('inf')
        
        for i, results in enumerate(results_list):
            metrics = results['metrics']
            total_return = metrics.get('total_return', -float('inf'))
            if total_return > best_return:
                best_return = total_return
                best_idx = i
        
        best_strategy_name = strategy_names[best_idx]
        best_results = results_list[best_idx]
        
        print(f"\n🏆 Best performing strategy: {best_strategy_name}")
        print(f"   Total Return: {best_return:.2%}")
        
        # Generate comprehensive analysis for best strategy
        print(f"\n📊 Generating comprehensive analysis...")
        analysis_report = visualizer.generate_analysis_report(best_results)
        
        # Display analysis
        print("\n" + "="*60)
        print(f"ANALYSIS FOR {ticker} - {best_strategy_name.upper()}")
        print("="*60)
        print(analysis_report)
        
        # Generate visualizations
        print(f"\n🎨 Generating visualizations...")
        visualizer.plot_portfolio_performance(best_results)
        visualizer.plot_drawdown(best_results)
        if best_results['trades']:
            visualizer.plot_trade_analysis(best_results)
        visualizer.create_dashboard(best_results)
        
        # Save analysis report
        analysis_file = f"{ticker}_analysis_report.txt"
        with open(analysis_file, 'w') as f:
            f.write(f"STOCK ANALYSIS REPORT\n")
            f.write(f"Ticker: {ticker}\n")
            f.write(f"Date Range: {start_date} to {end_date or 'today'}\n")
            f.write(f"Initial Capital: ${initial_capital:,.2f}\n")
            f.write(f"Best Strategy: {best_strategy_name}\n")
            f.write("="*60 + "\n\n")
            f.write(analysis_report)
        
        # Strategy comparison
        if len(results_list) > 1:
            print(f"\n📊 STRATEGY COMPARISON")
            print("-" * 30)
            comparison_data = []
            
            for i, results in enumerate(results_list):
                metrics = results['metrics']
                comparison_data.append({
                    'Strategy': strategy_names[i],
                    'Total Return': f"{metrics.get('total_return', 0):.2%}",
                    'Sharpe Ratio': f"{metrics.get('sharpe_ratio', 0):.3f}",
                    'Max Drawdown': f"{metrics.get('max_drawdown', 0):.2%}",
                    'Win Rate': f"{metrics.get('win_rate', 0):.2%}",
                    'Total Trades': metrics.get('total_trades', 0)
                })
            
            # Display comparison table
            print(f"{'Strategy':<25} {'Return':<10} {'Sharpe':<8} {'Drawdown':<10} {'Win Rate':<10} {'Trades':<8}")
            print("-" * 80)
            for data in comparison_data:
                print(f"{data['Strategy']:<25} {data['Total Return']:<10} {data['Sharpe Ratio']:<8} "
                      f"{data['Max Drawdown']:<10} {data['Win Rate']:<10} {data['Total Trades']:<8}")
        
        # Save results
        results_file = f"{ticker}_backtest_results.json"
        import json
        with open(results_file, 'w') as f:
            # Convert results to serializable format
            serializable_results = {
                'ticker': ticker,
                'date_range': f"{start_date} to {end_date or 'today'}",
                'initial_capital': initial_capital,
                'best_strategy': best_strategy_name,
                'results': best_results
            }
            json.dump(serializable_results, f, indent=2, default=str)
        
        print(f"\n✅ Analysis completed successfully!")
        print(f"\n📁 Generated files:")
        print(f"  📈 Charts:")
        print(f"    - portfolio_performance.png")
        print(f"    - drawdown_analysis.png")
        print(f"    - trade_analysis.png")
        print(f"    - backtest_dashboard.png")
        print(f"  📄 Reports:")
        print(f"    - {analysis_file}")
        print(f"    - {results_file}")
        
        print(f"\n🎯 Key Insights for {ticker}:")
        metrics = best_results['metrics']
        print(f"  • Best Strategy: {best_strategy_name}")
        print(f"  • Total Return: {metrics.get('total_return', 0):.2%}")
        print(f"  • Risk-Adjusted Return: {metrics.get('sharpe_ratio', 0):.3f}")
        print(f"  • Maximum Drawdown: {metrics.get('max_drawdown', 0):.2%}")
        print(f"  • Win Rate: {metrics.get('win_rate', 0):.2%}")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n\n⏹️  Analysis cancelled by user.")
        return False
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
