#!/usr/bin/env python3
"""
Demo script to generate and save trading backtester graphs automatically.
This script runs a backtest and saves all visualizations as PNG files.
"""

import sys
import os
sys.path.append('.')

def main():
    """Run a demo backtest and generate all visualizations."""
    print("🚀 Trading Backtester - Graph Demo")
    print("=" * 50)
    
    try:
        # Import required modules
        from backtester.engine import BacktestEngine
        from strategies.strategy_loader import StrategyLoader
        from analysis.performance_analyzer import PerformanceAnalyzer
        from analysis.visualizer import Visualizer
        from backtester.data_loader import DataLoader
        
        print("✓ Modules imported successfully")
        
        # Load sample data
        print("\n📊 Loading sample data...")
        data_loader = DataLoader()
        data = data_loader.load_data('data/sample_data.csv')
        print(f"✓ Loaded {len(data)} data points")
        
        # Initialize backtest engine
        print("\n⚙️  Initializing backtest engine...")
        engine = BacktestEngine(initial_capital=100000, commission=0.001)
        
        # Load strategy
        print("\n📈 Loading Moving Average strategy...")
        strategy_loader = StrategyLoader()
        strategy = strategy_loader.load_strategy('moving_average', {
            'fast_period': 5,
            'slow_period': 10,
            'ma_type': 'sma'
        })
        
        # Run backtest
        print("\n🔄 Running backtest...")
        results = engine.run_backtest(strategy, data)
        print("✓ Backtest completed successfully")
        
        # Analyze results
        print("\n📊 Analyzing results...")
        analyzer = PerformanceAnalyzer()
        analysis = analyzer.analyze(results)
        
        # Display key metrics
        print("\n=== BACKTEST RESULTS ===")
        print(f"Total Return: {analysis['total_return']:.2%}")
        print(f"Annualized Return: {analysis['annualized_return']:.2%}")
        print(f"Sharpe Ratio: {analysis['sharpe_ratio']:.3f}")
        print(f"Max Drawdown: {analysis['max_drawdown']:.2%}")
        print(f"Total Trades: {analysis['total_trades']}")
        print(f"Win Rate: {analysis['win_rate']:.2%}")
        print(f"Final Portfolio Value: ${analysis['final_value']:,.2f}")
        
        # Generate visualizations
        print("\n🎨 Generating visualizations...")
        visualizer = Visualizer()
        
        # Create all plots
        print("  - Portfolio performance plot...")
        visualizer.plot_portfolio_performance(results)
        
        print("  - Drawdown analysis...")
        visualizer.plot_drawdown(results)
        
        if results['trades']:
            print("  - Trade analysis...")
            visualizer.plot_trade_analysis(results)
        
        print("  - Comprehensive dashboard...")
        visualizer.create_dashboard(results)
        
        print("\n✅ All visualizations generated successfully!")
        print("\n📁 Generated files:")
        print("  - portfolio_performance.png")
        print("  - drawdown_analysis.png")
        print("  - trade_analysis.png")
        print("  - backtest_dashboard.png")
        
        print("\n🎯 You can now view these PNG files directly without any hovering!")
        print("   Open them in your file browser or image viewer.")
        
        # Generate comprehensive analysis report
        print("\n=== COMPREHENSIVE ANALYSIS ===")
        analysis_report = visualizer.generate_analysis_report(results)
        print(analysis_report)
        
        # Save analysis report to file
        analysis_file = "backtest_analysis_report.txt"
        with open(analysis_file, 'w') as f:
            f.write(analysis_report)
        print(f"\n📄 Analysis report saved to: {analysis_file}")
        
        print("\n📊 SUMMARY OF GENERATED FILES:")
        print("  📈 PNG Charts:")
        print("    - portfolio_performance.png")
        print("    - drawdown_analysis.png")
        print("    - trade_analysis.png")
        print("    - backtest_dashboard.png")
        print("  📄 Text Report:")
        print("    - backtest_analysis_report.txt")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Demo completed successfully!")
    else:
        print("\n💥 Demo failed. Please check the error messages above.")
        sys.exit(1)
