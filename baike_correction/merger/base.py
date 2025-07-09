from abc import ABC, abstractmethod

class BaseMerger(ABC):
    @abstractmethod
    def merge(self, chunks: list[str]) -> list[str]:
        pass
