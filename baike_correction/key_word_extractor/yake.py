from typing import override, Any
from warnings import warn

import yake
import jieba

from .base import BaseKeyWordExtractor
from ..utils.type_utils import KeyWordExtractorResult

class YakeKeyWordExtractor(BaseKeyWordExtractor):
    def __init__(self, extractor_cfgs: dict[str, Any]):
        self.kw_extractor = yake.KeywordExtractor(**extractor_cfgs)
        self.extractor_cfgs = extractor_cfgs
        self.lan = extractor_cfgs.get("lan", "en")

    @override
    def extract_key_words(self, text: str) -> list[KeyWordExtractorResult]:
        if self.lan == "zh":
            text = " ".join(jieba.cut(text))
        keywords = self.kw_extractor.extract_keywords(text)
        if len(keywords) == 0:
            warn(f"extract key words from {text} got an empty list")
            return []
        if isinstance(keywords[0], str):
            return [KeyWordExtractorResult(key_word=key_word, meta_data={}) for key_word in keywords]
        elif isinstance(keywords[0], tuple):
            return [KeyWordExtractorResult(key_word=key_word, meta_data={"yake_score": score}) for key_word, score in keywords]
        else:
            raise TypeError(f"Unexpected type of keywords result {type(keywords[0]).__name__}")
