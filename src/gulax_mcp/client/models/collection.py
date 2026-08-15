from datetime import datetime

from pydantic import BaseModel, ConfigDict

from gulax_mcp.client.models.pagination import GulaxPaginationDTO


class GulaxCollectionDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    gulax_name: str
    description: str | None
    roles: list[str]
    created_at: datetime
    created_by: str


class GulaxCollectionPageDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[GulaxCollectionDTO]
    pagination: GulaxPaginationDTO


class GulaxCollectionVectorsDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    dimension: int | dict[str, int]
    distance: str | dict[str, str]


class GulaxCollectionDetailsDTO(GulaxCollectionDTO):
    qdrant_name: str
    status: str
    vectors: GulaxCollectionVectorsDTO | None

    updated_at: datetime | None
    updated_by: str | None
    deleted_at: datetime | None
    deleted_by: str | None