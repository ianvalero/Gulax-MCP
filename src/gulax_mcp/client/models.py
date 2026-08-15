from datetime import datetime

from pydantic import BaseModel, ConfigDict


class KronosPaginationDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    offset: int
    limit: int
    total: int
    has_next: bool
    has_prev: bool


class KronosCollectionDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    gulax_name: str
    description: str | None
    roles: list[str]
    created_at: datetime
    created_by: str


class KronosCollectionPageDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[KronosCollectionDTO]
    pagination: KronosPaginationDTO


class KronosCollectionVectorsDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    dimension: int | dict[str, int]
    distance: str | dict[str, str]


class KronosCollectionDetailsDTO(KronosCollectionDTO):
    qdrant_name: str
    status: str
    vectors: KronosCollectionVectorsDTO | None

    updated_at: datetime | None
    updated_by: str | None
    deleted_at: datetime | None
    deleted_by: str | None