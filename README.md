# CheckPoint MCP Servers Explorer

MCP server for exploring and introspecting CheckPoint MCP servers. Provides tools to fetch server information, list available servers, and introspect their tools.

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
uv run chkp-mcp-servers-mcp-server

# Or directly with Python
uv run python -m chkp_mcp_servers
```

Run directly with uvx (no installation needed):

```bash
uvx --from . chkp-mcp-servers-mcp-server
```

## Claude Desktop Configuration

Add to your `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "chkp-mcp-servers": {
      "command": "/Users/YOUR_USERNAME/.local/bin/uv",
      "args": [
        "--directory",
        "/path/to/chkp_mcps",
        "run",
        "chkp-mcp-servers-mcp-server"
      ]
    }
  }
}
```

Replace `/path/to/chkp_mcps` with the absolute path to this project directory.

**Note**: Use the full path to `uv` (find it with `which uv`) because Claude Desktop doesn't inherit your shell's PATH.

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
