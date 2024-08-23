import base64
import logging
import time
from playwright.async_api import async_playwright

from src.app.common.config import settings


class ScreenCaptureProcessor(object):
    def __init__(self):
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def process(self, url: str):
        async with async_playwright() as client:
            webkit = client.webkit
            browser = await webkit.launch(headless=True)
            context = await browser.new_context()

            # create page
            page = await context.new_page()
            await page.goto(url=url)
            buffer = await page.screenshot(full_page=True, type="png")

            # return
            return base64.b64encode(buffer).decode("utf8")


screencapture_processor = ScreenCaptureProcessor()


def get_screencapture_processor() -> ScreenCaptureProcessor:
    return screencapture_processor
