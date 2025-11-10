#!/usr/bin/env python3

from datetime import datetime
from typing import Dict, Any, List
from clients import OpenAIClient, DDSelectionQdrantClient, DoorDashSnowflakeDataAccessor
from config import CollectionConfig
from utils import get_app_logger
from qdrant_client.http.models import Distance


def search_against_qdrant(store_id: int, search_terms: List[str], collection_name: str = None, logger=None) -> Dict[str, Any]:
    # Initialize clients and logger
    if collection_name is None:
        collection_name = CollectionConfig.get_collection_name(store_id)
    
    if logger is None:
        logger = get_app_logger()

    qdrant_client = DDSelectionQdrantClient()
    logger.info(f"Searching for {len(search_terms)} terms in collection: {collection_name}")
    search_results_list = qdrant_client.search(collection_name=collection_name, search_terms=search_terms)
    return search_results_list
