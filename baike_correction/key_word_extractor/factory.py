from typing import Any

from .base import BaseKeyWordExtractor

def get_key_word_extractor(extractor_cfgs: dict[str, Any]) -> BaseKeyWordExtractor:
    extractor_type = extractor_cfgs.pop("extractor_type")
    if extractor_type == "yake":
        from .yake import YakeKeyWordExtractor
        return YakeKeyWordExtractor(extractor_cfgs=extractor_cfgs)
    else:
        raise ValueError(f"Unsupported extractor type {extractor_type}")
