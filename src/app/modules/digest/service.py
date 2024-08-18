import logging

from src.app.common.config import settings


class DigestContentService(object):
    def __init__(self):
        self.logger = logging.getLogger(settings.PROJECT_NAME)

    async def get_content(self):
        return {}
