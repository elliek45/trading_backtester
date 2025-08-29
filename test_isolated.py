#!/usr/bin/env python3
"""
Isolated test to find the exact source of type annotation errors.
"""

import sys
import os

def test_isolated():
    """Test each import in isolation."""
    print("🔍 Testing imports in isolation...")
    print("=" * 40)
    
    # Test 1: Basic packages
    print("\n1. Testing basic packages...")
    try:
        import pandas as pd
        print("   ✅ pandas imported")
    except Exception as e:
        print(f"   ❌ pandas failed: {e}")
        return False
    
    try:
        import numpy as np
        print("   ✅ numpy imported")
    except Exception as e:
        print(f"   ❌ numpy failed: {e}")
        return False
    
    # Test 2: CSV loading
    print("\n2. Testing CSV loading...")
    try:
        data = pd.read_csv('data/sample_data.csv')
        print(f"   ✅ CSV loaded: {len(data)} rows")
    except Exception as e:
        print(f"   ❌ CSV failed: {e}")
        return False
    
    # Test 3: Base strategy (with proper path)
    print("\n3. Testing base strategy...")
    try:
        # Add the current directory to path for absolute imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        
        from strategies.base_strategy import BaseStrategy
        print("   ✅ BaseStrategy imported")
    except Exception as e:
        print(f"   ❌ BaseStrategy failed: {e}")
        return False
    
    # Test 4: Strategy loader (with proper path)
    print("\n4. Testing strategy loader...")
    try:
        from strategies.strategy_loader import StrategyLoader
        print("   ✅ StrategyLoader imported")
    except Exception as e:
        print(f"   ❌ StrategyLoader failed: {e}")
        return False
    
    # Test 5: Data loader (with proper path)
    print("\n5. Testing data loader...")
    try:
        from backtester.data_loader import DataLoader
        print("   ✅ DataLoader imported")
    except Exception as e:
        print(f"   ❌ DataLoader failed: {e}")
        return False
    
    # Test 6: Engine (with proper path)
    print("\n6. Testing engine...")
    try:
        from backtester.engine import BacktestEngine
        print("   ✅ BacktestEngine imported")
    except Exception as e:
        print(f"   ❌ BacktestEngine failed: {e}")
        return False
    
    print("\n🎉 All isolated imports successful!")
    return True

def test_simple_backtest():
    """Test a simple backtest with isolated components."""
    print("\n🚀 Testing simple backtest...")
    
    try:
        # Import components with proper paths
        from strategies.base_strategy import BaseStrategy
        from strategies.strategy_loader import StrategyLoader
        from backtester.data_loader import DataLoader
        from backtester.engine import BacktestEngine
        
        # Load data
        data_loader = DataLoader()
        data = data_loader.load_data('data/sample_data.csv')
        print(f"   ✅ Data loaded: {len(data)} rows")
        
        # Load strategy
        strategy_loader = StrategyLoader()
        strategy = strategy_loader.load_strategy('moving_average')
        print(f"   ✅ Strategy loaded: {strategy.name}")
        
        # Run backtest
        engine = BacktestEngine(initial_capital=10000, commission=0.001)
        results = engine.run_backtest(strategy, data=data)
        print(f"   ✅ Backtest completed: {len(results['trades'])} trades")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Backtest failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run isolated tests."""
    print("Isolated Python 3.8 Compatibility Test")
    print("=" * 50)
    
    # Test isolated imports
    if not test_isolated():
        print("\n❌ Isolated imports failed. Stopping here.")
        return False
    
    # Test simple backtest
    if not test_simple_backtest():
        print("\n❌ Simple backtest failed.")
        return False
    
    print("\n🎉 All tests passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
