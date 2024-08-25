from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class BaseEnum(str, Enum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value


class DigestContentType(BaseEnum):
    URL = "url"
    TEXT = "text"


class DigestContentRequest(BaseModel):
    content: str = Field(description="URL or Text")
    content_type: DigestContentType = Field(description="Content-Type", default=DigestContentType.TEXT)
    model: Optional[str] = Field(default="gpt-4o-mini", description="OpenAI model name")
    max_tokens: Optional[int] = Field(description="Max tokens", example=2000, default=2000)
