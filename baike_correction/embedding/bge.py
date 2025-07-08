from typing import override

import torch
from transformers import AutoModel, AutoTokenizer

from .base import BaseEmbedding
from .embedding_registry import register_embedding

@register_embedding("bge")
class BGEEmbedding(BaseEmbedding):
    def __init__(self, 
                 model_name, 
                 *,
                 device: str = None,
                 normalize_embeddings: bool = True,
                 max_length: int = 512,
                 max_batch_size: int = 8):
        """
        使用 BGE 模型的嵌入实现
        
        参数:
        model_name: BGE 模型名称或路径
        device: 使用的设备 (None 为自动选择, 'cuda', 'cpu')
        normalize_embeddings: 是否归一化嵌入向量
        max_length: 模型最大输入长度
        max_batch_size: 最大的批量大小
        """
        self.model_name = model_name
        self.normalize_embeddings = normalize_embeddings
        self.max_length = max_length
        self.max_batch_size = max_batch_size

        # 自动选择设备
        if device is None:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            self.device = device

        # 加载模型和tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()

        # 获取嵌入维度
        self._dimension = self.model.config.hidden_size

    @property
    def dimension(self) -> int:
        """返回嵌入向量的维度"""
        return self._dimension

    def _mean_pooling(self, model_output, attention_mask):
        """应用 mean pooling 获取句子嵌入"""
        token_embeddings = model_output[0]  # 第一个元素包含token嵌入
        input_mask_expanded = (
            attention_mask
            .unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    @override
    def embed(self, text: str) -> list[float]:
        """为单个文本生成嵌入向量"""
        return self.embed_batch([text])[0]

    @override
    def embed_batch(self, texts: list[str]) -> list[list[float]]:
        """为一批文本生成嵌入向量"""
        result: list[list[float]] = []
        for start_idx in range(0, len(texts), self.max_batch_size):
            end_idx = min(start_idx + self.max_batch_size, len(texts))
            batch = texts[start_idx:end_idx]
            # 对文本进行分词
            encoded_input = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt"
            ).to(self.device)

            # 计算嵌入
            with torch.no_grad():
                model_output = self.model(**encoded_input)

            # 应用 mean pooling
            sentence_embeddings = self._mean_pooling(
                model_output, encoded_input["attention_mask"]
            )

            # 归一化嵌入
            if self.normalize_embeddings:
                sentence_embeddings = torch.nn.functional.normalize(
                    sentence_embeddings, p=2, dim=1
                )

            # 转换为Python列表并移动到CPU
            result.extend(sentence_embeddings.cpu().numpy().tolist())
        return result
