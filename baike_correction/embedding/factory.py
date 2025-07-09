import os
from typing import Any

from .base import BaseEmbedding
from .registry import EMBEDDING_REGISTRY
from ..utils.tools import load_api_key


def get_embedding(embedding_cfgs: dict[str, Any]) -> BaseEmbedding:

    embedding_type: str = embedding_cfgs.pop("embedding_type")
    if embedding_type not in EMBEDDING_REGISTRY:
        raise ValueError(f"The embedding type {embedding_type} is not supported")
    embedding_cfgs = load_api_key(embedding_cfgs)
    return EMBEDDING_REGISTRY[embedding_type](**embedding_cfgs)
