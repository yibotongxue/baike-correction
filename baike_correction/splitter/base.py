from abc import ABC, abstractmethod

class BaseSplitter(ABC):
    @abstractmethod
    def split_text(self, text: str) -> list[str]:
        pass
