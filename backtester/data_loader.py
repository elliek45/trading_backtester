"""
Data loading and preprocessing for the backtesting engine.

This module handles loading historical data from various sources
and preprocessing it for use in backtesting.
"""

import pandas as pd
from typing import Optional, Union
from pathlib import Path
import logging

# Try to import yfinance, but make it optional for Python 3.8 compatibility
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    yf = None


class DataLoader:
    """
    Data loader for historical price data.
    
    This class handles loading data from:
    - CSV files
    - Yahoo Finance API (if available)
    - Other data sources
    """
    
    def __init__(self):
        """Initialize the data loader."""
        self.logger = logging.getLogger(__name__)
        if not YFINANCE_AVAILABLE:
            self.logger.warning("yfinance not available. Yahoo Finance data loading will be disabled.")
    
    def load_data(
        self,
        source: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load historical data from various sources.
        
        Args:
            source: Data source (file path or ticker symbol)
            start_date: Start date for data (YYYY-MM-DD)
            end_date: End date for data (YYYY-MM-DD)
            
        Returns:
            DataFrame with OHLCV data
        """
        if self._is_file_path(source):
            return self._load_from_file(source, start_date, end_date)
        else:
            if YFINANCE_AVAILABLE:
                return self._load_from_yahoo(source, start_date, end_date)
            else:
                raise ImportError("yfinance not available. Please install it with: pip install yfinance")
    
    def _is_file_path(self, source: str) -> bool:
        """Check if source is a file path."""
        return Path(source).exists() or source.endswith('.csv')
    
    def _load_from_file(
        self,
        file_path: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load data from CSV file.
        
        Args:
            file_path: Path to CSV file
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            # Load CSV file
            df = pd.read_csv(file_path)
            
            # Ensure required columns exist
            required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValueError(f"Missing required columns: {missing_columns}")
            
            # Convert date column
            df['Date'] = pd.to_datetime(df['Date'])
            df.set_index('Date', inplace=True)
            
            # Sort by date
            df.sort_index(inplace=True)
            
            # Filter by date range if specified
            if start_date:
                df = df[df.index >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
            
            self.logger.info(f"Loaded {len(df)} data points from {file_path}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data from {file_path}: {e}")
            raise
    
    def _load_from_yahoo(
        self,
        ticker: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load data from Yahoo Finance.
        
        Args:
            ticker: Stock ticker symbol
            start_date: Start date for data
            end_date: End date for data
            
        Returns:
            DataFrame with OHLCV data
        """
        if not YFINANCE_AVAILABLE:
            raise ImportError("yfinance not available. Please install it with: pip install yfinance")
            
        try:
            # Download data from Yahoo Finance
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            # Rename columns to match expected format
            df.columns = [col.title() for col in df.columns]
            
            self.logger.info(f"Loaded {len(df)} data points for {ticker}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error loading data for {ticker}: {e}")
            raise
    
    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Validate that the data meets requirements.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if data is valid, False otherwise
        """
        # Check required columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in df.columns for col in required_columns):
            return False
        
        # Check for missing values
        if df[required_columns].isnull().any().any():
            return False
        
        # Check for negative prices
        price_columns = ['Open', 'High', 'Low', 'Close']
        if (df[price_columns] <= 0).any().any():
            return False
        
        # Check for negative volume
        if (df['Volume'] < 0).any():
            return False
        
        return True
    
    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess the data for backtesting.
        
        Args:
            df: Raw data DataFrame
            
        Returns:
            Preprocessed DataFrame
        """
        # Remove any rows with missing values
        df = df.dropna()
        
        # Ensure data is sorted by date
        df.sort_index(inplace=True)
        
        # Add technical indicators if needed
        df = self._add_technical_indicators(df)
        
        return df
    
    def _add_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add common technical indicators to the data.
        
        Args:
            df: Price data DataFrame
            
        Returns:
            DataFrame with technical indicators
        """
        # Simple Moving Averages
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        
        # Exponential Moving Averages
        df['EMA_12'] = df['Close'].ewm(span=12).mean()
        df['EMA_26'] = df['Close'].ewm(span=26).mean()
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
        
        return df
    
    def save_data(self, df: pd.DataFrame, file_path: str):
        """
        Save data to CSV file.
        
        Args:
            df: DataFrame to save
            file_path: Output file path
        """
        try:
            df.to_csv(file_path)
            self.logger.info(f"Data saved to {file_path}")
        except Exception as e:
            self.logger.error(f"Error saving data to {file_path}: {e}")
            raise
