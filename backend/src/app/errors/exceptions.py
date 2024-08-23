from http import HTTPStatus


class StatusCode:
    HTTP_504 = HTTPStatus.GATEWAY_TIMEOUT.value
    HTTP_502 = HTTPStatus.BAD_GATEWAY.value
    HTTP_500 = HTTPStatus.INTERNAL_SERVER_ERROR.value
    HTTP_400 = HTTPStatus.BAD_REQUEST.value
    HTTP_401 = HTTPStatus.UNAUTHORIZED.value
    HTTP_402 = HTTPStatus.PAYMENT_REQUIRED.value
    HTTP_403 = HTTPStatus.FORBIDDEN.value
    HTTP_404 = HTTPStatus.NOT_FOUND.value
    HTTP_405 = HTTPStatus.METHOD_NOT_ALLOWED.value
    HTTP_422 = HTTPStatus.UNPROCESSABLE_ENTITY.value


class APIException(Exception):
    status_code: int
    code: str
    message: str
    detail: str
    ex: Exception

    def __init__(
        self,
        *,
        status_code: int = StatusCode.HTTP_500,
        code: str = None,
        message: str = None,
        detail: str = None,
        ex: Exception = None,
    ):
        self.status_code = status_code
        self.code = status_code if code is None else code
        self.message = message
        self.detail = detail
        self.ex = ex

        super().__init__(ex)


class UnAuthorizedException(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_401,
            message="인증되지 않은 사용자입니다.",
        )


class NotImplementedException(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_400,
            message="현재 지원하지 않는 요청 옵션을 포함하고 있습니다. 요청을 다시 확인해주세요.",
        )


class InternalServerException(APIException):
    def __init__(self):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            message="서버에서 오류가 발생했습니다. 관리자에게 문의해주세요.",
        )


class DatabaseEngineAlreadyClosedEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            message=f"DB 엔진이 이미 종료되었습니다. 서버에서 확인해주세요.",
            detail="",
            ex=ex,
        )


class SessionMakerIsNotInitializedEx(APIException):
    def __init__(self, ex: Exception = None):
        super().__init__(
            status_code=StatusCode.HTTP_500,
            message=f"DB 세션이 생성되지 않았습니다. 서버에서 확인해주세요.",
            detail="",
            ex=ex,
        )
