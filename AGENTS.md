# gulax-agent — AI Agent Instructions

## Project Overview

**gulax-agent** is an MCP (Model Context Protocol) server built with [`mcp[cli]>=2.0.0`](https://modelcontextprotocol.io). It exposes tools and capabilities to AI agents over the MCP protocol. The project is in active scaffolding — core implementations (server, client, models, tools) are being developed.

## Setup

```bash
uv sync          # install dependencies into .venv
```

- Python ≥ 3.13 (enforced via `.python-version`)
- Package manager: **uv**

## Run & Test

```bash
python main.py          # entry point
pytest tests/           # run test suite
pytest --cov=src tests/ # run with coverage
```

## Architecture

```
src/gulax_mcp/
  server.py        # MCP server — asyncio, registers tools/resources
  client.py        # MCP client — used for testing or external connections
  config.py        # configuration (env vars, settings)
  excepcions.py    # custom exception classes
  models/          # Pydantic models / request+response schemas
  tools/           # MCP tool implementations (one module per tool group)
```

Each tool in `tools/` should be registered with the MCP server in `server.py`. Follow the async/await pattern throughout — all I/O is async.

## Conventions

- **Formatter/Linter**: Ruff (`ruff check` / `ruff format`)
  - Line length: 100 chars
  - Quotes: double (`"`)
  - Rules: E, F, I, B, UP, SIM
- **Testing**: pytest + pytest-asyncio; use `@pytest.mark.asyncio` for async tests
- **Exception file**: `excepcions.py` (intentional spelling — do not rename)
- **Package layout**: `src/` layout; import as `from gulax_mcp.xxx import ...`

## Key Patterns

- Register new tools in `tools/` then import and attach them in `server.py`
- Use models from `models/` for structured input/output validation
- Raise custom exceptions from `excepcions.py` rather than built-in exceptions where domain errors apply
