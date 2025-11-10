#!/usr/bin/env python3
"""
Snowflake Utilities - Helper Functions and Troubleshooting
========================================================

This module contains utility functions for:
- Snowflake connection troubleshooting
- Query execution troubleshooting
- Connection parameter validation
"""

import os
import socket
import logging
from typing import List, Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)


def validate_snowflake_connection_params(account: str, user: str) -> None:
    """
    Validate that required Snowflake connection parameters are provided.
    
    Args:
        account: Snowflake account identifier
        user: Snowflake username
        
    Raises:
        ValueError: If required parameters are missing
    """
    required_params = ['account', 'user']
    param_values = {'account': account, 'user': user}
    
    missing_params = [param for param in required_params if not param_values[param]]

    if missing_params:
        raise ValueError(f"Missing required Snowflake connection parameters: {', '.join(missing_params)}")
    
    logger.info("✅ Snowflake connection parameters validated")


def check_snowflake_prerequisites() -> None:
    """Check prerequisites for Snowflake connection."""
    logger.info("🔍 Checking Snowflake prerequisites...")
    
    # Check for common Snowflake environment variables
    snowflake_vars = [
        'SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER',
        'SNOWFLAKE_WAREHOUSE', 'SNOWFLAKE_DATABASE'
    ]
    missing_vars = [var for var in snowflake_vars if not os.environ.get(var)]
    if missing_vars:
        logger.info(f"ℹ️  Some Snowflake environment variables not set: {', '.join(missing_vars)}")
    
    # Check if we can access the internet (basic connectivity test)
    try:
        socket.gethostbyname("8.8.8.8")
        logger.info("✅ Basic internet connectivity available")
    except socket.gaierror:
        logger.warning("⚠️  Basic internet connectivity test failed")


def display_snowflake_connection_info(account: str, user: str, warehouse: Optional[str] = None, 
                                    database: Optional[str] = None) -> None:
    """
    Display Snowflake connection information.
    
    Args:
        account: Snowflake account identifier
        user: Snowflake username
        warehouse: Snowflake warehouse name
        database: Snowflake database name
    """
    logger.info(f"🔗 Snowflake Connection Info:")
    logger.info(f"   Account: {account}")
    logger.info(f"   User: {user}")
    logger.info(f"   Warehouse: {warehouse or 'Not set'}")
    logger.info(f"   Database: {database or 'Not set'}")


def print_snowflake_connection_troubleshooting_tips(account: str) -> None:
    """
    Print troubleshooting tips for Snowflake connection issues.
    
    Args:
        account: Snowflake account identifier for troubleshooting
    """
    logger.error("\n🔧 SNOWFLAKE CONNECTION TROUBLESHOOTING:")
    logger.error("=" * 50)
    logger.error("1. 🔑 CREDENTIALS:")
    logger.error("   • Verify account, username are correct")
    logger.error("   • Check if account is locked or expired")
    logger.error("   • Ensure user has proper permissions")
    
    logger.error("\n2. 🌐 NETWORK:")
    logger.error("   • Check internet connectivity")
    logger.error("   • Verify firewall allows Snowflake connections")
    logger.error(f"   • Test: ping {account}")
    logger.error("   • Verify port 443 (HTTPS) is accessible")
    
    logger.error("\n3. ⚙️  CONFIGURATION:")
    logger.error("   • Verify warehouse and database exist")
    logger.error("   • Check if user has access to specified resources")
    logger.error("   • Ensure account identifier format is correct")
    logger.error("   • Verify account is not suspended")
    
    logger.error("\n4. 📱 IMMEDIATE ACTIONS:")
    logger.error("   • Restart your terminal/IDE")
    logger.error("   • Clear any cached credentials")
    logger.error("   • Try connecting from Snowflake web interface")
    logger.error("   • Check Snowflake service status")
    logger.error("   • Verify your IP is not blocked")
    
    logger.error("=" * 50)


