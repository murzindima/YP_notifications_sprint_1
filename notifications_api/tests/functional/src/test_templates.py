from http import HTTPStatus

import pytest
from aiohttp import ClientSession

pytestmark = pytest.mark.asyncio
BOOKMARK_ID_TO_DELETE: str | None = None


async def test_get_templates_wo_auth(notifications_api_templates_url):
    async with ClientSession() as session:
        url = f"{notifications_api_templates_url}"

        async with session.get(url) as response:
            assert (
                response.status == HTTPStatus.UNAUTHORIZED
            ), f"API response status is not {HTTPStatus.UNAUTHORIZED}"
