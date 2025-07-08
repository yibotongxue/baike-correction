import os
from typing import Any

from .base import BaseEmbedding
from .embedding_registry import EMBEDDING_REGISTRY


def get_embedding(embedding_cfgs: dict[str, Any]) -> BaseEmbedding:

    embedding_type: str = embedding_cfgs.pop("embedding_type")
    if embedding_type not in EMBEDDING_REGISTRY:
        raise ValueError(f"The embedding type {embedding_type} is not supported")
    if "api_key_name" in embedding_cfgs:
        api_key_name: str = embedding_cfgs.pop("api_key_name")
        api_key = os.environ.get(api_key_name)
        if api_key is None:
            raise ValueError(f"The {api_key_name} is not set")
        embedding_cfgs["api_key"] = api_key
    return EMBEDDING_REGISTRY[embedding_type](**embedding_cfgs)
