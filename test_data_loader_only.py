#!/usr/bin/env python3
"""
Test only the DataLoader import to isolate the type annotation issue.
"""

import sys
import os

def test_data_loader_import():
    """Test DataLoader import step by step."""
    print("🔍 Testing DataLoader import step by step...")
    print("=" * 50)
    
    # Add current directory to path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)
    
    # Test 1: Basic imports
    print("\n1. Testing basic imports...")
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
    
    # Test 2: Check pandas version
    print(f"\n2. Pandas version: {pd.__version__}")
    print(f"   Numpy version: {np.__version__}")
    
    # Test 3: Test typing imports
    print("\n3. Testing typing imports...")
    try:
        from typing import Optional, Union
        print("   ✅ typing imports successful")
    except Exception as e:
        print(f"   ❌ typing imports failed: {e}")
        return False
    
    # Test 4: Test pathlib
    print("\n4. Testing pathlib...")
    try:
        from pathlib import Path
        print("   ✅ pathlib imported")
    except Exception as e:
        print(f"   ❌ pathlib failed: {e}")
        return False
    
    # Test 5: Test logging
    print("\n5. Testing logging...")
    try:
        import logging
        print("   ✅ logging imported")
    except Exception as e:
        print(f"   ❌ logging failed: {e}")
        return False
    
    # Test 6: Test yfinance import (optional)
    print("\n6. Testing yfinance import...")
    try:
        import yfinance as yf
        print("   ✅ yfinance imported")
    except Exception as e:
        print(f"   ❌ yfinance failed: {e}")
        print("   (This is optional)")
    
    # Test 7: Try to import DataLoader
    print("\n7. Testing DataLoader import...")
    try:
        from backtester.data_loader import DataLoader
        print("   ✅ DataLoader imported successfully!")
        return True
    except Exception as e:
        print(f"   ❌ DataLoader import failed: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function."""
    print("DataLoader Import Test")
    print("=" * 30)
    
    success = test_data_loader_import()
    
    if success:
        print("\n🎉 DataLoader import successful!")
    else:
        print("\n❌ DataLoader import failed.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
