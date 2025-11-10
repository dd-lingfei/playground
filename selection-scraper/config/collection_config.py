#!/usr/bin/env python3

from datetime import datetime
from typing import Dict
from qdrant_client.http.models import Distance, VectorParams, PayloadSchemaType


class CollectionConfig:
    # Collection naming
    COLLECTION_PREFIX = "selection"
    DATE_FORMAT = "%Y-%m-%d"
    
    # Vector configurations
    EMBEDDING_SIZE = 1536  # text-embedding-3-small dimension
    VECTOR_DISTANCE = Distance.COSINE
    VECTOR_NAME_SENTENCE_EMBEDDING = "sentence_embedding"
    
    # Qdrant connection settings
    QDRANT_HOST = "qdrant-catalog.svc.ddnw.net"
    QDRANT_GRPC_PORT = 50051
    QDRANT_HTTPS = False
    QDRANT_PREFER_GRPC = True
    QDRANT_TIMEOUT = 10
    
    # UUID namespace for generating deterministic IDs
    UUID_NAMESPACE = "7885d7d7-c909-457a-90f4-a1fdb82b1b4b"
    
    # Collection schema
    VECTOR_CONFIGS = {
        VECTOR_NAME_SENTENCE_EMBEDDING: VectorParams(size=EMBEDDING_SIZE, distance=VECTOR_DISTANCE),
        # Add more vector configs here as needed
        # "clip_sentence_embedding": VectorParams(size=768, distance=Distance.COSINE),
        # "clip_photo_embedding": VectorParams(size=768, distance=Distance.COSINE),
    }
    
    _INDEX_FIELDS = {
        "msid": PayloadSchemaType.KEYWORD,
        "photo_url": PayloadSchemaType.KEYWORD,
        "item_name": PayloadSchemaType.KEYWORD,
        "size": PayloadSchemaType.KEYWORD,
        "price_usd": PayloadSchemaType.KEYWORD
    }
    
    ON_DISK_PAYLOAD = True
    
    @classmethod
    def get_collection_name(cls, store_id: int) -> str:
        return f"{cls.COLLECTION_PREFIX}_{store_id}"
    
    @classmethod
    def get_grpc_options(cls) -> Dict[str, str]:
        return {
            "grpc.lb_policy_name": "round_robin",
            "grpc.service_config": '{"loadBalancingConfig":[{"round_robin":{}}]}'
        }
