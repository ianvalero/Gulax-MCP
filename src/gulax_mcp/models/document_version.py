from datetime import datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class DocumentVersionStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    ARCHIVED = "ARCHIVED"


class DocumentVersionListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    filename: str | None = Field(
        default=None,
        description="Filter document versions by their filename.",
    )

    status: DocumentVersionStatus | None = Field(
        default=None,
        description="Filter document versions by their status.",
    )

    upload_by: str | None = Field(
        default=None,
        description="Filter document versions by uploader.",
    )

    upload_at_from: datetime | None = Field(
        default=None,
        description=(
            "Return document versions uploaded at or after this timestamp."
        ),
    )

    upload_at_to: datetime | None = Field(
        default=None,
        description=(
            "Return document versions uploaded at or before this timestamp."
        ),
    )
    
    @model_validator(mode="after")
    def validate_upload_at_range(self) -> "DocumentVersionListQuery":
        if (
            self.upload_at_from is not None
            and self.upload_at_to is not None
            and self.upload_at_from > self.upload_at_to
        ):
            raise ValueError("upload_at_from must be before or equal to upload_at_to")

        return self


class DocumentVersionSummary(BaseModel):
    id: int
    document_id: int
    filename: str
    original_filename: str
    uploaded_by: str
    uploaded_at: datetime
    task_id: str | None = None
    error_message: str | None
    status: DocumentVersionStatus


class DocumentVersionPage(BaseModel):
    items: list[DocumentVersionSummary]

    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)

    has_next: bool
    has_prev: bool


class DocumentVersionDetails(DocumentVersionSummary):
    file_path: str
    file_size: int
    mime_type: str
    qdrant_point_ids: list[str] | None
    attempts: int


class DocumentVersionTaskSummary(BaseModel):
    task_id: str
    status: str
    result: Any | None = None


