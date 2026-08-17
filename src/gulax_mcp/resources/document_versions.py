from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

from gulax_mcp.exceptions import KronosHTTPError
from gulax_mcp.models.document_version import DocumentVersionSummary


async def get_document_version_resource(
    document_id: int,
    document_version_id: int,
    ctx: Context,
) -> DocumentVersionSummary:
    """Read a document version accessible to the current Gulax user."""

    app = ctx.request_context.lifespan_context

    try:
        result = await app.gulax.get_document_version(
            document_id=document_id,
            document_version_id=document_version_id,
            api_key=app.api_key.get_secret_value(),
        )
    except KronosHTTPError as exc:
        if exc.status_code == 404:
            raise ResourceNotFoundError(
                f"Document version {document_version_id} does not exist"
            ) from exc

        raise

    return DocumentVersionSummary(
        id=result.id,
        document_id=result.document_id,
        original_filename=result.original_filename,
        uploaded_by=result.uploaded_by,
        uploaded_at=result.uploaded_at,
        task_id=result.task_id,
        error_message=result.error_message,
        status=result.status,
    )


def register_document_version_resources(server: MCPServer) -> None:
    server.resource(
        "gulax://documents/{document_id}/versions/{document_version_id}",
        name="document_version",
        title="Gulax document version",
        description=(
            "Detailed information about a document version accessible to the current Gulax user."
        ),
        mime_type="application/json",
    )(get_document_version_resource)
