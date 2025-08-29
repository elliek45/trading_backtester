#!/usr/bin/env python3
"""
Simple CSV-only test script for Python 3.8 compatibility.
Tests basic functionality with CSV files only.
"""

import sys
import os
sys.path.append('.')

def test_basic_imports():
    """Test basic package imports."""
    try:
        import pandas as pd
        import numpy as np
        print("✅ Basic packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Basic import error: {e}")
        return False

def test_csv_loading():
    """Test loading CSV data directly."""
    try:
        import pandas as pd
        
        # Test loading sample data directly
        data = pd.read_csv('data/sample_data.csv')
        print(f"✅ CSV loaded directly: {len(data)} rows, {len(data.columns)} columns")
        print(f"   Columns: {list(data.columns)}")
        print(f"   Date range: {data['Date'].min()} to {data['Date'].max()}")
        return True
    except Exception as e:
        print(f"❌ CSV loading error: {e}")
        return False

def test_data_loader_csv():
    """Test data loader with CSV files only."""
    try:
        from backtester.data_loader import DataLoader
        
        loader = DataLoader()
        print("✅ DataLoader imported successfully")
        
        # Test loading sample data
        data = loader.load_data('data/sample_data.csv')
        print(f"✅ Sample data loaded via DataLoader: {len(data)} rows")
        print(f"   Date range: {data.index.min()} to {data.index.max()}")
        return True
    except Exception as e:
        print(f"❌ DataLoader CSV error: {e}")
        return False

def test_strategy_loader():
    """Test strategy loader."""
    try:
        from strategies.strategy_loader import StrategyLoader
        
        loader = StrategyLoader()
        strategies = loader.list_strategies()
        print(f"✅ Found {len(strategies)} strategies: {strategies}")
        return True
    except Exception as e:
        print(f"❌ Strategy loader error: {e}")
        return False

def test_simple_backtest():
    """Test a simple backtest with CSV data."""
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
        
        print(f"✅ Backtest completed successfully")
        print(f"  - Total trades: {len(results['trades'])}")
        print(f"  - Final value: ${results['metrics']['final_value']:,.2f}")
        return True
    except Exception as e:
        print(f"❌ Backtest error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Trading Backtester (CSV Only - Python 3.8 Compatible)")
    print("=" * 60)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("CSV Loading", test_csv_loading),
        ("Data Loader CSV", test_data_loader_csv),
        ("Strategy Loader", test_strategy_loader),
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
    
    print(f"\n{'='*60}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The backtester is working correctly with CSV files.")
        print("\n🚀 You can now run:")
        print("  python3 main.py --strategy moving_average --data data/sample_data.csv --initial-capital 10000")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
