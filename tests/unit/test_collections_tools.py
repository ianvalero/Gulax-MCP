import pytest
from mcp import Client

from gulax_mcp.server import create_server


@pytest.mark.anyio
async def test_list_collections_schema(kronos_env: None) -> None:
    server = create_server()

    async with Client(server) as client:
        result = await client.list_tools()

    tool = next(
        tool
        for tool in result.tools
        if tool.name == "list_collections"
    )

    assert tool.title == "List Kronos collections"
    assert tool.input_schema["type"] == "object"