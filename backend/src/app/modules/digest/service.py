import logging

from src.app.common.config import settings
from src.app.clients.screencapture import ScreenCaptureProcessor, get_screencapture_processor
from src.app.clients.llm import LLM, PageDigestor


class DigestContentService(object):
    def __init__(self):
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def get_content(
        self,
        url: str,
        model: str,
        max_tokens: int = 2000,
    ):
        # clients
        screen_capture_processor: ScreenCaptureProcessor = get_screencapture_processor()
        page_digestor: PageDigestor = PageDigestor(
            client=LLM(
                model=model,
                api_key=settings.OPENAI_API_KEY,
                max_tokens=max_tokens,
            )
        )

        # processing and return
        base64_encoded_image_str = await screen_capture_processor.process(url=url)
        return await page_digestor.process(page_content=base64_encoded_image_str)
