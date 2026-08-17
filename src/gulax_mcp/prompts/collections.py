from typing import Annotated

from mcp.server import MCPServer
from pydantic import Field


def explore_gulax_prompt(
    topic: Annotated[str, Field(description="Topic or subject to explore in Gulax.")],
) -> str:
    """Guide an exploration of Gulax for a specific topic."""

    return (
        "Help me find the Gulax collections most relevant "
        f"to this topic: {topic!r}. "
        "Use the available Gulax capabilities to identify "
        "relevant collections. Explain which collections "
        "appear useful and why. Do not invent collections "
        "or document contents that have not been retrieved."
        "Respond in the language used by the user. "
        "If that cannot be determined reliably, use the "
        "language of the supplied topic."
    )

def register_collection_prompts(server: MCPServer) -> None:
    server.prompt(
        "explore_gulax",
        title="Explore Gulax",
        description=("Find Gulax collection relevant to a topic."),
    )(explore_gulax_prompt)