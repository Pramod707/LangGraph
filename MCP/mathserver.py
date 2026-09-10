from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MATH")


@mcp.tool
def add(a: int, b: int):
    """_summary_
    Add two numbers
    """
    return a + b


@mcp.tool
def multiply(a: int, b: int):
    """_summary_
    multiply two numbers
    """
    return a * b


if __name__ == "__main__":
    mcp.run(transport="stdio")
