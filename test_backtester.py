#!/usr/bin/env python3
"""
Simple test script to verify the trading backtester works correctly.
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test that all modules can be imported."""
    try:
        from backtester.engine import BacktestEngine
        from strategies.strategy_loader import StrategyLoader
        from analysis.performance_analyzer import PerformanceAnalyzer
        from analysis.visualizer import Visualizer
        print("✓ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_strategy_loader():
    """Test strategy loader functionality."""
    try:
        loader = StrategyLoader()
        strategies = loader.list_strategies()
        print(f"✓ Found {len(strategies)} strategies: {strategies}")
        
        # Test loading a strategy
        strategy = loader.load_strategy('moving_average')
        print(f"✓ Successfully loaded {strategy.name} strategy")
        return True
    except Exception as e:
        print(f"✗ Strategy loader error: {e}")
        return False

def test_data_loader():
    """Test data loader functionality."""
    try:
        from backtester.data_loader import DataLoader
        loader = DataLoader()
        
        # Test loading sample data
        data = loader.load_data('data/sample_data.csv')
        print(f"✓ Loaded {len(data)} data points from sample file")
        return True
    except Exception as e:
        print(f"✗ Data loader error: {e}")
        return False

def test_simple_backtest():
    """Test a simple backtest."""
    try:
        from backtester.engine import BacktestEngine
        from strategies.strategy_loader import StrategyLoader
        from backtester.data_loader import DataLoader
        
        # Load data
        data_loader = DataLoader()
        data = data_loader.load_data('data/sample_data.csv')
        
        # Load strategy
        strategy_loader = StrategyLoader()
        strategy = strategy_loader.load_strategy('moving_average')
        
        # Run backtest
        engine = BacktestEngine(initial_capital=10000, commission=0.001)
        results = engine.run_backtest(strategy, data=data)
        
        print(f"✓ Backtest completed successfully")
        print(f"  - Total trades: {len(results['trades'])}")
        print(f"  - Final value: ${results['metrics']['final_value']:,.2f}")
        return True
    except Exception as e:
        print(f"✗ Backtest error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Trading Backtester Framework")
    print("=" * 40)
    
    tests = [
        ("Module Imports", test_imports),
        ("Strategy Loader", test_strategy_loader),
        ("Data Loader", test_data_loader),
        ("Simple Backtest", test_simple_backtest),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} failed!")
    
    print(f"\n{'='*40}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The backtester is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
