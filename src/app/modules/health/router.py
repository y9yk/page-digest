from fastapi import APIRouter

from src.app.common.base_schema import BaseResponse

router = APIRouter(
    tags=["Health"],
)


@router.get(
    "",
    response_model=BaseResponse,
    response_model_exclude_none=True,
)
async def get_health():
    """
    Support to readiness API
    """
    return BaseResponse(results=None)
