from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")


@mcp.tool
async def weather(location: str) -> str:
    """get the weather of the location"""
    return "its sunny always in the hyderabad"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
