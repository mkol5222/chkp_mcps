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

- **list_chkp_mcp_servers**: Lists all CheckPoint MCP servers from the repository
  - Arguments: None
  - Returns: A structured list of MCP servers with:
    - `server_name`: Name of the server
    - `package_name`: NPM package name
    - `description`: Server description

- **get_chkp_mcp_server_tools**: Gets all tools from a CheckPoint MCP server
  - Arguments:
    - `package_name` (str): The NPM package name (e.g., "@chkp/quantum-gw-cli-mcp")
  - Returns: A list of tools with:
    - `name`: Tool name
    - `description`: Tool description
    - `inputSchema`: JSON schema for the tool's input parameters
