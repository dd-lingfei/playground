#!/usr/bin/env python3
"""
Trino Utilities - Exception Handling, Troubleshooting, and Result Formatting
==========================================================================

This module contains utility functions for:
- Handling exceptions and troubleshooting common issues with Trino connections and queries
- Formatting query results
- Note: Connectivity test functions have been moved to TrinoClient to avoid circular imports
"""

import logging

# Set up logging
logger = logging.getLogger(__name__)


def handle_trino_execution_error(error: Exception, context: str = "query execution") -> None:
    """
    Handle Trino execution errors with standardized troubleshooting information.
    
    Args:
        error (Exception): The exception that occurred
        context (str): Context description for the error
    """
    logger.error(f"\n❌ {context.capitalize()} failed: {error}")
    logger.error("\nTroubleshooting:")
    logger.error("1. Ensure you're connected to DoorDash VPN")
    logger.error("2. Verify OAuth2 authentication is working")
    logger.error("3. Check if the required tables exist")
    logger.error("4. Verify you have permissions to access the tables")
    logger.error("5. Check if the catalogs are available")


def handle_specific_table_error(error: Exception, table_path: str) -> None:
    """
    Handle errors specific to a particular table with targeted troubleshooting.
    
    Args:
        error (Exception): The exception that occurred
        table_path (str): The table path that caused the error
    """
    logger.error(f"\n❌ Execution failed: {error}")
    logger.error(f"\nTroubleshooting for table '{table_path}':")
    logger.error("1. Ensure you're connected to DoorDash VPN")
    logger.error("2. Verify OAuth2 authentication is working")
    logger.error(f"3. Check if table '{table_path}' exists")
    logger.error("4. Verify you have permissions to access this table")
    logger.error("5. Check if the catalog is available")


def format_query_results(results: list, max_rows: int = 5, truncate_length: int = 50) -> None:
    """
    Format and display query results in a readable format.
    
    Args:
        results (list): Query results as a list of dictionaries
        max_rows (int): Maximum number of rows to display
        truncate_length (int): Maximum length for cell values before truncation
    """
    if not results:
        logger.info("   No data returned (empty result set)")
        return
    
    # Show column information
    columns = list(results[0].keys())
    logger.info(f"📋 Columns ({len(columns)}): {', '.join(columns)}")
    
    # Show results
    display_rows = min(max_rows, len(results))
    logger.info(f"\n📋 Sample results (first {display_rows} rows):")
    
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


def format_detailed_results(results: list, search_identifier: str, truncate_length: int = 80) -> None:
    """
    Format and display detailed query results for specific item lookups.
    
    Args:
        results (list): Query results as a list of dictionaries
        search_identifier (str): Identifier used in the search (e.g., MSID)
        truncate_length (int): Maximum length for cell values before truncation
    """
    if not results:
        logger.info(f"   No data returned for {search_identifier} (empty result set)")
        return
    
    # Show column information
    columns = list(results[0].keys())
    logger.info(f"📋 Columns ({len(columns)}): {', '.join(columns)}")
    
    # Show all results (since this is a specific item lookup)
    logger.info(f"\n📋 Results for {search_identifier}:")
    for i, row in enumerate(results, 1):
        logger.info(f"   Row {i}:")
        for key, value in row.items():
            # Truncate long values for display
            display_value = str(value)
            if len(display_value) > truncate_length:
                display_value = display_value[:truncate_length-3] + "..."
            logger.info(f"     {key}: {display_value}")
        logger.info("") 