from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from gulax_mcp.models.collection import CollectionSummary
from gulax_mcp.models.document_version import DocumentVersionSummary


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class DocumentSortField(StrEnum):
    ID = "id"
    COLLECTION_ID = "collection_id"
    COLLECTION_GULAX_NAME = "collection_gulax_name"
    DESCRIPTION = "description"
    COLLECTION_ROLES = "collection_roles"
    CREATED_AT = "created_at"
    CREATED_BY = "created_by"


class DocumentListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    collection_id: str | None = Field(
        default=None,
        description="Filter documents by their collection ID.",
    )

    description: str | None = Field(
        default=None,
        description="Filter documents by description.",
    )

    roles: list[str] = Field(
        default_factory=list,
        description="Filter documents by allowed roles.",
    )

    created_by: str | None = Field(
        default=None,
        description="Filter documents by creator.",
    )

    created_at_from: datetime | None = Field(
        default=None,
        description=(
            "Return documents created at or after this timestamp."
        ),
    )

    created_at_to: datetime | None = Field(
        default=None,
        description=(
            "Return documents created at or before this timestamp."
        ),
    )

    include_deleted: bool = Field(
        default=False,
        description="Include deleted documents in the results."
    )

    offset: int = Field(
        default=0,
        ge=0,
        description="Number of matching documents to skip.",
    )

    limit: int = Field(
        default=100,
        ge=1,
        description="Maximum number of matching documents to return.",
    )

    sort_by: DocumentSortField = Field(
        default=DocumentSortField.ID,
        description="Field used to order the documents.",
    )
    
    sort_order: SortDirection = Field(
        default=SortDirection.ASC,
        description="Sort direction.",
    )
    
    @model_validator(mode="after")
    def validate_created_at_range(self) -> "DocumentListQuery":
        if (
            self.created_at_from is not None
            and self.created_at_to is not None
            and self.created_at_from > self.created_at_to
        ):
            raise ValueError("created_at_from must be before or equal to created_at_to")

        return self


class DocumentSummary(BaseModel):
    id: int
    description: str
    collection: CollectionSummary
    created_at: datetime
    created_by: str
    updated_at: datetime | None
    updated_by: str | None
    deleted_at: datetime | None
    deleted_by: str | None

    documents_versions: list[DocumentVersionSummary] = list()


class DocumentPage(BaseModel):
    items: list[DocumentSummary]

    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)

    has_next: bool
    has_prev: bool