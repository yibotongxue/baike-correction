from typing import override

import numpy as np

from .base import BaseMerger
from ..embedding import BaseEmbedding

class SemanticsMerger(BaseMerger):
    def __init__(self, embedding: BaseEmbedding, threshold: float = 0.3):
        self.embedding = embedding
        self.threshold = threshold

    @override
    def merge(self, chunks: list[str]) -> list[str]:
        chunk_embeddings = self.embedding.embed_batch(chunks)
        embedding_matrix = np.array(chunk_embeddings)
        embedding_norm: np.ndarray = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        embedding_matrix /= embedding_norm
        scores = np.sum(embedding_matrix[:-1] * embedding_matrix[1:], axis=1)
        print(scores)
        result = [chunks[0]]
        for i in range(1, len(chunks)):
            if scores[i - 1] < self.threshold:
                result.append(chunks[i])
            else:
                result[-1] += chunks[i]
        return result
