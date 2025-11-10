#!/usr/bin/env python3
"""
Trino Client - Database Connection and Query Execution
=====================================================

This module provides a Trino client for connecting to and querying
Trino databases with OAuth2 authentication and proper connection management.
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
    handle_trino_execution_error,
    handle_specific_table_error,
    format_query_results,
    format_detailed_results
)


class TrinoClient:
    """
    Trino database client with OAuth2 authentication and connection management.
    
    This client handles:
    - OAuth2 authentication
    - Trino connection establishment
    - Query execution and result formatting
    - Connection cleanup
    - Error handling and troubleshooting
    """
    
    def __init__(self, 
                 host: Optional[str] = "trino.doordash.team",
                 port: Optional[int] = 443,
                 user: Optional[str] = "lingfei.li@doordash.com",
                 http_scheme: Optional[str] = "https"):
        """
        Initialize Trino client with OAuth2 authentication parameters.
        
        Args:
            host: Trino server hostname
            port: Trino server port
            user: Trino username
            http_scheme: HTTP scheme (http or https)
        """
        self.conn = None
        self.cur = None
        
        # Connection parameters - prioritize environment variables, then constructor args
        self.host = host or os.environ.get('TRINO_HOST')
        self.port = port or int(os.environ.get('TRINO_PORT', 443))
        self.user = user or os.environ.get('TRINO_USER')
        self.http_scheme = http_scheme or os.environ.get('TRINO_HTTP_SCHEME', 'https')
        
        # Validate required parameters
        self._validate_connection_params()

    def _validate_connection_params(self):
        """Validate required connection parameters."""
        if not self.host:
            raise ValueError("Trino host is required")
        if not self.user:
            raise ValueError("Trino user is required")
        if not self.port or not isinstance(self.port, int):
            raise ValueError("Trino port must be a valid integer")
        if self.http_scheme not in ['http', 'https']:
            raise ValueError("HTTP scheme must be 'http' or 'https'")

    def __enter__(self):
        """Establish connection when entering context manager."""
        logger.info("Initializing Trino client...")
        logger.info("Connecting to Trino...")
        
        try:
            # Import trino connector here to avoid import errors if not installed
            from trino.dbapi import connect
            from trino.auth import OAuth2Authentication
            
            # Create connection
            self.conn = connect(
                host=self.host,
                port=self.port,
                user=self.user,
                auth=OAuth2Authentication(),
                http_scheme=self.http_scheme,
            )
            
            self.cur = self.conn.cursor()
            logger.info("✅ Trino connection established")
            
            # Display connection information
            self._display_connection_info()
            
            return self
            
        except ImportError:
            logger.error("❌ Trino connector not installed")
            logger.error("   Install with: pip install trino")
            raise
        except Exception as e:
            logger.error(f"❌ Trino connection failed: {e}")
            self._print_connection_troubleshooting_tips()
            raise

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up connection when exiting context manager."""
        logger.info("Closing Trino connection...")
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        logger.info("✅ Trino connection closed")
        
        # Return False to propagate any exceptions
        return False

    def _display_connection_info(self):
        """Display connection information."""
        logger.info(f"🔗 Connected to Trino:")
        logger.info(f"   Host: {self.host}:{self.port}")
        logger.info(f"   User: {self.user}")
        logger.info(f"   Scheme: {self.http_scheme}")

    def _print_connection_troubleshooting_tips(self):
        """Print connection troubleshooting tips."""
        logger.error("\n🔧 Connection troubleshooting tips:")
        logger.error("1. Ensure you're connected to DoorDash VPN")
        logger.error("2. Verify OAuth2 authentication is working")
        logger.error("3. Check if the Trino server is accessible")
        logger.error("4. Verify your credentials and permissions")

    def _print_query_troubleshooting_tips(self, query: str):
        """Print query troubleshooting tips."""
        logger.error("\n🔧 Query troubleshooting tips:")
        logger.error("1. Ensure you're connected to DoorDash VPN")
        logger.error("2. Verify OAuth2 authentication is working")
        logger.error("3. Check if the required tables exist")
        logger.error("4. Verify you have permissions to access the tables")
        logger.error("5. Check if the catalogs are available")
        logger.error(f"6. Review your query syntax: {query[:100]}...")

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return results.
        
        Args:
            query: SQL query to execute
            
        Returns:
            List of dictionaries containing query results
        """
        logger.info(f"Executing Trino query:\n{query}")
        
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
            handle_trino_execution_error(e, "query execution")
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
        logger.info(f"Executing Trino query with {timeout_seconds}s timeout:\n{query}")
        
        try:
            # Set session timeout (Trino specific)
            self.cur.execute(f"SET SESSION query_max_run_time = '{timeout_seconds}s'")
            
            # Execute the actual query
            return self.execute_query(query)
            
        except Exception as e:
            logger.error(f"❌ Query execution with timeout failed: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test the Trino connection with a simple query.
        
        Returns:
            True if connection is working, False otherwise
        """
        try:
            logger.info("🧪 Testing Trino connection...")
            
            # Simple test query
            test_query = "SELECT current_user, current_timestamp, node_id FROM system.runtime.nodes LIMIT 1"
            results = self.execute_query(test_query)
            
            if results and len(results) > 0:
                user, timestamp, node_id = results[0].values()
                logger.info(f"✅ Connection test successful:")
                logger.info(f"   Current user: {user}")
                logger.info(f"   Current time: {timestamp}")
                logger.info(f"   Node ID: {node_id}")
                return True
            else:
                logger.error("❌ Connection test failed: No results returned")
                return False
                
        except Exception as e:
            logger.error(f"❌ Connection test failed: {e}")
            return False

    def show_catalogs(self) -> List[Dict[str, Any]]:
        """Show available catalogs."""
        return self.execute_query("SHOW CATALOGS")

    def show_schemas(self, catalog: Optional[str] = None) -> List[Dict[str, Any]]:
        """Show schemas in a catalog."""
        if catalog:
            return self.execute_query(f"SHOW SCHEMAS FROM {catalog}")
        else:
            return self.execute_query("SHOW SCHEMAS")

    def show_tables(self, catalog: Optional[str] = None, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """Show tables in a schema."""
        if catalog and schema:
            return self.execute_query(f"SHOW TABLES FROM {catalog}.{schema}")
        elif schema:
            return self.execute_query(f"SHOW TABLES FROM {schema}")
        else:
            return self.execute_query("SHOW TABLES")

    def describe_table(self, table_name: str, catalog: Optional[str] = None, schema: Optional[str] = None) -> List[Dict[str, Any]]:
        """Describe table structure."""
        if catalog and schema:
            return self.execute_query(f"DESCRIBE {catalog}.{schema}.{table_name}")
        elif schema:
            return self.execute_query(f"DESCRIBE {schema}.{table_name}")
        else:
            return self.execute_query(f"DESCRIBE {table_name}")

    def get_connection_string(self) -> str:
        """Get a formatted connection string for reference."""
        return f"{self.http_scheme}://{self.user}@{self.host}:{self.port}"

    def test_connectivity(self) -> bool:
        """Test basic connectivity to Trino server."""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.host, self.port))
            sock.close()
            return result == 0
        except Exception:
            return False

    def run_diagnostics(self) -> None:
        """Run comprehensive diagnostics on the Trino connection."""
        logger.info("🔧 Running Trino connection diagnostics...")
        
        # Test basic connectivity
        if self.test_connectivity():
            logger.info("✅ Basic network connectivity: OK")
        else:
            logger.error("❌ Basic network connectivity: FAILED")
            return
        
        # Test connection
        if self.test_connection():
            logger.info("✅ Database connection: OK")
        else:
            logger.error("❌ Database connection: FAILED")
            return
        
        # Test catalog access
        try:
            catalogs = self.show_catalogs()
            logger.info(f"✅ Catalog access: OK ({len(catalogs)} catalogs available)")
            
            # Test specific catalogs if available
            for catalog_info in catalogs[:3]:  # Test first 3 catalogs
                catalog_name = catalog_info.get('Catalog', 'Unknown')
                try:
                    schemas = self.show_schemas(catalog_name)
                    logger.info(f"   ✅ {catalog_name}: {len(schemas)} schemas")
                except Exception as e:
                    logger.error(f"   ❌ {catalog_name}: {e}")
                    
        except Exception as e:
            logger.error(f"❌ Catalog access: FAILED - {e}")

    def format_results(self, results: List[Dict[str, Any]], max_rows: int = 5) -> None:
        """Format and display query results."""
        format_query_results(results, max_rows)

    def format_detailed_results(self, results: List[Dict[str, Any]], search_identifier: str) -> None:
        """Format and display detailed query results."""
        format_detailed_results(results, search_identifier) 