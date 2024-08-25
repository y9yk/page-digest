import logging
from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from src.app.common.config import settings
from src.app.common.base_schema import BaseResponse
from src.app.modules.digest import DigestContentRequest, DigestContentService


logger = logging.getLogger(settings.PROJECT_NAME)
router = APIRouter(
    tags=["Digest"],
)


@router.post("/content")
async def get_digest_content(
    request: Request,
    digest_content_request: DigestContentRequest,
):
    """
    get_digest_content
    """

    logger.debug(locals())

    # processing
    results = await DigestContentService().get_content(**digest_content_request.model_dump())
    return StreamingResponse(
        results,
        media_type="text/event-stream",
    )
