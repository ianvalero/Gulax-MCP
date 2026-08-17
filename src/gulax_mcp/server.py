from importlib.metadata import version

from mcp.server import MCPServer

from gulax_mcp.lifespan import app_lifespan
from gulax_mcp.prompts.collections import register_collection_prompts
from gulax_mcp.resources.collections import register_collection_resources
from gulax_mcp.resources.document_versions import register_document_version_resources
from gulax_mcp.resources.documents import register_document_resources
from gulax_mcp.tools.collections import register_collection_tools


def create_server() -> MCPServer:
    server = MCPServer(
        "Gulax",
        title="Gulax MCP",
        description="MCP server for interacting with the Gulax API",
        instructions=(
            "This server provides an interface to the Gulax API for managing collections "
            "and other resources."
        ),
        version=version("gulax-mcp"),
        lifespan=app_lifespan,
    )

    register_collection_tools(server)

    register_collection_resources(server)
    register_document_resources(server)
    register_document_version_resources(server)

    register_collection_prompts(server)

    return server


mcp = create_server()


if __name__ == "__main__":
    mcp.run()
