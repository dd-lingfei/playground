#!/usr/bin/env python3

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import pandas
import snowflake.connector
from clients.doordash_snowflake_data_accessor_interface import DoorDashSnowflakeDataAccessorInterface

class DoorDashSnowflakeDataAccessor(DoorDashSnowflakeDataAccessorInterface):
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern - only one instance of DoorDashSnowflakeDataAccessor will be created"""
        if cls._instance is None:
            cls._instance = super(DoorDashSnowflakeDataAccessor, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, 
                 account: Optional[str] = "DOORDASH",
                 user: Optional[str] = "lingfei.li",
                 password: Optional[str] = None,
                 warehouse: Optional[str] = "ADHOC",
                 database: Optional[str] = "PRODDB",
                 schema: Optional[str] = 'LINGFEILI'):

        # Only initialize once
        if self._initialized:
            return

        self.conn = None
        self.cur = None
        
        # Connection parameters - prioritize environment variables, then constructor args
        self.account = account
        self.user = user or os.environ.get('SNOWFLAKE_USER')
        self.password = password or os.environ.get('SNOWFLAKE_PASSWORD')
        self.warehouse = warehouse
        self.database = database
        self.schema = schema
        if (self.user is None):
            raise ValueError("Snowflake user is missing")
        if (self.password is None):
            raise ValueError("Snowflake password is missing")
        self._initialized = True
        print(f"✓ DoorDashSnowflakeDataAccessor singleton initialized with user: {self.user}")

    def __enter__(self):
        try:            
            self.conn = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                password=self.password,
                # authenticator='externalbrowser',
                warehouse=self.warehouse,
                database=self.database,
                schema=self.schema
            )
            
            self.cur = self.conn.cursor()
            return self
            
        except Exception as e:
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        
        # Return False to propagate any exceptions
        return False

    def get_selection_data(self, store_id: int, limit: int = None) -> List[Dict[str, Any]]:
        limit_clause = f"LIMIT {limit}" if limit is not None else ""
        query = f"""
        SELECT
            rif.MERCHANT_SUPPLIED_ITEM_ID as MSID, 
            ctlg.UMP_ITEM_NAME as ITEM_NAME,
            ctlg.PHOTO_URL as PHOTO_URL,
            ctlg.SIZE as SIZE,
            rif.RAW_INVENTORY_CONTENT:price:unitAmount::NUMBER / 100.0 AS PRICE_USD
            FROM RETAIL_INVENTORY_SERVICE.PUBLIC.RAW_INVENTORY_FEED rif

            JOIN edw.cng.merchant_catalog_dlcopy ctlg
            ON rif.business_id = ctlg.business_id
            AND rif.MERCHANT_SUPPLIED_ITEM_ID = ctlg.item_merchant_supplied_id
            
            WHERE 1=1
            AND IS_ACTIVE=true
            AND rif.STORE_ID={store_id}
            
            {limit_clause}
        """
        
        print("Querying Snowflake...")        
        df = pandas.read_sql(query, self.conn)
        df.columns = map(str.lower, df.columns)
        return df
    

