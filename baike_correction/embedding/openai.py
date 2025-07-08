from typing import override

from openai import OpenAI

from .base import BaseEmbedding
from .embedding_registry import register_embedding


@register_embedding("openai")
class OpenAIEmbedding(BaseEmbedding):
    MODEL_NAMES_TO_DIMENSIONS: dict[str, int] = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
    }

    def __init__(
        self,
        api_key: str,
        model_name: str = "text-embedding-3-small",
        dimension: int | None = None,
    ):
        if not model_name in self.MODEL_NAMES_TO_DIMENSIONS:
            raise ValueError(
                f"All valid model names are {self.MODEL_NAMES_TO_DIMENSIONS.keys()}, and the input model name {model_name} is invalid"
            )
        if not isinstance(dimension, int | None):
            app_logger.error(
                f"The type of dimension should be int or None, but actually is {type(dimension).__name__}"
            )
            raise TypeError(
                f"The type of dimension should be int or None, but actually is {type(dimension).__name__}"
            )
        if not dimension is None and dimension < 256:
            raise ValueError(
                f"The dimension of embedding should be at least 256, which is {dimension} now"
            )
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self._dimension = dimension

    @override
    def embed(self, text: str) -> list[float]:
        response = self.client.embeddings.create(input=text, model=self.model_name)
        if self._dimension is None:
            return response.data[0].embedding  # type: ignore [no-any-return]
        return response.data[0].embedding[: self._dimension]  # type: ignore [no-any-return]

    @override
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        response = self.client.embeddings.create(input=texts, model=self.model_name)
        return [
            (
                d.embedding[: self._dimension]
                if self._dimension
                else d.embedding
            )
            for d in response.data
        ]

    @property
    def dimension(self) -> int:
        if self._dimension is not None:
            return self._dimension
        return self.MODEL_NAMES_TO_DIMENSIONS[self.model_name]
