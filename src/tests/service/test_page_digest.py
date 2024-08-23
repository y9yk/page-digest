import logging
import pytest

from src.app.common.config import settings

logger = logging.getLogger(settings.PROJECT_NAME)


@pytest.mark.asyncio
async def test_page_digest(
    client,
    get_request_header,
    pytestconfig,
):
    """
    data_grid_query
    """
    data = {
        "url": "https://medium.com/dlift/%EC%9E%90%EB%8F%99%EC%9C%BC%EB%A1%9C-%EC%B5%9C%EC%8B%A0-%EA%B8%B0%EC%88%A0-%EB%8F%99%ED%96%A5%EC%9D%84-%EC%A0%95%EB%A6%AC%ED%95%B4%EC%A3%BC%EB%8A%94-%EB%AF%B8%EB%94%94%EC%97%84-%EB%B8%94%EB%A1%9C%EA%B7%B8-%EB%A7%8C%EB%93%A4%EA%B8%B0-5a2585c2ded2",
        "model": "gpt-4o",
    }

    url = pytestconfig.getini("path_page_digest")
    async with client.stream(
        method="POST",
        url=url,
        headers=get_request_header,
        json=data,
    ) as response:
        assert response.status_code == 200

        content = ""
        async for chunk in response.aiter_lines():
            content += chunk

        logger.debug(content)
