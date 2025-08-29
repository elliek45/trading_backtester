#!/usr/bin/env python3
"""
Simple test script for Python 3.8 compatibility.
Tests basic functionality without problematic imports.
"""

import sys
import os
sys.path.append('.')

def test_basic_imports():
    """Test basic package imports."""
    try:
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        print("✅ Basic packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Basic import error: {e}")
        return False

def test_data_loader():
    """Test data loader without yfinance."""
    try:
        from backtester.data_loader import DataLoader
        loader = DataLoader()
        print("✅ DataLoader imported successfully")
        
        # Test loading sample data
        data = loader.load_data('data/sample_data.csv')
        print(f"✅ Sample data loaded: {len(data)} rows")
        return True
    except Exception as e:
        print(f"❌ DataLoader error: {e}")
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

def test_sample_data():
    """Test if sample data exists and can be read."""
    try:
        import pandas as pd
        data = pd.read_csv('data/sample_data.csv')
        print(f"✅ Sample data read: {len(data)} rows, {len(data.columns)} columns")
        print(f"   Columns: {list(data.columns)}")
        return True
    except Exception as e:
        print(f"❌ Sample data error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Trading Backtester (Python 3.8 Compatible)")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Sample Data", test_sample_data),
        ("Data Loader", test_data_loader),
        ("Strategy Loader", test_strategy_loader),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"  {test_name} failed!")
    
    print(f"\n{'='*50}")
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
