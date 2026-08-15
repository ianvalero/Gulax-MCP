from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.types import ToolAnnotations

from gulax_mcp.context import AppContext
from gulax_mcp.models.collection import CollectionListQuery, CollectionPage, CollectionSummary


async def list_collections(query: CollectionListQuery, ctx: Context[AppContext]) -> CollectionPage:
    """List Gulax collections accessible to the current user.

    Use this tool to discover collections or filter them by name,
    description, roles, creator, or creation date. Results can be
    sorted and paginated.
    """

    app = ctx.request_context.lifespan_context

    result = await app.gulax.list_collections(
        query=query,
        api_key=app.api_key.get_secret_value(),
    )

    return CollectionPage(
        items=[
            CollectionSummary(
                id=item.id,
                name=item.gulax_name,
                description=item.description,
                roles=item.roles,
                created_at=item.created_at,
                created_by=item.created_by,
            )
            for item in result.items
        ],
        total=result.pagination.total,
        limit=result.pagination.limit,
        offset=result.pagination.offset,
        has_next=result.pagination.has_next,
        has_prev=result.pagination.has_prev,
    )


def register_collection_tools(server: MCPServer) -> None:
    server.add_tool(
        list_collections,
        title="List Gulax collections",
        annotations=ToolAnnotations(
            read_only_hint=True,
            open_world_hint=False,
        ),
        structured_output=True,
    )