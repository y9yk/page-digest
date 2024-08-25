import logging

from src.app.common.config import settings
from src.app.clients.llm import LLM
from src.app.modules.digest import DigestContentType


class PageDigestor(object):
    def __init__(self, client: LLM):
        self.client = client
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def process(
        self,
        content: str,
        content_type: DigestContentType,
    ):
        try:
            messages = [
                {
                    "role": "system",
                    "content": "웹 페이지의 텍스트를 해석하고 요약하는 Web-Page Summarizer",
                }
            ]

            # construct messages
            if content_type == DigestContentType.URL:
                prompt = "이미지를 텍스트로 변환하고, 요약해서 Markdown 형태로 표현해줘"
                messages.append(
                    {
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{prompt}"},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{content}"}},
                            ],
                        },
                    }
                )
            else:
                prompt = f"content: {content}\n\n위의 content를 해석하고 요약해서 Markdown 형태로 표현해줘"
                messages.append(
                    {
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": f"{prompt}"},
                            ],
                        },
                    }
                )

            return self.client.get_chat_response(messages=messages)
        except Exception as e:
            self.logger.error(f"Error in page-digest: {e}")
