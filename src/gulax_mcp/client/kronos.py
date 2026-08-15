from collections.abc import Mapping, Sequence
from typing import TypeVar

import httpx
from pydantic import BaseModel, ValidationError

from gulax_mcp.client.models.collection import GulaxCollectionDetailsDTO, GulaxCollectionPageDTO
from gulax_mcp.client.models.document import GulaxDocumentDTO
from gulax_mcp.client.models.document_version import GulaxDocumentVersionDetailsDTO
from gulax_mcp.exceptions import KronosHTTPError, KronosInvalidResponseError, KronosTransportError
from gulax_mcp.models.collection import CollectionListQuery

ModelT = TypeVar("ModelT", bound=BaseModel)

type QueryParamPrimitive = str | int | float | bool | None
type QueryParamValue = QueryParamPrimitive | Sequence[QueryParamPrimitive]
type QueryParams = Mapping[str, QueryParamValue]


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
    ) -> GulaxCollectionPageDTO:
        params = query.model_dump(mode="json", exclude_none=True)

        if not query.roles:
            params.pop("roles", None)

        return await self._get_model(
            "/api/collections/",
            params=params,
            api_key=api_key,
            response_model=GulaxCollectionPageDTO,
        )

    async def get_collection(
        self,
        *,
        collection_id: int,
        api_key: str,
    ) -> GulaxCollectionDetailsDTO:
        return await self._get_model(
            f"/api/collections/{collection_id}",
            api_key=api_key,
            response_model=GulaxCollectionDetailsDTO,
        )

    async def get_document(
        self,
        *,
        document_id: int,
        api_key: str,
    ) -> GulaxDocumentDTO:
        return await self._get_model(
            f"/api/documents/{document_id}",
            api_key=api_key,
            response_model=GulaxDocumentDTO,
        )

    async def get_document_version(
        self,
        *,
        document_id: int,
        document_version_id: int,
        api_key: str,
    ) -> GulaxDocumentVersionDetailsDTO:
        return await self._get_model(
            f"/api/documents/{document_id}/versions/{document_version_id}",
            api_key=api_key,
            response_model=GulaxDocumentVersionDetailsDTO,
        )

    async def _get_model(
        self,
        path: str,
        *,
        api_key: str,
        response_model: type[ModelT],
        params: QueryParams | None = None,
    ) -> ModelT:
        try:
            response = await self._http_client.get(
                path,
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
            return response_model.model_validate(response.json())
        except (ValueError, ValidationError) as exc:
            raise KronosInvalidResponseError("Kronos returned an invalid response") from exc