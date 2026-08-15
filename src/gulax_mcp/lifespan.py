from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from mcp.server import MCPServer

from gulax_mcp.client.kronos import KronosClient
from gulax_mcp.config import Settings
from gulax_mcp.context import AppContext


@asynccontextmanager
async def app_lifespan(server: MCPServer) -> AsyncIterator[AppContext]:
    settings = Settings() # pyright: ignore[reportCallIssue]

    timeout = httpx.Timeout(
        connect=settings.http_connect_timeout_s,
        read=settings.http_read_timeout_s,
        write=settings.http_write_timeout_s,
        pool=settings.http_pool_timeout_s,
    )

    limits = httpx.Limits(
        max_connections=settings.http_max_connections,
        max_keepalive_connections=settings.http_max_keepalive_connections
    )

    async with httpx.AsyncClient(
        base_url=str(settings.api_base_url),
        timeout=timeout,
        limits=limits,
        follow_redirects=False,
        headers={
            "Accept": "application/json",
            "User-Agent": "gulax-mcp/0.1.0",
        },
    ) as http_client:
        kronos_client = KronosClient(http_client=http_client)

        yield AppContext(gulax=kronos_client, api_key=settings.api_key)