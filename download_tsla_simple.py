#!/usr/bin/env python3
"""
Simple script to download TSLA stock data from Yahoo Finance.
Clean, minimal dependencies, should work with Python 3.8+.
"""

import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import os

def download_tsla_data():
    """Download TSLA stock data and save as CSV."""
    print("📈 Downloading TSLA Stock Data")
    print("=" * 40)
    
    try:
        # Set date range (last 2 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        
        print(f"📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Download TSLA data
        print("🔄 Downloading data from Yahoo Finance...")
        tsla = yf.Ticker("TSLA")
        data = tsla.history(start=start_date, end=end_date)
        
        if data.empty:
            print("⚠️  No data with date range, trying without dates...")
            data = tsla.history(period="2y")
        
        if data.empty:
            print("❌ Failed to download TSLA data")
            return None
        
        print(f"✅ Downloaded {len(data)} data points")
        
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Save to CSV
        csv_path = "data/TSLA.csv"
        data.to_csv(csv_path)
        
        print(f"💾 Data saved to: {csv_path}")
        print(f"📊 Data summary:")
        print(f"   - Rows: {len(data)}")
        print(f"   - Columns: {list(data.columns)}")
        print(f"   - Date range: {data.index.min().strftime('%Y-%m-%d')} to {data.index.max().strftime('%Y-%m-%d')}")
        print(f"   - Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
        
        return csv_path
        
    except Exception as e:
        print(f"❌ Error downloading data: {e}")
        return None

def create_sample_data():
    """Create sample data if download fails."""
    print("\n📝 Creating sample TSLA data...")
    
    # Create date range for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Remove weekends
    dates = dates[dates.weekday < 5]
    
    # Generate realistic TSLA-like price data
    import numpy as np
    np.random.seed(42)  # For reproducible results
    
    # Start with realistic price and add some volatility
    base_price = 200.0
    prices = [base_price]
    
    for i in range(1, len(dates)):
        # Add random walk with some trend
        change = np.random.normal(0, 0.02)  # 2% daily volatility
        if i % 30 == 0:  # Monthly trend changes
            change += np.random.normal(0, 0.05)
        
        new_price = prices[-1] * (1 + change)
        prices.append(max(new_price, 50))  # Don't go below $50
    
    # Create OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        volatility = close * 0.02
        high = close + np.random.uniform(0, volatility)
        low = close - np.random.uniform(0, volatility)
        open_price = close + np.random.uniform(-volatility/2, volatility/2)
        volume = np.random.randint(10000000, 100000000)
        
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
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    csv_path = "data/TSLA_sample.csv"
    df.to_csv(csv_path)
    
    print(f"✅ Sample data created: {csv_path}")
    print(f"   - Data points: {len(df)}")
    print(f"   - Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    
    return csv_path

def main():
    """Main function."""
    print("🚀 TSLA Data Downloader")
    print("=" * 30)
    
    # Try to download real data first
    csv_path = download_tsla_data()
    
    if not csv_path:
        print("\n📝 Download failed, creating sample data instead...")
        csv_path = create_sample_data()
    
    if csv_path:
        print(f"\n🎯 Success! You can now use this data:")
        print(f"   File: {csv_path}")
        print(f"   Test with: python3 main.py --strategy moving_average --data {csv_path} --initial-capital 10000")
    
    return csv_path is not None

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
