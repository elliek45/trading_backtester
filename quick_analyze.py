#!/usr/bin/env python3
"""
Quick Stock Analysis - Simple interactive script for analyzing any stock.
Just run this script and enter a stock ticker to get comprehensive analysis.
"""

import sys
import os
sys.path.append('.')

def main():
    """Quick stock analysis with interactive input."""
    print("🚀 Quick Stock Analysis")
    print("=" * 30)
    print("Enter a stock ticker to get comprehensive analysis with multiple strategies!")
    print()
    
    try:
        # Get stock ticker
        ticker = input("Stock ticker (e.g., AAPL, MSFT, TSLA): ").strip().upper()
        if not ticker:
            print("❌ No ticker provided. Exiting.")
            return False
        
        print(f"\n📊 Analyzing {ticker}...")
        
        # Import modules
        from backtester.engine import BacktestEngine
        from strategies.strategy_loader import StrategyLoader
        from analysis.visualizer import Visualizer
        from backtester.data_loader import DataLoader
        
        # Load data
        data_loader = DataLoader()
        data = data_loader.load_data(ticker, start_date="2020-01-01")
        print(f"✓ Loaded {len(data)} data points")
        
        # Initialize components
        engine = BacktestEngine(initial_capital=100000, commission=0.001)
        strategy_loader = StrategyLoader()
        visualizer = Visualizer()
        
        # Test strategies
        strategies = ['moving_average', 'rsi', 'macd']
        best_results = None
        best_strategy = None
        best_return = -float('inf')
        
        print(f"\n🔄 Testing strategies...")
        for strategy_name in strategies:
            print(f"  - {strategy_name}...")
            try:
                strategy = strategy_loader.load_strategy(strategy_name)
                results = engine.run_backtest(strategy, data=data)
                
                total_return = results['metrics']['total_return']
                if total_return > best_return:
                    best_return = total_return
                    best_results = results
                    best_strategy = strategy_name
                
                print(f"    ✓ Return: {total_return:.2%}")
            except Exception as e:
                print(f"    ❌ Failed: {e}")
        
        if best_results is None:
            print("❌ No strategies worked. Exiting.")
            return False
        
        print(f"\n🏆 Best strategy: {best_strategy} ({best_return:.2%})")
        
        # Generate analysis
        print(f"\n📊 Generating analysis...")
        analysis_report = visualizer.generate_analysis_report(best_results)
        
        # Display analysis
        print("\n" + "="*60)
        print(f"ANALYSIS FOR {ticker}")
        print("="*60)
        print(analysis_report)
        
        # Generate charts
        print(f"\n🎨 Creating charts...")
        visualizer.plot_portfolio_performance(best_results)
        visualizer.plot_drawdown(best_results)
        if best_results['trades']:
            visualizer.plot_trade_analysis(best_results)
        visualizer.create_dashboard(best_results)
        
        # Save report
        report_file = f"{ticker}_quick_analysis.txt"
        with open(report_file, 'w') as f:
            f.write(f"QUICK ANALYSIS REPORT\n")
            f.write(f"Ticker: {ticker}\n")
            f.write(f"Best Strategy: {best_strategy}\n")
            f.write("="*60 + "\n\n")
            f.write(analysis_report)
        
        print(f"\n✅ Analysis complete!")
        print(f"📁 Files saved:")
        print(f"  - {report_file}")
        print(f"  - portfolio_performance.png")
        print(f"  - drawdown_analysis.png")
        print(f"  - trade_analysis.png")
        print(f"  - backtest_dashboard.png")
        
        return True
        
    except KeyboardInterrupt:
        print(f"\n⏹️  Cancelled.")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
