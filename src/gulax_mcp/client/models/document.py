from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from gulax_mcp.client.models.collection import GulaxCollectionDTO
from gulax_mcp.client.models.document_version import GulaxDocumentVersionDTO
from gulax_mcp.client.models.pagination import GulaxPaginationDTO


class GulaxDocumentDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    description: str
    collection: GulaxCollectionDTO
    created_at: datetime
    created_by: str
    updated_at: datetime | None = None
    updated_by: str | None = None
    deleted_at: datetime | None = None
    deleted_by: str | None = None

    documents_versions: list[GulaxDocumentVersionDTO] = Field(default_factory=list)


class GulaxDocumentPageDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[GulaxDocumentDTO]
    pagination: GulaxPaginationDTO