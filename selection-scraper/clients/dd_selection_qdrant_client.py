from qdrant_client import QdrantClient as QdrantClientBase
from qdrant_client.http import models
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from typing import List, Dict, Any, Optional, Union
from uuid import uuid4
import pandas as pd
import uuid
import json
from clients.openai_client import OpenAIClient
from config import CollectionConfig
from utils import metrics_tracker
from multiprocessing.pool import ThreadPool
import numpy as np
import tqdm
import math
from typing import Dict, List, Optional, Any
from pydash import find, omit, pick, is_empty
from enum import Enum
from multiprocessing.pool import ThreadPool
from qdrant_client.http.models import PayloadSchemaType, VectorParams, Distance
from utils import get_app_logger

UPLOAD_BATCH_SIZE = 1000
UPLOAD_THREADS = 10
UPLOAD_TIMEOUT_SECONDS = 30

# Ensure you're connected to K8S with command: dd-toolbox connect-to-cluster run main-00.prod-us-west-2
class DDSelectionQdrantClient:
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern - only one instance of DDSelectionQdrantClient will be created"""
        if cls._instance is None:
            cls._instance = super(DDSelectionQdrantClient, cls).__new__(cls)
        return cls._instance
    
    def __init__(
        self,
        host: str = None,
        grpc_port: int = None,
        https: bool = None,
        prefer_grpc: bool = None,
        timeout: int = UPLOAD_TIMEOUT_SECONDS, # seconds
        openai_client: OpenAIClient = None,
    ):
        # Only initialize once
        if self._initialized:
            return
            
        self.logger = get_app_logger()
        self.client = QdrantClientBase(
            url=host or CollectionConfig.QDRANT_HOST,
            grpc_port=grpc_port or CollectionConfig.QDRANT_GRPC_PORT,
            https=https if https is not None else CollectionConfig.QDRANT_HTTPS,
            prefer_grpc=prefer_grpc if prefer_grpc is not None else CollectionConfig.QDRANT_PREFER_GRPC,
            grpc_options=CollectionConfig.get_grpc_options(),
            timeout=timeout or CollectionConfig.QDRANT_TIMEOUT
        )
        # Use singleton OpenAI client
        self.openai_client = openai_client if openai_client is not None else OpenAIClient()
        self._initialized = True
        print("✓ DDSelectionQdrantClient singleton initialized")
        
    def _convert_to_qdrant_record(self, row: pd.Series, embedding: List[float] = None) -> dict:
        record = {
            "id": str(uuid.uuid5(namespace=uuid.UUID(CollectionConfig.UUID_NAMESPACE), name=str(row["msid"]))),
            "sentence_embedding": embedding,
            "msid": row["msid"],
            "item_name": row["item_name"],
            "photo_url": row["photo_url"]
        }

        size = row.get("size", None)
        if size is not None:
            size = str(size)
            record["size"] = size
        
        price_usd = row.get("price_usd", None)
        if price_usd is not None and not pd.isna(price_usd):
            price_usd = str(price_usd)
            record["price_usd"] = price_usd
        
        return record

    @metrics_tracker.track
    def _process_chunk(
        self,
        chunk_df: pd.DataFrame, 
        pool: ThreadPool,
        collection_name: str
    ) -> Optional[List[dict]]:

        print(f'Processing {len(chunk_df)} SKUs')
        
        # Batch generate embeddings for all items in the chunk
        item_names = chunk_df["item_name"].tolist()
        print(f'Generating embeddings for {len(item_names)} items in batch...')
        embeddings = self.openai_client.generate_embeddings(texts=item_names)
        print(f'Generated {len(embeddings)} embeddings')
        
        # Create records with pre-generated embeddings
        records = []
        for idx, (_, row) in enumerate(chunk_df.iterrows()):
            embedding = embeddings[idx] if idx < len(embeddings) else None
            record = self._convert_to_qdrant_record(row, embedding=embedding)
            records.append(record)
        
        # Filter valid records
        records = [
            x for x in records 
            if x['sentence_embedding'] is not None 
        ]
        print(f'{len(records)} valid records')

        try:
            if len(records) > 0:
                print(f'Uploading {len(records)} records...')
                self._upsert_records(records=records, collection_name=collection_name)
                print(f'Successfully uploaded {len(records)} records')
            else:
                print(f'No records to upload in this chunk')
        except Exception as e:
            print(f'Error uploading records: {e}')

    @metrics_tracker.track
    def _upsert_records(self, records: List[Dict[str, Any]], collection_name: str):
        vector_keys = list(CollectionConfig.VECTOR_CONFIGS.keys())
        points = []
        skipped = []

        for record in records:
            vectors = {
                k: v for k, v in pick(record, vector_keys).items() if not is_empty(v)
            }
            if vectors:
                points.append(
                    models.PointStruct(
                        id=record["id"],
                        vector=vectors,
                        payload=omit(record, vector_keys),
                    )
                )
            else:
                skipped.append(record["id"])

        self.client.upsert(collection_name=collection_name, points=points)
        print(f"✅ Upserted {len(points)} records")
        if skipped:
            print(f"⚠️ Skipped {len(skipped)} records due to missing vectors")
        return (len(points), len(skipped))

    
    @metrics_tracker.track        
    def upsert_df(self, collection_name: str, df: pd.DataFrame) -> Any:
        pool = ThreadPool(UPLOAD_THREADS)

        # Split data into chunks
        if len(df) > 0:
            split_count = math.ceil(len(df) / UPLOAD_BATCH_SIZE)
            list_of_dfs = np.array_split(df, split_count)
            print(f"Split into {split_count} chunks of ~{UPLOAD_BATCH_SIZE} records each")
        else:
            list_of_dfs = []
            print("No records to split into chunks")

        print("\nStarting batch upload...")
        for i, chunk_df in enumerate(tqdm.tqdm(list_of_dfs, desc="Uploading chunks")):
            self._process_chunk(
                chunk_df, 
                pool=pool,
                collection_name=collection_name
            )

    @metrics_tracker.track
    def search(self, collection_name: str, search_terms: List[str], limit: int = 5) -> Any:
        search_term_embeddings = self.openai_client.generate_embeddings(texts=search_terms)
        search_results_list = [self.client.query_points(
            collection_name=collection_name,
            query=search_term_embedding,
            using='sentence_embedding',
            limit=limit,
        ) for search_term_embedding in search_term_embeddings]
        return search_results_list



    @metrics_tracker.track
    def create_collection(
        self,
        collection_name: str,
        vector_size: int = None,
        distance: Distance = None,
        vector_name: str = None,
        on_disk_payload: bool = None
    ) -> bool:
        return self.client.create_collection(
            collection_name=collection_name,
            vectors_config={
                (vector_name or CollectionConfig.VECTOR_NAME_SENTENCE_EMBEDDING): VectorParams(
                    size=vector_size or CollectionConfig.EMBEDDING_SIZE,
                    distance=distance or CollectionConfig.VECTOR_DISTANCE,
                    on_disk=False
                )
            },
            on_disk_payload=on_disk_payload if on_disk_payload is not None else CollectionConfig.ON_DISK_PAYLOAD
        )
    
    @metrics_tracker.track
    def delete_collection(self, collection_name: str) -> bool:
        return self.client.delete_collection(collection_name=collection_name)
    
    @metrics_tracker.track
    def collection_exists(self, collection_name: str) -> bool:
        return self.client.collection_exists(collection_name=collection_name)
    
    @metrics_tracker.track
    def get_collection_info(self, collection_name: str) -> Any:
        return self.client.get_collection(collection_name=collection_name)
    