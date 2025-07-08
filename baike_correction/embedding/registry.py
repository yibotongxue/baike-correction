from .base import BaseEmbedding

EMBEDDING_REGISTRY: dict[str, type[BaseEmbedding]] = {}


def register_embedding(embedding_type: str):
    def decorator(cls):
        EMBEDDING_REGISTRY[embedding_type] = cls
        return cls

    return decorator
