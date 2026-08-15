from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

from gulax_mcp.context import AppContext  # Bug en la version 2.0.0
from gulax_mcp.exceptions import KronosHTTPError
from gulax_mcp.models.collection import (
    CollectionDetails,
    CollectionVectors,
)


async def get_collection_resource(
    collection_id: int,
    ctx: Context,
) -> CollectionDetails:
    """Read a collection accessible to the current Gulax user."""

    app = ctx.request_context.lifespan_context

    try:
        result = await app.gulax.get_collection(    # type: ignore
            collection_id=collection_id,
            api_key=app.api_key.get_secret_value(), # type: ignore
        )
    except KronosHTTPError as exc:
        if exc.status_code == 404:
            raise ResourceNotFoundError(f"Collection {collection_id} does not exist") from exc

        raise

    return CollectionDetails(
        id=result.id,
        name=result.gulax_name,
        description=result.description,
        roles=result.roles,
        created_at=result.created_at,
        created_by=result.created_by,
        status=result.status,
        vectors=CollectionVectors(
            dimension=result.vectors.dimension,
            distance=result.vectors.distance,
        ),
        updated_at=result.updated_at,
        updated_by=result.updated_by,
    )

def register_collection_resources(server: MCPServer,) -> None:
    server.resource(
        "gulax://collections/{collection_id}",
        name="collection",
        title="Gulax collection",
        description=(
            "Detailed information about a collection "
            "accessible to the current Gulax user."
        ),
        mime_type="application/json",
    )(get_collection_resource)