from typing import override

from .base import BaseSplitter

class SentenceSplitter(BaseSplitter):
    def __init__(self, sep: list[str] = None):
        if sep is None:
            sep = ['。', '？', '！']
        self.sep = sep

    @override
    def split_text(self, text: str) -> list[str]:
        n = len(text)
        if n == 0:
            return []
        i = 0
        start = 0
        sentences = []
        while i < n:
            matched = False
            for s in self.sep:
                s_len = len(s)
                if i + s_len <= n and text[i:i+s_len] == s:
                    sentence = text[start:i + s_len]
                    sentences.append(sentence)
                    i += s_len
                    start = i
                    matched = True
                    break
            if matched:
                continue
            i += 1
        if start < n:
            sentences.append(text[start:])
        return sentences
