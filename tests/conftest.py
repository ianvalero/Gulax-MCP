import pytest


@pytest.fixture
def kronos_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(
        "KRONOS_MCP_API_BASE_URL",
        "https://example.com",
    )
    monkeypatch.setenv(
        "KRONOS_MCP_API_KEY",
        "test-api-key",
    )