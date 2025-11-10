#!/usr/bin/env python3

import os
from typing import List, Dict, Any, Optional
import pandas
from clients.doordash_snowflake_data_accessor_interface import DoorDashSnowflakeDataAccessorInterface

class MockDoorDashSnowflakeDataAccessor(DoorDashSnowflakeDataAccessorInterface):
    
    def __init__(self, 
                 account: Optional[str] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 warehouse: Optional[str] = None,
                 database: Optional[str] = None,
                 schema: Optional[str] = None):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


    def get_selection_data(self, store_id: int, limit: int = None) -> List[Dict[str, Any]]:
        # Read mock data from CSV file
        mock_data_dir_name = 'mock_data'
        mock_data_filename = f"mock_snowflake_response_store_{store_id}.csv"

        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                mock_data_dir_name, 
                                mock_data_filename)
        
        print(f"Reading mock data from: {csv_path}")
        df = pandas.read_csv(csv_path)
        df.columns = map(str.lower, df.columns)
        
        # Apply limit if specified
        if limit is not None and limit > 0:
            df = df.head(limit)
            print(f"Loaded {len(df)} rows from mock CSV (limited to {limit})")
        else:
            print(f"Loaded {len(df)} rows from mock CSV")
        
        return df

