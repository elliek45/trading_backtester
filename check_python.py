#!/usr/bin/env python3
"""
Check Python version and compatibility.
"""

import sys
import platform

def check_python():
    """Check Python version and compatibility."""
    print("🐍 Python Environment Check")
    print("=" * 30)
    
    # Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Platform: {platform.platform()}")
    
    # Check if we're using the right Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required!")
        return False
    elif sys.version_info >= (3, 9):
        print("✅ Python 3.9+ detected - should work with all features")
    else:
        print("⚠️  Python 3.8 detected - some features may have compatibility issues")
    
    # Check typing module
    try:
        from typing import Type, Dict, List, Any
        print("✅ typing module imported successfully")
        
        # Test type annotations
        test_dict: Dict[str, Any] = {"test": "value"}
        test_list: List[str] = ["test"]
        print("✅ Type annotations working")
        
    except Exception as e:
        print(f"❌ typing module error: {e}")
        return False
    
    # Check pandas
    try:
        import pandas as pd
        print(f"✅ pandas {pd.__version__} imported")
    except Exception as e:
        print(f"❌ pandas error: {e}")
        return False
    
    # Check numpy
    try:
        import numpy as np
        print(f"✅ numpy {np.__version__} imported")
    except Exception as e:
        print(f"❌ numpy error: {e}")
        return False
    
    print("\n🎯 Environment looks good!")
    return True

def test_simple_imports():
    """Test simple imports."""
    print("\n🔍 Testing simple imports...")
    
    try:
        # Test basic imports
        import pandas as pd
        import numpy as np
        
        # Test CSV loading
        data = pd.read_csv('data/sample_data.csv')
        print(f"✅ CSV loaded: {len(data)} rows")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple imports failed: {e}")
        return False

def main():
    """Main function."""
    if not check_python():
        return False
    
    if not test_simple_imports():
        return False
    
    print("\n🎉 All checks passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
