import re
from typing import Any, Dict, List, TypedDict

import httpx
from fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPServer(TypedDict):
    """Structure for MCP server information."""
    server_name: str
    package_name: str
    description: str


class MCPTool(TypedDict):
    """Structure for MCP tool information."""
    name: str
    description: str
    inputSchema: Dict[str, Any]


class MCPPrompt(TypedDict):
    """Structure for MCP prompt information."""
    name: str
    description: str
    arguments: List[Dict[str, Any]]


mcp = FastMCP("CheckPoint MCP Servers Explorer")


# Helper functions (not exposed as tools)
def _fetch_readme_content() -> str:
    """Internal helper to fetch README content."""
    url = "https://raw.githubusercontent.com/CheckPointSW/mcp-servers/main/README.md"
    response = httpx.get(url)
    response.raise_for_status()
    return response.text


def _parse_mcp_servers_table(readme_content: str) -> List[MCPServer]:
    """Internal helper to parse the MCP servers table from README content."""
    servers = []
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


async def _get_mcp_server_tools(package_name: str) -> List[MCPTool]:
    """Internal async helper to connect to an MCP server and list its tools."""
    server_params = StdioServerParameters(
        command="npx",
        args=[package_name],
        env=None
    )

    tools_list = []

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List all available tools
            tools_response = await session.list_tools()

            for tool in tools_response.tools:
                tools_list.append(MCPTool(
                    name=tool.name,
                    description=tool.description or "",
                    inputSchema=tool.inputSchema
                ))

    return tools_list


async def _get_mcp_server_prompts(package_name: str) -> List[MCPPrompt]:
    """Internal async helper to connect to an MCP server and list its prompts."""
    server_params = StdioServerParameters(
        command="npx",
        args=[package_name],
        env=None
    )

    prompts_list = []

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List all available prompts
            prompts_response = await session.list_prompts()

            for prompt in prompts_response.prompts:
                prompts_list.append(MCPPrompt(
                    name=prompt.name,
                    description=prompt.description or "",
                    arguments=[
                        {
                            "name": arg.name,
                            "description": arg.description or "",
                            "required": arg.required
                        }
                        for arg in (prompt.arguments or [])
                    ]
                ))

    return prompts_list


# MCP Tools
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
    return _fetch_readme_content()


@mcp.tool()
def list_chkp_mcp_servers() -> List[MCPServer]:
    """List all CheckPoint MCP servers by parsing the README table.

    Fetches the README from CheckPointSW/mcp-servers repository and extracts
    server information from the markdown table.

    Returns:
        A list of MCP servers with server_name, package_name, and description
    """
    readme_content = _fetch_readme_content()
    return _parse_mcp_servers_table(readme_content)


@mcp.tool()
async def get_chkp_mcp_server_tools(package_name: str) -> List[MCPTool]:
    """Get all tools from a CheckPoint MCP server.

    Connects to the specified MCP server via stdio and retrieves all available
    tools with their metadata including name, description, and input schema.

    Args:
        package_name: The NPM package name of the MCP server (e.g., "@chkp/quantum-gw-cli-mcp")

    Returns:
        A list of tools with name, description, and inputSchema for each tool
    """
    return await _get_mcp_server_tools(package_name)


@mcp.tool()
async def get_chkp_mcp_server_prompts(package_name: str) -> List[MCPPrompt]:
    """Get all prompts from a CheckPoint MCP server.

    Connects to the specified MCP server via stdio and retrieves all available
    prompts with their metadata including name, description, and arguments.

    Args:
        package_name: The NPM package name of the MCP server (e.g., "@chkp/quantum-gw-cli-mcp")

    Returns:
        A list of prompts with name, description, and arguments for each prompt
    """
    return await _get_mcp_server_prompts(package_name)


if __name__ == "__main__":
    mcp.run()
