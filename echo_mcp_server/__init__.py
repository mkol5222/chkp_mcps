import httpx
from fastmcp import FastMCP

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


if __name__ == "__main__":
    mcp.run()
