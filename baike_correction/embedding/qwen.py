from typing import override
from warnings import warn

from openai import OpenAI

from .base import BaseEmbedding
from .embedding_registry import register_embedding


@register_embedding("qwen")
class QwenEmbedding(BaseEmbedding):
    MODEL_NAMES_TO_DIMENSIONS: dict[str, int] = {
        "text-embedding-v4": 1024,
        "text-embedding-v3": 1024,
        "text-embedding-v2": 1536,
        "text-embedding-v1": 1536,
    }

    ALLOWED_DIMENSIONS_DICT: dict[str, list[int]] = {
        "text-embedding-v4": [2048, 1536, 1024, 768, 512, 256, 128, 64],
        "text-embedding-v3": [1024, 768, 512, 256, 128, 64],
    }

    BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    def __init__(
        self,
        api_key: str,
        model_name: str = "text-embedding-v3",
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
        self._dimension = None
        if dimension is not None:
            if not model_name in self.ALLOWED_DIMENSIONS_DICT:
                warn(
                    f"The model {model_name} doesn't support the dimension choice, it will be ignored"
                )
            elif not dimension in self.ALLOWED_DIMENSIONS_DICT[model_name]:
                warn(
                    f"The dimension {dimension} is not in the supported dimension list {self.ALLOWED_DIMENSIONS_DICT[model_name]} of model {model_name}, it will be ignored"
                )
            else:
                self._dimension = dimension
        self.client = OpenAI(api_key=api_key, base_url=self.BASE_URL)
        self.model_name = model_name

    @override
    def embed(self, text: str) -> list[float]:
        if self._dimension is not None:
            response = self.client.embeddings.create(
                input=text, model=self.model_name, dimensions=self._dimension
            )
        else:
            response = self.client.embeddings.create(
                input=text,
                model=self.model_name,
            )
        return response.data[0].embedding[: self._dimension]  # type: ignore [no-any-return]

    @override
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        if self._dimension is not None:
            response = self.client.embeddings.create(
                input=texts, model=self.model_name, dimensions=self._dimension
            )
        else:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model_name,
            )
        return [d.embedding for d in response.data]

    @property
    def dimension(self) -> int:
        if self._dimension is not None:
            return self._dimension
        return self.MODEL_NAMES_TO_DIMENSIONS[self.model_name]
