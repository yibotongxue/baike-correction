from typing import override
from warnings import warn

from google import genai
from google.genai import types

from .base import BaseEmbedding
from .embedding_registry import register_embedding


@register_embedding("gemini")
class GeminiEmbedding(BaseEmbedding):
    MODEL_NAMES: set[str] = {
        "gemini-embedding-exp-03-07",
        "text-embedding-004",
        "embedding-001",
    }

    def __init__(
        self,
        api_key: str,
        model_name: str = "gemini-embedding-exp-03-07",
        dimension: int | None = None,
    ):
        if dimension:
            warn("The gemini doesn't support dimension")
        self.client = genai.Client(api_key=api_key)
        if model_name not in self.MODEL_NAMES:
            raise ValueError(
                f"All valid model names are {self.MODEL_NAMES}, and the input model name {model_name} is invalid"
            )
        self.model_name = model_name

    @override
    def embed(self, text: str) -> list[float]:
        result = self.client.models.embed_content(
            model=self.model_name,
            contents=text,
            config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY"),
        )
        return result.embeddings[0].values  # type: ignore [no-any-return]

    @property
    def dimension(self) -> int:
        return 768
