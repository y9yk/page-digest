from pydantic import BaseModel, Field
from typing import Optional


class DigestContentRequest(BaseModel):
    url: str = Field(description="URL")
    model: Optional[str] = Field(default="gpt-4o-mini", description="OpenAI model name")
    max_tokens: Optional[int] = Field(description="Max tokens", example=2000, default=2000)
