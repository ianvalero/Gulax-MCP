from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

from gulax_mcp.context import AppContext  # Bug en la version 2.0.0
from gulax_mcp.exceptions import KronosHTTPError
from gulax_mcp.models.document_version import DocumentVersionDetails


async def get_document_version_resource(
    document_id: int,
    document_version_id: int,
    ctx: Context,
) -> DocumentVersionDetails:
    """Read a document version accessible to the current Gulax user."""

    app = ctx.request_context.lifespan_context

    try:
        result = await app.gulax.get_document_version(    # type: ignore
            document_id=document_id,
            document_version_id=document_version_id,
            api_key=app.api_key.get_secret_value(), # type: ignore
        )
    except KronosHTTPError as exc:
        if exc.status_code == 404:
            raise ResourceNotFoundError(
                f"Document version {document_version_id} does not exist"
            ) from exc

        raise

    return DocumentVersionDetails(
        id=result.id,
        document_id=result.document_id,
        filename=result.filename,
        original_filename=result.original_filename,
        uploaded_by=result.uploaded_by,
        uploaded_at=result.uploaded_at,
        task_id=result.task_id,
        error_message=result.error_message,
        status=result.status,
        file_path=result.file_path,
        file_size=result.file_size,
        mime_type=result.mime_type,
        qdrant_point_ids=result.qdrant_point_ids,
        attempts=result.attempts,
    )


def register_documents_version_resources(server: MCPServer,) -> None:
    server.resource(
        "gulax://documents/{document_id}/versions/{document_version_id}",
        name="document_version",
        title="Gulax document version",
        description=(
            "Detailed information about a document version "
            "accessible to the current Gulax user."
        ),
        mime_type="application/json",
    )(get_document_version_resource)

