#!/usr/bin/env python3
"""
Minimal test script to isolate Python 3.8 compatibility issues.
"""

import sys
import os
sys.path.append('.')

def test_1_basic_packages():
    """Test basic package imports."""
    try:
        import pandas as pd
        import numpy as np
        print("✅ Basic packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Basic import error: {e}")
        return False

def test_2_csv_direct():
    """Test loading CSV directly."""
    try:
        import pandas as pd
        data = pd.read_csv('data/sample_data.csv')
        print(f"✅ CSV loaded directly: {len(data)} rows")
        return True
    except Exception as e:
        print(f"❌ CSV direct error: {e}")
        return False

def test_3_base_strategy():
    """Test base strategy import."""
    try:
        from strategies.base_strategy import BaseStrategy
        print("✅ BaseStrategy imported successfully")
        return True
    except Exception as e:
        print(f"❌ BaseStrategy error: {e}")
        return False

def test_4_strategy_loader():
    """Test strategy loader import."""
    try:
        from strategies.strategy_loader import StrategyLoader
        print("✅ StrategyLoader imported successfully")
        return True
    except Exception as e:
        print(f"❌ StrategyLoader error: {e}")
        return False

def test_5_data_loader():
    """Test data loader import."""
    try:
        from backtester.data_loader import DataLoader
        print("✅ DataLoader imported successfully")
        return True
    except Exception as e:
        print(f"❌ DataLoader error: {e}")
        return False

def test_6_engine():
    """Test engine import."""
    try:
        from backtester.engine import BacktestEngine
        print("✅ BacktestEngine imported successfully")
        return True
    except Exception as e:
        print(f"❌ BacktestEngine error: {e}")
        return False

def main():
    """Run minimal tests."""
    print("Minimal Python 3.8 Compatibility Test")
    print("=" * 40)
    
    tests = [
        ("Basic Packages", test_1_basic_packages),
        ("CSV Direct", test_2_csv_direct),
        ("Base Strategy", test_3_base_strategy),
        ("Strategy Loader", test_4_strategy_loader),
        ("Data Loader", test_5_data_loader),
        ("Engine", test_6_engine),
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
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
