from mcp.server import MCPServer
from mcp.server.mcpserver import Context
from mcp.server.mcpserver.exceptions import ResourceNotFoundError

from gulax_mcp.context import AppContext  # Bug en la version 2.0.0
from gulax_mcp.exceptions import KronosHTTPError
from gulax_mcp.models.collection import CollectionSummary
from gulax_mcp.models.document import DocumentSummary
from gulax_mcp.models.document_version import DocumentVersionSummary


async def get_document_resource(
    document_id: int,
    ctx: Context,
) -> DocumentSummary:
    """Read a document accessible to the current Gulax user."""

    app = ctx.request_context.lifespan_context

    try:
        result = await app.gulax.get_document(
            document_id=document_id,
            api_key=app.api_key.get_secret_value(),
        )
    except KronosHTTPError as exc:
        if exc.status_code == 404:
            raise ResourceNotFoundError(f"Document {document_id} does not exist") from exc

        raise

    return DocumentSummary(
        id=result.id,
        description=result.description,
        collection=CollectionSummary(
            id=result.collection.id,
            name=result.collection.gulax_name,
            description=result.collection.description,
            roles=result.collection.roles,
            created_at=result.collection.created_at,
            created_by=result.collection.created_by,
        ),
        created_at=result.created_at,
        created_by=result.created_by,
        updated_at=result.updated_at,
        updated_by=result.updated_by,
        deleted_at=result.deleted_at,
        deleted_by=result.deleted_by,
        versions=[
            DocumentVersionSummary(
                id=version.id,
                document_id=version.document_id,
                original_filename=version.original_filename,
                uploaded_by=version.uploaded_by,
                uploaded_at=version.uploaded_at,
                task_id=version.task_id,
                error_message=version.error_message,
                status=version.status,
            )
            for version in result.documents_versions
        ],
    )


def register_document_resources(server: MCPServer,) -> None:
    server.resource(
        "gulax://documents/{document_id}",
        name="document",
        title="Gulax document",
        description=(
            "Detailed information about a document "
            "accessible to the current Gulax user."
        ),
        mime_type="application/json",
    )(get_document_resource)

