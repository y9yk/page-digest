import logging
from fastapi import APIRouter, Request

from src.app.common.base_schema import BaseResponse
from src.app.common.config import settings
from src.app.common.constant import QueryType
from src.app.modules.digest import DigestContentRequest, DigestContentService

from src.app.errors import NotImplementedException


logger = logging.getLogger(settings.PROJECT_NAME)
router = APIRouter(
    tags=["Digest"],
)


@router.post("/content")
async def get_digest_content(
    request: Request,
    digest_content_request: DigestContentRequest,
) -> BaseResponse:
    """
    get_digest_content
    """

    logger.debug(locals())

    # process
    results = await DigestContentService().get_content()
    return BaseResponse(results=results)
