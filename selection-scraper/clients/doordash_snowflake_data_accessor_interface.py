#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import pandas


class DoorDashSnowflakeDataAccessorInterface(ABC):
    """
    Interface for DoorDash Snowflake Data Accessor.
    Defines the contract that all implementations must follow.
    """
    
    @abstractmethod
    def __enter__(self):
        """Context manager entry."""
        pass
    
    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        pass
    
    @abstractmethod
    def get_selection_data(self, store_id: int, limit: int = None) -> pandas.DataFrame:
        """
        Retrieve selection data for a given store from Snowflake.
        
        Args:
            store_id: The store ID to query
            limit: Optional limit on number of rows to return
            
        Returns:
            DataFrame containing selection data with columns:
            - msid: Merchant supplied item ID
            - item_name: Name of the item
            - photo_url: URL to item photo
            - size: Size information
            - price_usd: Price in USD
        """
        pass

