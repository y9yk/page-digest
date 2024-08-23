from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.app.errors.exceptions import APIException, StatusCode


async def api_exception_handler(request: Request, exc: APIException):
    if isinstance(exc, APIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.code,
                "message": exc.message,
            },
        )
    return None


def _make_validation_exception_message(exc: RequestValidationError):
    if len(exc.errors()) > 0:
        error_dict = exc.errors()[0]
        if len(error_dict.get("loc")) > 0:
            message = (
                error_dict.get("msg", "")
                + " ("
                + str(list(error_dict.get("loc", ""))[1])
                + ":"
                + str(error_dict.get("input", ""))
                + ")"
            )
        else:
            message = error_dict.get("msg", "") + " (" + str(error_dict.get("input", "")) + ")"
        return message
    return "Type Error(Request)가 발생하였습니다."


async def validation_exception_handler(request, exc: RequestValidationError):
    if isinstance(exc, RequestValidationError):
        message = _make_validation_exception_message(exc)
        return JSONResponse(
            status_code=StatusCode.HTTP_422,
            content={"code": StatusCode.HTTP_422, "message": message},
        )
    return None


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=StatusCode.HTTP_500,
        content={
            "code": StatusCode.HTTP_500,
            "message": "API 서버에서 오류가 발생했습니다. 관리자에게 문의해주세요.",
            "detail": str(exc),
        },
    )
