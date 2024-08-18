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
    ):
        try:
            messages = [
                {
                    "role": "system",
                    "content": "",
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": ""},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{page_content}"}},
                    ],
                },
            ]

            return self.client.get_chat_response(messages=messages)
        except Exception as e:
            self.logger.error(f"Error in page-digest: {e}")
