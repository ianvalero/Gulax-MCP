import httpx
import pytest

from gulax_mcp.client.kronos import KronosClient
from gulax_mcp.exceptions import KronosHTTPError, KronosInvalidResponseError
from gulax_mcp.models.collection import CollectionListQuery, CollectionSortField, SortDirection


@pytest.mark.anyio
async def test_list_collections() -> None:
    def handler(
        request: httpx.Request,
    ) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/api/collections/"

        assert request.headers["X-Api-Key"] == "test-api-key"
        assert request.url.params["sort_by"] == "created_at"
        assert request.url.params["sort_order"] == "desc"
        assert request.url.params.get_list("roles") == [
            "admin",
            "developer",
        ]
        
        return httpx.Response(
            status_code=200,
            json={
                "items": [
                    {
                        "id": 1,
                        "gulax_name": "Engineering",
                        "description": (
                            "Engineering documentation"
                        ),
                        "roles": [
                            "admin",
                            "developer",
                        ],
                        "created_at": (
                            "2026-08-13T10:00:00Z"
                        ),
                        "created_by": "ian",
                    }
                ],
                "pagination": {
                    "offset": 0,
                    "limit": 10,
                    "total": 1,
                    "has_next": False,
                    "has_prev": False,
                },
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport, base_url="http://kronos.test") as http_client:
        client = KronosClient(http_client=http_client)

        result = await client.list_collections(
            query=CollectionListQuery(
                roles=["admin", "developer"],
                limit=10,
                sort_by=CollectionSortField.CREATED_AT,
                sort_order=SortDirection.DESC,
            ),
            api_key="test-api-key",
        )

    assert result.pagination.total == 1
    assert result.items[0].gulax_name == "Engineering"


@pytest.mark.anyio
async def test_list_collections_rejects_invalid_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={
                "items": [
                    {
                        "id": 1,
                    }
                ],
                "pagination": {
                    "offset": 0,
                    "limit": 20,
                    "total": 1,
                    "has_next": False,
                    "has_prev": False,
                },
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport, base_url="http://kronos.test") as http_client:
        client = KronosClient(http_client=http_client)

        with pytest.raises(KronosInvalidResponseError):
            await client.list_collections(
                query=CollectionListQuery(),
                api_key="test-api-key",
            )


@pytest.mark.anyio
async def test_list_collections_handles_unauthorized() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=401,
            json={
                "detail": "Invalid API key",
            },
        )

    transport = httpx.MockTransport(handler)

    async with httpx.AsyncClient(transport=transport, base_url="http://kronos.test") as http_client:
        client = KronosClient(http_client=http_client,)

        with pytest.raises(KronosHTTPError) as exc_info:
            await client.list_collections(
                query=CollectionListQuery(),
                api_key="invalid",
            )

    assert exc_info.value.status_code == 401