#!/usr/bin/env python3
"""
SQL Utilities - File Operations and SQL Helper Functions
=======================================================

This module contains utility functions for:
- Loading SQL files
- SQL file validation
- SQL content processing
"""

import os


def load_sql_file(filename: str) -> str:
    """
    Load SQL content from a file.
    
    Args:
        filename (str): Path to the SQL file
        
    Returns:
        str: SQL content as string, or None if file cannot be loaded
    """
    try:
        if not os.path.exists(filename):
            print(f"❌ SQL file {filename} not found in current directory")
            return None
            
        with open(filename, 'r') as f:
            sql_content = f.read().strip()
        
        if not sql_content:
            print(f"❌ SQL file {filename} is empty")
            return None
            
        print(f"✅ Loaded SQL from {filename}")
        return sql_content
        
    except Exception as e:
        print(f"❌ Error reading SQL file {filename}: {e}")
        return None


def validate_sql_file(filename: str) -> bool:
    """
    Validate that a SQL file exists and is readable.
    
    Args:
        filename (str): Path to the SQL file
        
    Returns:
        bool: True if file is valid, False otherwise
    """
    if not os.path.exists(filename):
        print(f"❌ SQL file {filename} not found")
        return False
    
    if not os.access(filename, os.R_OK):
        print(f"❌ SQL file {filename} is not readable")
        return False
    
    return True


def get_sql_file_size(filename: str) -> int:
    """
    Get the size of a SQL file in bytes.
    
    Args:
        filename (str): Path to the SQL file
        
    Returns:
        int: File size in bytes, or -1 if error
    """
    try:
        if not os.path.exists(filename):
            return -1
        return os.path.getsize(filename)
    except Exception:
        return -1 