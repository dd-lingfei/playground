#!/usr/bin/env python3
"""
DoorDash Trino Test Entrypoint - MSID-based Item Lookup with Business/Store Support
==================================================================================

This script takes an MSID as a command line parameter and looks up
item level details of catalog attributes using the TrinoClient.
It also supports optional business_id and store_id parameters.
"""

import json
import sys
import argparse
from clients import TrinoClient
from clients.snowflake_client import SnowflakeClient
from utils import (
    load_sql_file,
    handle_trino_execution_error,
    handle_specific_table_error,
    run_basic_connectivity_tests,
    format_query_results,
    format_detailed_results
)
import logging
import os
from typing import Optional

# Set up logging
logging.basicConfig(level=logging.INFO)


def get_item_level_details_of_catalog_attributes(search_item_msid: str, business_id: Optional[str] = "", store_id: Optional[str] = ""):
    """
    Get item level details of catalog attributes for a specific MSID.
    
    Args:
        search_item_msid (str): The MSID to search for
        business_id (str, optional): The business ID to filter by
        store_id (str, optional): The store ID to filter by
        
    Returns:
        list: Query results as a list of dictionaries
    """
    print(f"🔍 Getting item level details for MSID: {search_item_msid}")
    if business_id and business_id.strip():
        print(f"   Business ID: {business_id}")
    if store_id and store_id.strip():
        print(f"   Store ID: {store_id}")
    print("=" * 60)
    
    # Load SQL from file
    sql_query = load_sql_file('queries/snowflake/item_level_details_of_catalog_attributes.sql')
    if not sql_query:
        print("Cannot proceed without SQL query. Please check queries/snowflake/item_level_details_of_catalog_attributes.sql file.")
        return None
    
    # Replace the MSID placeholder in the SQL
    sql_query = sql_query.replace('{{search_item_msid}}', search_item_msid)
    
    # Add business_id filter if provided
    if business_id and business_id.strip():
        # Check if the SQL already has a business_id filter, if not add one
        if '-- PLACEHOLDER FOR BUSINESS_ID FILTER --' in sql_query:
            sql_query = sql_query.replace('-- PLACEHOLDER FOR BUSINESS_ID FILTER --', f"business_id = '{business_id}'")
        else:
            print("business_id was provided but not found in the SQL query")
            return None
    
    # Add store_id filter if provided
    if store_id and store_id.strip():
        # Check if the SQL already has a store_id filter, if not add one
        if 'STORE_ID' in sql_query:
            sql_query = sql_query.replace('STORE_ID', f"STORE_ID = '{store_id}'")
        else:
            # Add store_id filter to the WHERE clause
            sql_query = sql_query.replace('where 1=1', f"where 1=1\n   and STORE_ID = '{store_id}'")
    
    print(f"\n📄 SQL Query to execute:")
    print("-" * 40)
    print(sql_query)
    print("-" * 40)
    
    try:
        print("\n🔗 Connecting to DoorDash Snowflake...")
        with SnowflakeClient() as client:
            print("\n🔍 Executing item level details query...")
            
            # Execute the SQL query
            results = client.execute_query(sql_query)
            
            print(f"\n✅ Query executed successfully!")
            print(f"📊 Results: {len(results)} rows returned")
            
            # Use utility function to format results
            format_detailed_results(results, f"MSID '{search_item_msid}'")
            
            return results
            
    except Exception as e:
        handle_trino_execution_error(e, "item level details query execution")
        return None


def get_item_menu_history(search_item_msid: str, business_id: Optional[str] = "", store_id: Optional[str] = ""):
    """
    Get item menu history for a specific MSID.
    
    Args:
        search_item_msid (str): The MSID to search for
        business_id (str, optional): The business ID to filter by
        store_id (str, optional): The store ID to filter by
        
    Returns:
        list: Query results as a list of dictionaries
    """
    print(f"🔍 Getting item menu history for MSID: {search_item_msid}")
    if business_id and business_id.strip():
        print(f"   Business ID: {business_id}")
    if store_id and store_id.strip():
        print(f"   Store ID: {store_id}")
    print("=" * 60)
    
    # Load SQL from file
    sql_query = load_sql_file('queries/snowflake/item_menu_history.sql')
    if not sql_query:
        print("Cannot proceed without SQL query. Please check queries/snowflake/item_menu_history.sql file.")
        return None
    
    # Replace the MSID placeholder in the SQL
    sql_query = sql_query.replace('{{search_item_msid}}', search_item_msid)
    
    # Add business_id filter if provided
    if business_id and business_id.strip():
        # Check if the SQL already has a business_id filter, if not add one
        if '{{ businessid }}' in sql_query:
            sql_query = sql_query.replace('{{ businessid }}', business_id)
        else:
            # Add business_id filter to the WHERE clause if not already present
            if 'business_id =' not in sql_query:
                sql_query = sql_query.replace('where 1=1', f"where 1=1\n   and business_id = '{business_id}'")
    
    # Add store_id filter if provided
    if store_id and store_id.strip():
        # Add store_id filter to the WHERE clause if not already present
        if 'store_id =' not in sql_query:
            sql_query = sql_query.replace('where 1=1', f"where 1=1\n   and store_id = '{store_id}'")
    
    print(f"\n📄 SQL Query to execute:")
    print("-" * 40)
    print(sql_query)
    print("-" * 40)
    
    try:
        print("\n🔗 Connecting to DoorDash Snowflake...")
        with SnowflakeClient() as client:
            print("\n🔍 Executing item menu history query...")
            
            # Execute the SQL query
            results = client.execute_query(sql_query)
            
            print(f"\n✅ Query executed successfully!")
            print(f"📊 Results: {len(results)} rows returned")
            
            # Use utility function to format results
            format_detailed_results(results, f"MSID '{search_item_msid}' menu history")
            
            return results
            
    except Exception as e:
        handle_trino_execution_error(e, "item menu history query execution")
        return None

