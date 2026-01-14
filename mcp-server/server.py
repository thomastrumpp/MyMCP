from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("MathTools")

@mcp.tool()
def add(a: float, b: float) -> float:
    """Adds two numbers together."""
    return a + b

@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtracts the second number from the first."""
    return a - b

@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiplies two numbers."""
    return a * b

@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divides a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Expose the ASGI app for uvicorn
# We use 'sse' transport to make it compatible with standard MCP clients connecting via SSE
app = mcp.http_app(transport='sse')

if __name__ == "__main__":
    # This allows running the server directly with: python server.py
    # Although typically FastMCP is run via 'fastmcp run server.py' or 'uvicorn server:mcp'
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
