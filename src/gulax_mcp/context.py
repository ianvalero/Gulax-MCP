from dataclasses import dataclass

from pydantic import SecretStr

from gulax_mcp.client.kronos import KronosClient


@dataclass(frozen=True, slots=True)
class AppContext:
    kronos: KronosClient
    api_key: SecretStr