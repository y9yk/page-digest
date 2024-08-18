import logging
import time
from typing import Callable, List
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint


def _get_excluded_logging_urls() -> List[str]:
    return [
        "/docs",
        "/openapi.json",
    ]


class HttpRequestLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        *,
        logger: logging.Logger,
    ) -> None:
        self._logger = logger
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # setting uuid to request.state
        request.state.request_id = str(uuid4())

        # execution
        response: Response = await self._log_response(request, call_next)

        #
        return response

    async def _log_response(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        # information[request]
        request_id = str(request.state.request_id)
        method = request.method
        url = request.url
        ip = request.client.host

        # execution
        start_time = time.time() * 1000.0
        response: Response = await self._execute_request(request, call_next)
        execution_time = time.time() * 1000.0 - start_time

        # information[response]
        status_code = response.status_code
        user_agent = response.headers.get("user-agent", "")
        content_length = response.headers.get("content-length")

        # logging with excluded url path
        if request.url.path not in _get_excluded_logging_urls():
            # set project_id to base message on http request
            try:
                project_id = str(request.state.project_id)
            except:
                project_id = "global"
            message = f"{request_id}: {project_id} {method} {url} {status_code} {content_length} - {user_agent} {ip} - {execution_time:0.4f}ms"

            self._logger.info(message)

        #
        return response

    async def _execute_request(
        self,
        request: Request,
        call_next: Callable,
    ) -> Response:
        try:
            # execution
            response: Response = await call_next(request)

            #
            return response
        except Exception as e:
            self._logger.exception(
                {
                    "url": request.url,
                    "method": request.method,
                    "detail": str(e),
                }
            )
            # raise exception
            raise e
