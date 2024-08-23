import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from src.app.main import app


def pytest_addoption(parser):
    parser.addini("timeout", "")
    parser.addini("path_page_digest", "")


@pytest_asyncio.fixture(autouse=True)
async def client(pytestconfig):
    timeout = pytestconfig.getini("timeout")
    async with AsyncClient(app=app, base_url="http://test", timeout=timeout) as client, LifespanManager(app):
        yield client


@pytest.fixture(autouse=True)
def get_request_header(pytestconfig):
    return {
        "Content-Type": "application/json",
    }
