import math

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

@mcp.tool()
def square(a: float) -> float:
    """Squares a number."""
    return a * a

@mcp.tool()
def sqrt(a: float) -> float:
    """Calculates the square root of a number."""
    if a < 0:
        raise ValueError("Cannot calculate square root of a negative number")
    return math.sqrt(a)

@mcp.tool()
def factorial(n: int) -> int:
    """Calculates the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    return math.factorial(n)

@mcp.tool()
def calculate_sin(a: float) -> float:
    """Calculates the sine of a number."""
    return math.sin(a)


