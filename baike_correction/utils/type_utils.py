from typing import Any

from pydantic import BaseModel

class KeyWordExtractorResult(BaseModel):
    key_word: str
    meta_data: dict[str, Any]
