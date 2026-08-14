import httpx
from pydantic import ValidationError

from gulax_mcp.client.models import KronosCollectionPageDTO
from gulax_mcp.exceptions import KronosHTTPError, KronosInvalidResponseError, KronosTransportError
from gulax_mcp.models.collection import CollectionListQuery


class KronosClient:
    """Async client for the Kronos REST API.

    The underlying HTTP client is injected and owned by the caller.
    KronosClient must not close it.
    """

    def __init__(self, http_client: httpx.AsyncClient) -> None:
        self._http_client = http_client

    async def list_collections(
        self,
        *,
        query: CollectionListQuery,
        api_key: str,
    ) -> KronosCollectionPageDTO:
        params = query.model_dump(mode="json", exclude_none=True)

        if not query.roles:
            params.pop("roles", None)

        try:
            response = await self._http_client.get(
                "/api/collections/",
                params=params,
                headers={
                    "X-Api-Key": api_key,
                },
            )
        except httpx.TimeoutException as exc:
            raise KronosTransportError("Kronos API request timed out") from exc
        except httpx.RequestError as exc:
            raise KronosTransportError("Could not communicate with the Kronos API") from exc

        if response.status_code >= 400:
            raise KronosHTTPError(status_code=response.status_code)

        try:
            payload = response.json()
            return KronosCollectionPageDTO.model_validate(payload)
        except (ValueError, ValidationError) as exc:
            raise KronosInvalidResponseError(
                "Kronos returned an invalid collections response"
            ) from exc