def get_live_inf_by_merchant(business_id: str):
    pass #TODO




def request_a_sku():
    """Basic test function to return results from request_a_sku.sql - see if things are working"""
    print("DoorDash Trino Client - SQL File Execution")
    print("=" * 50)
    
    # Load SQL from file
    sql_query = load_sql_file('queries/trino/request_a_sku.sql')
    if not sql_query:
        print("Cannot proceed without SQL query. Please check queries/trino/request_a_sku.sql file.")
        return
    
    print(f"\n📄 SQL Query to execute:")
    print("-" * 30)
    print(sql_query)
    print("-" * 30)
    
    try:
        print("\n🔗 Connecting to DoorDash Trino...")
        with TrinoClient() as client:
            print("\n🔍 Executing queries/trino/request_a_sku.sql query...")
            
            # Execute the SQL from file
            results = client.execute_query(sql_query)
            
            print(f"\n✅ Query executed successfully!")
            print(f"📊 Results: {len(results)} rows returned")
            
            # Use utility function to format results
            format_query_results(results, max_rows=5, truncate_length=50)
            
    except Exception as e:
        handle_specific_table_error(e, 'iceberg.nv_item_selection.request_a_sku')
        
        # Additional troubleshooting - try basic queries
        run_basic_connectivity_tests()


def main():
    """Main function that takes MSID and optional business_id/store_id as command line arguments."""
    parser = argparse.ArgumentParser(
        description="Look up item details by MSID using DoorDash Trino/Snowflake with optional business/store filtering",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_entrypoint.py --msid "ABC123"
  python test_entrypoint.py -m "XYZ789" --business-id "BUS001"
  python test_entrypoint.py -m "ABC123" --store-id "STORE001"
  python test_entrypoint.py -m "XYZ789" --business-id "BUS001" --store-id "STORE001"
  python test_entrypoint.py --msid "ABC123" --query "item_level_details"
  python test_entrypoint.py --msid "ABC123" --query "item_menu_history"
  python test_entrypoint.py --test-request-a-sku
        """
    )
    
    parser.add_argument(
        '--msid', '-m',
        type=str,
        help='MSID to search for (required for item lookup)'
    )
    
    parser.add_argument(
        '--business-id', '-b',
        type=str,
        help='Business ID to filter results (optional)'
    )
    
    parser.add_argument(
        '--store-id', '-s',
        type=str,
        help='Store ID to filter results (optional)'
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        choices=['item_level_details', 'item_menu_history', 'request_a_sku'],
        help='Type of query to run (default: item_level_details)'
    )
    
    parser.add_argument(
        '--test-request-a-sku',
        action='store_true',
        help='Run the basic request_a_sku test instead of MSID lookup'
    )
    
    args = parser.parse_args()
    
    print("🚀 DoorDash Trino Test Entrypoint")
    print("=" * 50)
    
    
    if args.msid:
        print(f"🔍 Looking up item details for MSID: {args.msid}")
        print(f"📊 Query type: {args.query}")
        
        # Show additional filters if provided
        if args.business_id and args.business_id.strip():
            print(f"   Business ID filter: {args.business_id}")
        if args.store_id and args.store_id.strip():
            print(f"   Store ID filter: {args.store_id}")
        
        # Choose which function to call based on query type
        if args.query == 'item_level_details':
            results = get_item_level_details_of_catalog_attributes(
                args.msid, 
                business_id=args.business_id, 
                store_id=args.store_id
            )
        elif args.query == 'item_menu_history':
            results = get_item_menu_history(
                args.msid, 
                business_id=args.business_id, 
                store_id=args.store_id
            )
        elif args.query == 'request_a_sku':
            results = request_a_sku()
        else:
            print(f"❌ Unknown query type: {args.query}")
            sys.exit(1)
        
        if results is not None:
            print(f"\n✅ MSID lookup completed successfully for: {args.msid}")
            print(f"   Query type: {args.query}")
            if args.business_id and args.business_id.strip():
                print(f"   Filtered by Business ID: {args.business_id}")
            if args.store_id and args.store_id.strip():
                print(f"   Filtered by Store ID: {args.store_id}")
        else:
            print(f"\n❌ MSID lookup failed for: {args.msid}")
            sys.exit(1)
    else:
        print("❌ No MSID provided and no test mode selected.")
        print("Use --help for usage information.")
        print("\nAvailable query types:")
        print("  - item_level_details: Get item level details of catalog attributes")
        print("  - item_menu_history: Get item menu history")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()