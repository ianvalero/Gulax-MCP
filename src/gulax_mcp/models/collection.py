from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SortDirection(StrEnum):
    ASC = "asc"
    DESC = "desc"


class CollectionSortField(StrEnum):
    ID = "id"
    GULAX_NAME = "gulax_name"
    DESCRIPTION = "description"
    ROLES = "roles"
    CREATED_AT = "created_at"
    CREATED_BY = "created_by"

class CollectionListQuery(BaseModel):
    model_config = ConfigDict(extra="forbid")

    gulax_name: str | None = Field(
        default=None,
        description="Filter collections by their Kronos name.",
    )

    description: str | None = Field(
        default=None,
        description="Filter collections by description.",
    )

    roles: list[str] = Field(
        default_factory=list,
        description="Filter collections by allowed roles.",
    )

    created_by: str | None = Field(
        default=None,
        description="Filter collections by creator.",
    )

    created_at_from: datetime | None = Field(
        default=None,
        description=(
            "Return collections created at or after this timestamp."
        ),
    )

    created_at_to: datetime | None = Field(
        default=None,
        description=(
            "Return collections created at or before this timestamp."
        ),
    )

    offset: int = Field(
        default=0,
        ge=0,
        description="Number of matching collections to skip.",
    )

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Maximum number of collections to return.",
    )

    sort_by: CollectionSortField = Field(
        default=CollectionSortField.ID,
        description="Field used to order the collections.",
    )

    sort_order: SortDirection = Field(
        default=SortDirection.ASC,
        description="Sort direction.",
    )

    @model_validator(mode="after")
    def validate_created_at_range(self) -> "CollectionListQuery":
        if (
            self.created_at_from is not None
            and self.created_at_to is not None
            and self.created_at_from > self.created_at_to
        ):
            raise ValueError("created_at_from must be before or equal to created_at_to")

        return self


class CollectionSummary(BaseModel):
    id: int
    name: str
    description: str | None
    roles: list[str]
    created_at: datetime
    created_by: str

    @field_validator("created_at", mode="after")
    @classmethod
    def ensure_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)

        return value


class CollectionPage(BaseModel):
    items: list[CollectionSummary]

    total: int = Field(ge=0)
    limit: int = Field(ge=1)
    offset: int = Field(ge=0)

    has_next: bool
    has_prev: bool

class CollectionVectors(BaseModel):
    dimension: int | dict[str, int]
    distance: str | dict[str, str]


class CollectionDetails(CollectionSummary):
    status: str
    vectors: CollectionVectors | None

    updated_at: datetime | None
    updated_by: str | None