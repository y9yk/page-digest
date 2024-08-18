import base64
from playwright.async_api import async_playwright


class ScreenCaptureProcessor(object):
    async def process(self, url: str):
        async with async_playwright() as client:
            webkit = client.webkit
            browser = await webkit.launch(headless=True)
            context = await browser.new_context()

            # create page
            page = await context.new_page()
            await page.goto(url=url)
            buffer = await page.screenshot(full_page=True)
            return base64.b64encode(buffer).decode()


screencapture_processor = ScreenCaptureProcessor()


def get_screencapture_processor() -> ScreenCaptureProcessor:
    return screencapture_processor
