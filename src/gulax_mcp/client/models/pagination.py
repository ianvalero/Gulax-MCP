from pydantic import BaseModel, ConfigDict


class GulaxPaginationDTO(BaseModel):
    model_config = ConfigDict(extra="ignore")

    offset: int
    limit: int
    total: int
    has_next: bool
    has_prev: bool
