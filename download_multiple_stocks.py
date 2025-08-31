#!/usr/bin/env python3
"""
Create realistic stock data for multiple companies as CSV files.
Python 3.8 compatible, generates high-quality synthetic data for backtesting.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_stock_data(ticker, base_price, volatility, trend, start_date, end_date):
    """Create realistic stock data for a specific ticker."""
    print(f"📝 Creating realistic {ticker} data...")
    
    # Create date range for business days only
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = dates[dates.weekday < 5]  # Remove weekends
    
    print(f"📅 Generating data for {len(dates)} business days")
    print(f"   From: {start_date.strftime('%Y-%m-%d')}")
    print(f"   To: {end_date.strftime('%Y-%m-%d')}")
    
    # Generate realistic price data
    np.random.seed(42)  # For reproducible results
    
    prices = [base_price]
    
    for i in range(1, len(dates)):
        # Add trend
        trend_change = trend
        
        # Add volatility (different for each stock)
        daily_volatility = np.random.normal(0, volatility)
        
        # Add some market cycles
        cycle = 0.001 * np.sin(2 * np.pi * i / 252)  # Annual cycle
        
        # Add some company-specific patterns
        company_pattern = 0.0005 * np.sin(2 * np.pi * i / 63)  # Quarterly pattern
        
        # Combine all factors
        change = trend_change + daily_volatility + cycle + company_pattern
        
        new_price = prices[-1] * (1 + change)
        
        # Ensure realistic bounds based on stock characteristics
        if ticker == "AAPL":
            new_price = max(new_price, 100)  # AAPL has been above $100
            new_price = min(new_price, 300)
        elif ticker == "TSLA":
            new_price = max(new_price, 100)
            new_price = min(new_price, 400)
        elif ticker == "NVDA":
            new_price = max(new_price, 200)  # NVDA has been higher
            new_price = min(new_price, 800)
        elif ticker == "GOOG":
            new_price = max(new_price, 2000)  # GOOG has been higher
            new_price = min(new_price, 4000)
        elif ticker == "SBUX":
            new_price = max(new_price, 50)  # SBUX has been lower
            new_price = min(new_price, 150)
        
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
        
        # Realistic volume based on stock characteristics
        if ticker == "AAPL":
            volume = np.random.randint(50000000, 150000000)  # AAPL trades heavily
        elif ticker == "TSLA":
            volume = np.random.randint(20000000, 100000000)  # TSLA trades heavily
        elif ticker == "NVDA":
            volume = np.random.randint(30000000, 80000000)  # NVDA trades well
        elif ticker == "GOOG":
            volume = np.random.randint(15000000, 50000000)  # GOOG trades moderately
        elif ticker == "SBUX":
            volume = np.random.randint(8000000, 25000000)  # SBUX trades less
        
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
    
    csv_path = f"data/{ticker}.csv"
    df.to_csv(csv_path)
    
    print(f"✅ Realistic {ticker} data created: {csv_path}")
    print(f"   - Data points: {len(df)}")
    print(f"   - Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")
    print(f"   - Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
    print(f"   - Final price: ${df['Close'].iloc[-1]:.2f}")
    
    return csv_path, df

def show_data_summary(ticker, df):
    """Show a summary of the generated data."""
    print(f"\n📊 {ticker} Data Summary:")
    print(f"   - Total rows: {len(df)}")
    print(f"   - Columns: {list(df.columns)}")
    print(f"   - Date range: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}")

    print(f"\n💰 {ticker} Price Statistics:")
    print(f"   - Open: ${df['Open'].mean():.2f} avg, ${df['Open'].min():.2f} min, ${df['Open'].max():.2f} max")
    print(f"   - High: ${df['High'].mean():.2f} avg, ${df['High'].min():.2f} min, ${df['High'].max():.2f} max")
    print(f"   - Low: ${df['Low'].mean():.2f} avg, ${df['Low'].min():.2f} min, ${df['Low'].max():.2f} max")
    print(f"   - Close: ${df['Close'].mean():.2f} avg, ${df['Close'].min():.2f} min, ${df['Close'].max():.2f} max")
    print(f"   - Volume: {df['Volume'].mean():,.0f} avg, {df['Volume'].min():,} min, {df['Volume'].max():,} max")

    print(f"\n📈 {ticker} Sample Data (First 5 rows):")
    print(df.head().to_string())

    print(f"\n📉 {ticker} Sample Data (Last 5 rows):")
    print(df.tail().to_string())

def main():
    """Main function to create data for all stocks."""
    print("🚀 Multi-Stock Data Generator (CSV Only)")
    print("=" * 50)
    print("This script creates realistic stock data for multiple companies.")
    print("No API calls or internet connection required.")
    print()
    
    # Define stock characteristics
    stocks = [
        {
            "ticker": "AAPL",
            "base_price": 150.0,
            "volatility": 0.025,  # 2.5% daily volatility
            "trend": 0.0003,  # Slight upward trend
            "description": "Apple Inc. - Technology giant with steady growth"
        },
        {
            "ticker": "TSLA",
            "base_price": 200.0,
            "volatility": 0.04,  # 4% daily volatility (more volatile)
            "trend": 0.0008,  # Stronger upward trend
            "description": "Tesla Inc. - Electric vehicle leader with high volatility"
        },
        {
            "ticker": "NVDA",
            "base_price": 400.0,
            "volatility": 0.035,  # 3.5% daily volatility
            "trend": 0.0012,  # Very strong upward trend (AI boom)
            "description": "NVIDIA Corp. - AI chip leader with strong growth"
        },
        {
            "ticker": "GOOG",
            "base_price": 2800.0,
            "volatility": 0.02,  # 2% daily volatility (more stable)
            "trend": 0.0004,  # Moderate upward trend
            "description": "Alphabet Inc. - Tech giant with stable growth"
        },
        {
            "ticker": "SBUX",
            "base_price": 80.0,
            "volatility": 0.015,  # 1.5% daily volatility (most stable)
            "trend": 0.0001,  # Very slight upward trend
            "description": "Starbucks Corp. - Consumer staple with low volatility"
        }
    ]
    
    # Create date range for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    created_files = []
    
    for stock in stocks:
        print(f"\n{'='*60}")
        print(f"🎯 Creating data for {stock['ticker']}")
        print(f"📝 {stock['description']}")
        print(f"{'='*60}")
        
        try:
            csv_path, df = create_stock_data(
                stock['ticker'],
                stock['base_price'],
                stock['volatility'],
                stock['trend'],
                start_date,
                end_date
            )
            
            show_data_summary(stock['ticker'], df)
            created_files.append((stock['ticker'], csv_path, df))
            
        except Exception as e:
            print(f"❌ Error creating {stock['ticker']} data: {e}")
            continue
    
    # Summary
    print(f"\n{'='*60}")
    print("🎉 SUMMARY")
    print(f"{'='*60}")
    
    if created_files:
        print(f"✅ Successfully created {len(created_files)} stock datasets:")
        for ticker, csv_path, df in created_files:
            print(f"   📊 {ticker}: {csv_path}")
            print(f"      - {len(df)} data points")
            print(f"      - Price range: ${df['Close'].min():.2f} - ${df['Close'].max():.2f}")
            print(f"      - Final price: ${df['Close'].iloc[-1]:.2f}")
        
        print(f"\n🚀 You can now use these datasets for backtesting:")
        for ticker, _, _ in created_files:
            print(f"   python3 main.py --strategy moving_average --data data/{ticker}.csv --initial-capital 10000")
            print(f"   python3 main.py --strategy rsi --data data/{ticker}.csv --initial-capital 10000")
            print(f"   python3 main.py --strategy macd --data data/{ticker}.csv --initial-capital 10000")
        
        print(f"\n💡 Each stock has different characteristics:")
        for stock in stocks:
            if any(ticker == stock['ticker'] for ticker, _, _ in created_files):
                print(f"   • {stock['ticker']}: {stock['description']}")
                print(f"     - Volatility: {stock['volatility']*100:.1f}% daily")
                print(f"     - Trend: {stock['trend']*100:.2f}% daily")
        
        print(f"\n📈 Stock Characteristics:")
        print(f"   • AAPL: Stable tech giant with moderate volatility")
        print(f"   • TSLA: High-growth EV company with high volatility")
        print(f"   • NVDA: AI leader with strong growth and high volatility")
        print(f"   • GOOG: Stable tech giant with low volatility")
        print(f"   • SBUX: Consumer staple with very low volatility")
        
        return True
    else:
        print("❌ No datasets were created successfully")
        return False

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
