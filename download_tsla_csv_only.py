#!/usr/bin/env python3
"""
Create realistic TSLA stock data as CSV (no API calls).
Python 3.8 compatible, generates high-quality synthetic data.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_realistic_tsla_data():
    """Create realistic TSLA-like data based on historical patterns."""
    print("📝 Creating realistic TSLA data...")
    
    # Create date range for the last 2 years (business days only)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Remove weekends
    dates = dates[dates.weekday < 5]
    
    print(f"📅 Generating data for {len(dates)} business days")
    print(f"   From: {start_date.strftime('%Y-%m-%d')}")
    print(f"   To: {end_date.strftime('%Y-%m-%d')}")
    
    # Generate realistic TSLA-like price data with actual patterns
    np.random.seed(42)  # For reproducible results
    
    # Start with realistic TSLA price from 2 years ago
    base_price = 150.0  # TSLA was around $150 in early 2022
    
    # Add some realistic trends and volatility
    prices = [base_price]
    trend = 0.0005  # Slight upward trend
    
    for i in range(1, len(dates)):
        # Add trend
        trend_change = trend
        
        # Add volatility (TSLA is quite volatile)
        volatility = np.random.normal(0, 0.03)  # 3% daily volatility
        
        # Add some market cycles
        cycle = 0.001 * np.sin(2 * np.pi * i / 252)  # Annual cycle
        
        # Combine all factors
        change = trend_change + volatility + cycle
        
        new_price = prices[-1] * (1 + change)
        
        # Ensure realistic bounds (TSLA has been between $100-$400 in recent years)
        new_price = max(new_price, 100)
        new_price = min(new_price, 400)
        
        prices.append(new_price)
    
    # Create OHLCV data with realistic relationships
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Calculate realistic OHLC from close price
        daily_volatility = close * 0.02  # 2% intraday volatility
        
        # High and low should bracket the close
        high = close + np.random.uniform(0, daily_volatility)
        low = close - np.random.uniform(0, daily_volatility)
        
        # Open should be close to previous close
        if i > 0:
            open_price = prices[i-1] + np.random.uniform(-daily_volatility/2, daily_volatility/2)
        else:
            open_price = close + np.random.uniform(-daily_volatility/2, daily_volatility/2)
        
        # Ensure OHLC relationships are correct
        high = max(high, open_price, close)
        low = min(low, open_price, close)
        
        # Realistic volume (TSLA trades 20M-100M shares per day)
        volume = np.random.randint(20000000, 100000000)
        
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
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    csv_path = "data/TSLA.csv"
    df.to_csv(csv_path)
    
    print(f"✅ Realistic TSLA data created: {csv_path}")
    print(f"   - Data points: {len(df)}")
    print(f"   - Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    print(f"   - Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    print(f"   - Final price: ${df['Close'].iloc[-1]:.2f}")
    
    return csv_path, df

def show_data_summary(df):
    """Show a summary of the generated data."""
    print(f"\n📊 Data Summary:")
    print(f"   - Total rows: {len(df)}")
    print(f"   - Columns: {list(df.columns)}")
    print(f"   - Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    
    print(f"\n💰 Price Statistics:")
    print(f"   - Open: ${df['Open'].mean():.2f} avg, ${df['Open'].min():.2f} min, ${df['Open'].max():.2f} max")
    print(f"   - High: ${df['High'].mean():.2f} avg, ${df['High'].min():.2f} min, ${df['High'].max():.2f} max")
    print(f"   - Low: ${df['Low'].mean():.2f} avg, ${df['Low'].min():.2f} min, ${df['Low'].max():.2f} max")
    print(f"   - Close: ${df['Close'].mean():.2f} avg, ${df['Close'].min():.2f} min, ${df['Close'].max():.2f} max")
    print(f"   - Volume: {df['Volume'].mean():,.0f} avg, {df['Volume'].min():,} min, {df['Volume'].max():,} max")
    
    print(f"\n📈 Sample Data (First 5 rows):")
    print(df.head().to_string())
    
    print(f"\n📉 Sample Data (Last 5 rows):")
    print(df.tail().to_string())

def main():
    """Main function."""
    print("🚀 TSLA Data Generator (CSV Only)")
    print("=" * 40)
    print("This script creates realistic TSLA stock data for backtesting.")
    print("No API calls or internet connection required.")
    print()
    
    # Create realistic TSLA data
    csv_path, df = create_realistic_tsla_data()
    
    if csv_path and df is not None:
        # Show data summary
        show_data_summary(df)
        
        print(f"\n🎯 Success! Your TSLA data is ready:")
        print(f"   📁 File: {csv_path}")
        print(f"   📊 Rows: {len(df)}")
        print(f"   💰 Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
        
        print(f"\n🚀 You can now use this data for backtesting:")
        print(f"   python3 main.py --strategy moving_average --data {csv_path} --initial-capital 10000")
        print(f"   python3 main.py --strategy rsi --data {csv_path} --initial-capital 10000")
        print(f"   python3 main.py --strategy macd --data {csv_path} --initial-capital 10000")
        
        print(f"\n💡 The data includes:")
        print(f"   - Realistic price movements based on TSLA's volatility")
        print(f"   - Proper OHLC relationships (High ≥ Open/Close ≥ Low)")
        print(f"   - Realistic volume patterns")
        print(f"   - Market cycles and trends")
        print(f"   - 2 years of business day data")
        
        return True
    else:
        print("❌ Failed to create TSLA data")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
