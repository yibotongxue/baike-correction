from typing import Any

from .base import BaseMerger

def get_merger(merger_cfgs: dict[str, Any]) -> BaseMerger:
    merger_type = merger_cfgs.pop('merger_type')
    if merger_type == 'semantics':
        embedding_cfgs = merger_cfgs.pop('embedding_cfgs')
        from .semantics import SemanticsMerger
        from ..embedding import get_embedding
        return SemanticsMerger(get_embedding(embedding_cfgs), **merger_cfgs)
    else:
        raise ValueError(f"Merger type {merger_type} is not supported")
