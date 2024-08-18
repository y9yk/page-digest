from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware

from src.app.common.config import settings
from src.app.errors import (
    APIException,
    api_exception_handler,
    global_exception_handler,
    validation_exception_handler,
)
from src.app.modules.api import api_router


# create application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESC,
    docs_url="/doc",
    openapi_url="/openapi.json",
)

# register middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(APIException, api_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# register router (APIs)
app.include_router(
    api_router,
    prefix=settings.API_PREFIX,
)
