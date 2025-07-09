from typing import override

from .base import BaseMerger
from ..key_word_extractor import BaseKeyWordExtractor

class KeyWordsMerger(BaseMerger):
    def __init__(self, key_word_extractor: BaseKeyWordExtractor):
        self.key_word_extractor = key_word_extractor

    @override
    def merge(self, chunks: list[str]) -> list[str]:
        if len(chunks) == 0:
            return []
        result = [chunks[0]]
        prev_key_word = self.key_word_extractor.extract_key_words(chunks[0])[0].key_word
        for i in range(1, len(chunks)):
            key_words = self.key_word_extractor.extract_key_words(chunks[i])
            if len(key_words) == 0:
                result.append(chunks[i])
                continue
            key_word = key_words[0].key_word
            if prev_key_word == key_word:
                result[-1] += chunks[i]
            else:
                result.append(chunks[i])
            prev_key_word = key_word
        return result

