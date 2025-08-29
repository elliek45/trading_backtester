#!/usr/bin/env python3
"""
Download TSLA data and save as CSV for local testing.
"""

import sys
import os
sys.path.append('.')

def download_tsla_csv():
    """Download TSLA data and save as CSV."""
    try:
        import yfinance as yf
        import pandas as pd
        from datetime import datetime, timedelta
        
        print("📈 Downloading TSLA data...")
        
        # Download TSLA data for the last 2 years
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        
        tsla = yf.Ticker("TSLA")
        data = tsla.history(start=start_date, end=end_date)
        
        if data.empty:
            print("❌ No data downloaded. Trying alternative approach...")
            # Try downloading without date restrictions
            data = tsla.history(period="2y")
        
        if not data.empty:
            # Save to CSV
            csv_path = "data/TSLA.csv"
            data.to_csv(csv_path)
            print(f"✅ TSLA data saved to {csv_path}")
            print(f"   Data points: {len(data)}")
            print(f"   Date range: {data.index.min().date()} to {data.index.max().date()}")
            return csv_path
        else:
            print("❌ Failed to download TSLA data")
            return None
            
    except Exception as e:
        print(f"❌ Error downloading TSLA data: {e}")
        return None

def create_sample_tsla_csv():
    """Create a sample TSLA CSV with synthetic data for testing."""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    print("�� Creating sample TSLA data for testing...")
    
    # Create date range for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Remove weekends (simple approach)
    dates = dates[dates.weekday < 5]
    
    # Generate realistic TSLA-like price data
    np.random.seed(42)  # For reproducible results
    
    # Start with a realistic price
    base_price = 200.0
    prices = [base_price]
    
    for i in range(1, len(dates)):
        # Add some random walk with trend
        change = np.random.normal(0, 0.02)  # 2% daily volatility
        if i % 30 == 0:  # Add some trend changes monthly
            change += np.random.normal(0, 0.05)
        
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 50))  # Don't go below $50
    
    # Create OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC from close price
        volatility = close * 0.02
        high = close + np.random.uniform(0, volatility)
        low = close - np.random.uniform(0, volatility)
        open_price = close + np.random.uniform(-volatility/2, volatility/2)
        volume = np.random.randint(10000000, 100000000)  # 10M to 100M shares
        
        data.append({
            'Date': date.strftime('%Y-%m-%d'),
            'Open': round(open_price, 2),
            'High': round(high, 2),
            'Low': round(low, 2),
            'Close': round(close, 2),
            'Volume': volume
        })
    
    # Create DataFrame and save
    df = pd.DataFrame(data)
    csv_path = "data/TSLA_sample.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"✅ Sample TSLA data created: {csv_path}")
    print(f"   Data points: {len(df)}")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"   Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    
    return csv_path

def main():
    """Main function to download or create TSLA data."""
    print("�� TSLA Data Setup")
    print("=" * 30)
    
    # First try to download real data
    csv_path = download_tsla_csv()
    
    if not csv_path:
        print("\n📝 Creating sample data instead...")
        csv_path = create_sample_tsla_csv()
    
    if csv_path:
        print(f"\n🎯 Now you can test with: python3 main.py --strategy moving_average --data {csv_path} --initial-capital 10000")
    
    return csv_path is not None

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)