def print_snowflake_query_troubleshooting_tips(query: str) -> None:
    """
    Print troubleshooting tips for Snowflake query execution issues.
    
    Args:
        query: The query that caused the issue
    """
    logger.error("\n🔧 SNOWFLAKE QUERY EXECUTION TROUBLESHOOTING:")
    logger.error("=" * 50)
    logger.error(f"Query: {query[:100]}{'...' if len(query) > 100 else ''}")
    logger.error("\n1. 🔍 SYNTAX:")
    logger.error("   • Check SQL syntax for errors")
    logger.error("   • Verify table and column names exist")
    logger.error("   • Check for missing quotes or semicolons")
    logger.error("   • Verify Snowflake-specific syntax is correct")
    
    logger.error("\n2. 🔐 PERMISSIONS:")
    logger.error("   • Verify user has SELECT permission on tables")
    logger.error("   • Check if user has access to specified database")
    logger.error("   • Ensure user has necessary privileges")
    logger.error("   • Verify warehouse access permissions")
    
    logger.error("\n3. ⚡ PERFORMANCE:")
    logger.error("   • Check if warehouse is running")
    logger.error("   • Verify warehouse size is appropriate")
    logger.error("   • Consider adding query timeout")
    logger.error("   • Check for concurrent query limits")
    
    logger.error("\n4. 🗄️  RESOURCES:")
    logger.error("   • Verify database exists")
    logger.error("   • Check if tables are accessible")
    logger.error("   • Ensure warehouse is not suspended")
    logger.error("   • Verify user has access to resources")
    
    logger.error("=" * 50)


def format_snowflake_results(results: List[Dict[str, Any]], max_rows: int = 10, truncate_length: int = 100) -> None:
    """
    Format and display Snowflake query results in a readable format.
    
    Args:
        results: Query results as a list of dictionaries
        max_rows: Maximum number of rows to display
        truncate_length: Maximum length for cell values before truncation
    """
    if not results:
        logger.info("   No data returned (empty result set)")
        return
    
    # Show column information
    columns = list(results[0].keys())
    logger.info(f"📋 Columns ({len(columns)}): {', '.join(columns)}")
    
    # Show results
    display_rows = min(max_rows, len(results))
    logger.info(f"\n📋 Snowflake results (first {display_rows} rows):")
    
    for i, row in enumerate(results[:display_rows], 1):
        logger.info(f"   Row {i}:")
        for key, value in row.items():
            # Truncate long values for display
            display_value = str(value)
            if len(display_value) > truncate_length:
                display_value = display_value[:truncate_length-3] + "..."
            logger.info(f"     {key}: {display_value}")
        logger.info("")
    
    if len(results) > max_rows:
        logger.info(f"   ... and {len(results) - max_rows} more rows")


def test_snowflake_connectivity(account: str) -> bool:
    """
    Test basic connectivity to Snowflake account.
    
    Args:
        account: Snowflake account identifier
        
    Returns:
        True if connectivity test passes, False otherwise
    """
    logger.info(f"🌐 Testing connectivity to Snowflake account: {account}")
    
    try:
        # Try to resolve the account hostname
        if '.snowflakecomputing.com' in account:
            hostname = account
        else:
            hostname = f"{account}.snowflakecomputing.com"
        
        socket.gethostbyname(hostname)
        logger.info("✅ Snowflake hostname is resolvable")
        return True
        
    except socket.gaierror:
        logger.error("❌ Cannot resolve Snowflake hostname")
        logger.error("   Please check your network connection and account identifier")
        return False
    except Exception as e:
        logger.error(f"❌ Connectivity test failed: {e}")
        return False


def get_snowflake_connection_string(account: str, user: str, warehouse: Optional[str] = None,
                                  database: Optional[str] = None) -> str:
    """
    Generate a Snowflake connection string for reference.
    
    Args:
        account: Snowflake account identifier
        user: Snowflake username
        warehouse: Snowflake warehouse name
        database: Snowflake database name
        
    Returns:
        Formatted connection string
    """
    connection_parts = [f"Account: {account}", f"User: {user}"]
    
    if warehouse:
        connection_parts.append(f"Warehouse: {warehouse}")
    if database:
        connection_parts.append(f"Database: {database}")
    
    return " | ".join(connection_parts) 