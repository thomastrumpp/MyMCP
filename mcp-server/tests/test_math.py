import pytest
import math
from server import mcp, add, subtract, multiply, divide, square, sqrt, factorial

# We can import the tool functions directly because they are decorated Python functions
# FastMCP decorators usually preserve the underlying function call, but let's verify logic directly.

def test_add():
    assert add(1, 2) == 3
    assert add(-1, -1) == -2

def test_subtract():
    assert subtract(10, 5) == 5
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(0, 100) == 0

def test_divide():
    assert divide(10, 2) == 5.0
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

def test_square():
    assert square(5) == 25
    assert square(-4) == 16

def test_sqrt():
    assert sqrt(16) == 4.0
    with pytest.raises(ValueError, match="Cannot calculate square root of a negative number"):
        sqrt(-1)

def test_factorial():
    assert factorial(5) == 120
    assert factorial(0) == 1
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial(-1)
