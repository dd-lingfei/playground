#!/usr/bin/env python3
"""
Snowflake Client - Database Connection and Query Execution
========================================================

This module provides a Snowflake client for connecting to and querying
Snowflake databases with SSO authentication and proper connection management.
"""

import os
import sys
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Import utility functions
from utils import (
    validate_snowflake_connection_params,
    check_snowflake_prerequisites,
    display_snowflake_connection_info,
    print_snowflake_connection_troubleshooting_tips,
    print_snowflake_query_troubleshooting_tips,
    format_snowflake_results,
    test_snowflake_connectivity,
    get_snowflake_connection_string
)


class SnowflakeClient:
    """
    Snowflake database client with SSO authentication and connection management.
    
    This client handles:
    - SSO authentication (external browser)
    - Snowflake connection establishment
    - Query execution and result formatting
    - Connection cleanup
    - Error handling and troubleshooting
    """
    
    def __init__(self, 
                 account: Optional[str] = "DOORDASH",
                 user: Optional[str] = "lingfei.li",
                 warehouse: Optional[str] = "ADHOC",
                 database: Optional[str] = "PRODDB"):
        """
        Initialize Snowflake client with SSO authentication parameters.
        
        Args:
            account: Snowflake account identifier (e.g., 'org-account.snowflakecomputing.com')
            user: Snowflake username
            warehouse: Snowflake warehouse name
            database: Snowflake database name
        """
        self.conn = None
        self.cur = None
        
        # Connection parameters - prioritize environment variables, then constructor args
        self.account = account or os.environ.get('SNOWFLAKE_ACCOUNT')
        self.user = user or os.environ.get('SNOWFLAKE_USER')
        self.warehouse = warehouse or os.environ.get('SNOWFLAKE_WAREHOUSE')
        self.database = database or os.environ.get('SNOWFLAKE_DATABASE')
        
        # Validate required parameters using utility function
        validate_snowflake_connection_params(self.account, self.user)

    def __enter__(self):
        """Establish connection when entering context manager."""
        logger.info("Initializing Snowflake client...")
        logger.info("Connecting to Snowflake...")
        
        # Check prerequisites using utility function
        check_snowflake_prerequisites()
        
        try:
            # Import snowflake connector here to avoid import errors if not installed
            import snowflake.connector
            
            # Create connection
            self.conn = snowflake.connector.connect(
                account=self.account,
                user=self.user,
                authenticator='externalbrowser',
                warehouse=self.warehouse,
                database=self.database
            )
            
            self.cur = self.conn.cursor()
            logger.info("✅ Snowflake connection established")
            
            # Display connection information using utility function
            display_snowflake_connection_info(
                self.account, self.user, self.warehouse, 
                self.database
            )
            
            return self
            
        except ImportError:
            logger.error("❌ Snowflake connector not installed")
            logger.error("   Install with: pip install snowflake-connector-python")
            raise
        except Exception as e:
            logger.error(f"❌ Snowflake connection failed: {e}")
            print_snowflake_connection_troubleshooting_tips(self.account)
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up connection when exiting context manager."""
        logger.info("Closing Snowflake connection...")
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("✅ Snowflake connection closed")
        
        # Return False to propagate any exceptions
        return False

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries containing query results
        """
        logger.info(f"Executing Snowflake query:\n{query}")
        
        try:
            # Execute the query
            self.cur.execute(query)
            
            # Get column names
            columns = [desc[0] for desc in self.cur.description] if self.cur.description else []
            
            # Fetch all results
            rows = self.cur.fetchall()
            
            # Convert to list of dictionaries
            results = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                results.append(row_dict)
            
            logger.info(f"✅ Query executed successfully: {len(results)} rows returned")
            return results
            
        except Exception as e:
            logger.error(f"❌ Query execution failed: {e}")
            print_snowflake_query_troubleshooting_tips(query)
            raise

    def execute_query_with_timeout(self, query: str, timeout_seconds: int = 300) -> List[Dict[str, Any]]:
        """
        Execute a query with a timeout.
        
        Args:
            query: SQL query to execute
            timeout_seconds: Maximum execution time in seconds
            
        Returns:
            List of dictionaries containing query results
        """
        logger.info(f"Executing Snowflake query with {timeout_seconds}s timeout:\n{query}")
        
        try:
            # Set statement timeout
            self.cur.execute(f"SET STATEMENT_TIMEOUT_IN_SECONDS = {timeout_seconds}")
            
            # Execute the actual query
            return self.execute_query(query)
            
        except Exception as e:
            logger.error(f"❌ Query execution with timeout failed: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test the Snowflake connection with a simple query.
        
        Returns:
            True if connection is working, False otherwise
        """
        try:
            logger.info("🧪 Testing Snowflake connection...")
            
            # Simple test query
            test_query = "SELECT CURRENT_TIMESTAMP(), CURRENT_VERSION(), CURRENT_USER()"
            results = self.execute_query(test_query)
            
            if results and len(results) > 0:
                timestamp, version, user = results[0].values()
                logger.info(f"✅ Connection test successful:")
                logger.info(f"   Current time: {timestamp}")
                logger.info(f"   Snowflake version: {version}")
                logger.info(f"   Connected as: {user}")
                return True
            else:
                logger.error("❌ Connection test failed: No results returned")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False

    def show_warehouses(self) -> List[Dict[str, Any]]:
        """Show available warehouses."""
        return self.execute_query("SHOW WAREHOUSES")

    def show_databases(self) -> List[Dict[str, Any]]:
        """Show available databases."""
        return self.execute_query("SHOW DATABASES")

    def show_schemas(self, database: Optional[str] = None) -> List[Dict[str, Any]]:
        """Show schemas in a database."""
        if database:
            return self.execute_query(f"SHOW SCHEMAS IN DATABASE {database}")
        else:
            return self.execute_query("SHOW SCHEMAS")

    def show_tables(self, database: Optional[str] = None, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """Show tables in a schema."""
        if database and schema:
            return self.execute_query(f"SHOW TABLES IN DATABASE {database}.{schema}")
        elif schema:
            return self.execute_query(f"SHOW TABLES IN SCHEMA {schema}")
        else:
            return self.execute_query("SHOW TABLES")

    def describe_table(self, table_name: str, database: Optional[str] = None, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """Describe table structure."""
        if database and schema:
            return self.execute_query(f"DESCRIBE TABLE {database}.{schema}.{table_name}")
        elif schema:
            return self.execute_query(f"DESCRIBE TABLE {schema}.{table_name}")
        else:
            return self.execute_query(f"DESCRIBE TABLE {table_name}")

    def get_connection_string(self) -> str:
        """Get a formatted connection string for reference."""
        return get_snowflake_connection_string(
            self.account, self.user, self.warehouse, 
            self.database
        )

    def test_connectivity(self) -> bool:
        """Test basic connectivity to Snowflake account."""
        return test_snowflake_connectivity(self.account) 