from abc import ABC, abstractmethod

class BaseMerger(ABC):
    @abstractmethod
    def merge(chunks: list[str]) -> list[str]:
        pass
