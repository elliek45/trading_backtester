"""
Strategy loader for managing and loading trading strategies.

This module provides a centralized way to load and manage different
trading strategies.
"""

import importlib
from typing import Dict, Any, List, Type
from .base_strategy import BaseStrategy
from .moving_average_strategy import MovingAverageStrategy
from .rsi_strategy import RSIStrategy
from .macd_strategy import MACDStrategy
import logging


class StrategyLoader:
    """
    Strategy loader for managing and loading trading strategies.
    
    This class provides a centralized interface for loading and
    instantiating different trading strategies.
    """
    
    def __init__(self):
        """Initialize the strategy loader."""
        self.logger = logging.getLogger(__name__)
        self._strategies = self._register_default_strategies()
    
    def _register_default_strategies(self) -> Dict[str, Type]:
        """
        Register default strategies.
        
        Returns:
            Dictionary mapping strategy names to strategy classes
        """
        return {
            'moving_average': MovingAverageStrategy,
            'rsi': RSIStrategy,
            'macd': MACDStrategy
        }
    
    def register_strategy(self, name: str, strategy_class: Type):
        """
        Register a new strategy.
        
        Args:
            name: Strategy name
            strategy_class: Strategy class
        """
        if not issubclass(strategy_class, BaseStrategy):
            raise ValueError("Strategy class must inherit from BaseStrategy")
        
        self._strategies[name] = strategy_class
        self.logger.info(f"Registered strategy: {name}")
    
    def load_strategy(self, name: str, parameters: Dict[str, Any] = None) -> BaseStrategy:
        """
        Load a strategy by name.
        
        Args:
            name: Strategy name
            parameters: Strategy parameters
            
        Returns:
            Strategy instance
        """
        if name not in self._strategies:
            available_strategies = list(self._strategies.keys())
            raise ValueError(f"Strategy '{name}' not found. Available strategies: {available_strategies}")
        
        strategy_class = self._strategies[name]
        strategy = strategy_class(parameters or {})
        
        # Validate parameters
        if not strategy.validate_parameters():
            raise ValueError(f"Invalid parameters for strategy '{name}'")
        
        self.logger.info(f"Loaded strategy: {name} with parameters: {parameters}")
        return strategy
    
    def list_strategies(self) -> List[str]:
        """
        List all available strategies.
        
        Returns:
            List of strategy names
        """
        return list(self._strategies.keys())
    
    def get_strategy_info(self, name: str) -> Dict[str, Any]:
        """
        Get information about a strategy.
        
        Args:
            name: Strategy name
            
        Returns:
            Dictionary with strategy information
        """
        if name not in self._strategies:
            raise ValueError(f"Strategy '{name}' not found")
        
        strategy_class = self._strategies[name]
        strategy = strategy_class()
        
        return {
            'name': name,
            'class': strategy_class.__name__,
            'description': strategy_class.__doc__,
            'parameters': strategy.get_parameter_summary()
        }
    
    def load_strategy_from_file(self, file_path: str, strategy_name: str, parameters: Dict[str, Any] = None) -> BaseStrategy:
        """
        Load a strategy from a Python file.
        
        Args:
            file_path: Path to the strategy file
            strategy_name: Name of the strategy class in the file
            parameters: Strategy parameters
            
        Returns:
            Strategy instance
        """
        try:
            # Import the module
            spec = importlib.util.spec_from_file_location("strategy_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Get the strategy class
            strategy_class = getattr(module, strategy_name)
            
            if not issubclass(strategy_class, BaseStrategy):
                raise ValueError(f"Class '{strategy_name}' must inherit from BaseStrategy")
            
            # Create strategy instance
            strategy = strategy_class(parameters or {})
            
            self.logger.info(f"Loaded strategy from file: {file_path}")
            return strategy
            
        except Exception as e:
            self.logger.error(f"Error loading strategy from file {file_path}: {e}")
            raise
