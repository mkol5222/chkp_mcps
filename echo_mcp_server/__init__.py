import re
from typing import List, TypedDict

import httpx
from fastmcp import FastMCP


class MCPServer(TypedDict):
    """Structure for MCP server information."""
    server_name: str
    package_name: str
    description: str


mcp = FastMCP("Echo Server")


@mcp.tool()
def echo(message: str) -> str:
    """Echo back the provided message.

    Args:
        message: The message to echo back

    Returns:
        The same message that was provided
    """
    return message


@mcp.tool()
def fetch_readme() -> str:
    """Fetch the README content from CheckPointSW/mcp-servers repository.

    Returns:
        The content of the README.md file as text
    """
    url = "https://raw.githubusercontent.com/CheckPointSW/mcp-servers/main/README.md"
    response = httpx.get(url)
    response.raise_for_status()
    return response.text


@mcp.tool()
def list_chkp_mcp_servers() -> List[MCPServer]:
    """List all CheckPoint MCP servers by parsing the README table.

    Fetches the README from CheckPointSW/mcp-servers repository and extracts
    server information from the markdown table.

    Returns:
        A list of MCP servers with server_name, package_name, and description
    """
    readme_content = fetch_readme()

    # Find the table in the markdown
    # Look for lines that start with | and contain server information
    servers = []

    # Split into lines and find table rows
    lines = readme_content.split('\n')
    in_table = False

    for line in lines:
        # Skip empty lines
        if not line.strip():
            continue

        # Check if this is a table row (starts and ends with |)
        if line.strip().startswith('|') and line.strip().endswith('|'):
            # Skip header row (contains "MCP Server")
            if 'MCP Server' in line and 'Package Name' in line:
                in_table = True
                continue

            # Skip separator row (contains dashes)
            if in_table and '---' in line:
                continue

            # Parse data rows
            if in_table:
                # Split by | and clean up
                parts = [p.strip() for p in line.split('|')]
                # Remove empty first and last elements (from leading/trailing |)
                parts = [p for p in parts if p]

                if len(parts) >= 3:
                    # Extract server name from markdown link [Name](url)
                    server_cell = parts[0]
                    match = re.search(r'\[([^\]]+)\]', server_cell)
                    server_name = match.group(1) if match else server_cell

                    # Extract package name (remove backticks)
                    package_name = parts[1].strip('`')

                    # Description is the third column
                    description = parts[2]

                    servers.append(MCPServer(
                        server_name=server_name,
                        package_name=package_name,
                        description=description
                    ))
        elif in_table and not line.strip().startswith('|'):
            # End of table
            break

    return servers


if __name__ == "__main__":
    mcp.run()
