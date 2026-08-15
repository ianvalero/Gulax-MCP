from datetime import datetime

from pydantic import BaseModel, ConfigDict

from gulax_mcp.client.models.pagination import GulaxPaginationDTO


class GulaxDocumentVersionDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: int
    document_id: int
    filename: str
    original_filename: str
    uploaded_by: str
    uploaded_at: datetime
    task_id: str | None = None
    error_message: str | None
    status: str


class GulaxDocumentVersionPageDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    items: list[GulaxDocumentVersionDTO]
    pagination: GulaxPaginationDTO


class GulaxDocumentVersionDetailsDTO(GulaxDocumentVersionDTO):
    file_path: str
    file_size: int
    mime_type: str
    qdrant_point_ids: list[str] | None
    attempts: int