from abc import ABC, abstractmethod

from ..utils.type_utils import KeyWordExtractorResult

class BaseKeyWordExtractor(ABC):
    @abstractmethod
    def extract_key_words(self, text: str) -> list[KeyWordExtractorResult]:
        pass
