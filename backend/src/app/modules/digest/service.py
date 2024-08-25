import logging

from src.app.common.config import settings
from src.app.modules.digest import DigestContentType
from src.app.clients.screencapture import ScreenCaptureProcessor, get_screencapture_processor
from src.app.clients.llm import LLM, PageDigestor


class DigestContentService(object):
    def __init__(self):
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def get_content(
        self,
        content: str,
        content_type: DigestContentType,
        model: str,
        max_tokens: int = 2000,
    ):
        # clients
        page_digestor: PageDigestor = PageDigestor(
            client=LLM(
                model=model,
                api_key=settings.OPENAI_API_KEY,
                max_tokens=max_tokens,
            )
        )

        # processing
        if content_type == DigestContentType.URL:
            screen_capture_processor: ScreenCaptureProcessor = get_screencapture_processor()
            base64_encoded_image_str = await screen_capture_processor.process(url=content)
            return await page_digestor.process(
                content=base64_encoded_image_str,
                content_type=DigestContentType.URL,
            )
        else:
            return await page_digestor.process(
                content=content,
                content_type=DigestContentType.TEXT,
            )
