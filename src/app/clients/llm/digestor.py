import logging

from src.app.common.config import settings
from src.app.clients.llm import LLM


class PageDigestor(object):
    def __init__(self, client: LLM):
        self.client = client
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def process(
        self,
        page_content: str,
        role: str = "이미지에 있는 텍스트를 추출하고 요약하는 Image2Text Transformer and Summarizer",
        prompt: str = "이미지에 있는 텍스트를 추출하고, 요약해줘",
    ):
        try:
            messages = [
                {
                    "role": "system",
                    "content": role,
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{prompt}"},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{page_content}"}},
                    ],
                },
            ]

            return self.client.get_chat_response(messages=messages)
        except Exception as e:
            self.logger.error(f"Error in page-digest: {e}")
