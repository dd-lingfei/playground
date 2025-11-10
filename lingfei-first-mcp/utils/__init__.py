#!/usr/bin/env python3
"""
Utils Package - DoorDash Trino Utilities
========================================

This package contains utility modules for:
- SQL file operations (sql_utils)
- Trino connection handling and troubleshooting (trino_utils)
- Snowflake connection handling and troubleshooting (snowflake_utils)
"""

from .sql_utils import load_sql_file, validate_sql_file, get_sql_file_size
from .trino_utils import (
    handle_trino_execution_error,
    handle_specific_table_error,
    format_query_results,
    format_detailed_results
)
from .snowflake_utils import (
    validate_snowflake_connection_params,
    check_snowflake_prerequisites,
    display_snowflake_connection_info,
    print_snowflake_connection_troubleshooting_tips,
    print_snowflake_query_troubleshooting_tips,
    format_snowflake_results,
    test_snowflake_connectivity,
    get_snowflake_connection_string
)

__all__ = [
    # SQL utilities
    'load_sql_file',
    'validate_sql_file', 
    'get_sql_file_size',
    
    # Trino utilities
    'handle_trino_execution_error',
    'handle_specific_table_error',
    'format_query_results',
    'format_detailed_results',
    
    # Snowflake utilities
    'validate_snowflake_connection_params',
    'check_snowflake_prerequisites',
    'display_snowflake_connection_info',
    'print_snowflake_connection_troubleshooting_tips',
    'print_snowflake_query_troubleshooting_tips',
    'format_snowflake_results',
    'test_snowflake_connectivity',
    'get_snowflake_connection_string'
] 