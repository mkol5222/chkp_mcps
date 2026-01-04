# Echo MCP Server

A simple FastMCP 2.0 based MCP server with a single echo tool.

## Installation

This project uses `uv` for Python project management.

```bash
# Install dependencies
uv sync
```

## Usage

Run the server:

```bash
# Using the CLI entry point
uv run echo-server

# Or directly with Python
uv run python -m echo_mcp_server
```

Run directly with uvx (no installation needed):

```bash
uvx --from . echo-server
```

## Tools

- **echo**: Echoes back the provided message
  - Arguments:
    - `message` (str): The message to echo back

- **fetch_readme**: Fetches the README content from CheckPointSW/mcp-servers repository
  - Arguments: None
  - Returns: The content of the README.md file as text
