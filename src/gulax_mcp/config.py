from pydantic import Field, HttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="KRONOS_MCP_",
        dotenv_filtering="match_prefix",
        extra="forbid",
        frozen=True,
    )

    api_base_url: HttpUrl
    api_key: SecretStr

    http_connect_timeout_s: float = Field(default=5.0, gt=0)
    http_read_timeout_s: float = Field(default=15.0, gt=0)
    http_write_timeout_s: float = Field(default=15.0, gt=0)
    http_pool_timeout_s: float = Field(default=5.0, gt=0)

    http_max_connections: int = Field(default=50, ge=1)
    http_max_keepalive_connections: int = Field(default=20, ge=0)

    @field_validator("api_base_url")
    @classmethod
    def validate_api_base_url(cls, value: HttpUrl) -> HttpUrl:
        if value.path not in ("", "/"):
            raise ValueError(
                "api_base_url must not contain a path"
            )

        if value.query is not None:
            raise ValueError(
                "api_base_url must not contain query parameters"
            )

        if value.fragment is not None:
            raise ValueError(
                "api_base_url must not contain a fragment"
            )

        return value