#!/usr/bin/env python3

from datetime import datetime
from typing import Dict, Any, List, Optional
from clients import OpenAIClient, DDSelectionQdrantClient, DoorDashSnowflakeDataAccessor, MockDoorDashSnowflakeDataAccessor
from config import CollectionConfig

def refresh_qdrant_collection(store_id: int, collection_name: str = None, limit: Optional[int] = None) -> Dict[str, Any]:
    # Initialize clients
    qdrant_client = DDSelectionQdrantClient()
    
    # Generate collection name with today's date
    if collection_name is None:
        collection_name = CollectionConfig.get_collection_name(store_id)
    
    print(f"Processing store_id: {store_id}")
    print(f"Collection name: {collection_name}")
    print(f"Record limit: {limit if limit is not None else 'No limit'}")
    
    with MockDoorDashSnowflakeDataAccessor() as sf_client:
        df = sf_client.get_selection_data(limit=limit, store_id=store_id)
    
    if df.empty:
        print(f"No data found for store_id {store_id}")
        return {
            "collection_name": collection_name,
            "items_processed": 0,
            "status": "no_data"
        }
    
    print(f"Retrieved {len(df)} items from Snowflake")
    
    # Create Qdrant collection if it doesn't exist
    if not qdrant_client.collection_exists(collection_name):
        print(f"Creating new collection: {collection_name}")
        qdrant_client.create_collection(collection_name=collection_name)
    else:
        print(f"Collection {collection_name} already exists")
    
    print(f"Inserting {len(df)} items into collection {collection_name}")
    qdrant_client.upsert_df(
        collection_name=collection_name,
        df=df
    )
    print(f"Successfully upserted {len(df)} items to collection {collection_name}")