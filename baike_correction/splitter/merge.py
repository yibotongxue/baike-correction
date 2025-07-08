from typing import override

from .base import BaseSplitter
from ..merger import BaseMerger

class MergeSplitter(BaseSplitter):
    def __init__(self, splitter: BaseSplitter, merger: BaseMerger):
        self.splitter = splitter
        self.merger = merger

    @override
    def split_text(self, text: str) -> list[str]:
        chunks = self.splitter.split_text(text)
        merged_chunks = self.merger.merge(chunks)
        return merged_chunks
