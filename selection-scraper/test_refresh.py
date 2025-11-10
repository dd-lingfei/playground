#!/usr/bin/env python3

import argparse
from workflow_steps.refresh_qdrant_collection import refresh_qdrant_collection
from workflow_steps.search_against_qdrant import search_against_qdrant
from config import CollectionConfig
from utils import print_metrics, verify_prod_connection
from datetime import datetime


# Example usage
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Upsert data to Qdrant collection')
    parser.add_argument('--metrics', action='store_true', help='Print performance metrics at the end')
    parser.add_argument('--store-id', type=int, default=1741819, help='Store ID (default: 1741819)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of records to process (default: no limit)')
    
    args = parser.parse_args()
    
    # Verify production connection
    verify_prod_connection()
    
    # Specify the store ID you want to refresh
    store_id = args.store_id
    limit = args.limit
    collection_name = CollectionConfig.get_collection_name(store_id)
    print(f"Collection name: {collection_name}")
    
    limit_msg = f"with limit: {limit}" if limit is not None else "with no limit"
    print(f"Starting refresh for store_id: {store_id} {limit_msg}")
    
    result = refresh_qdrant_collection(store_id, limit=limit)
    
    # Print performance metrics if requested
    if args.metrics:
        print_metrics()