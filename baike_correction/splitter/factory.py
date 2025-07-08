from typing import Any

from .base import BaseSplitter

def get_splitter(splitter_cfgs: dict[str, Any]) -> BaseSplitter:
    splitter_type = splitter_cfgs.pop('splitter_type')
    if splitter_type == 'sentence':
        from .sentence import SentenceSplitter
        return SentenceSplitter(**splitter_cfgs)
    if splitter_type == 'merge':
        from .merge import MergeSplitter
        from ..merger import get_merger
        inner_splitter_cfgs = splitter_cfgs.get('inner_splitter_cfgs')
        inner_splitter = get_splitter(inner_splitter_cfgs)
        merger_cfgs = splitter_cfgs.get('merger_cfgs')
        merger = get_merger(merger_cfgs)
        return MergeSplitter(inner_splitter, merger)
    raise ValueError(f"Splitter type {splitter_type} is not supported")
