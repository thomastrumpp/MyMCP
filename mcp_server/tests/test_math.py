
import pytest
from server import add, divide, factorial, multiply, sqrt, square, subtract

# We can import the tool functions directly because they are decorated Python functions
# FastMCP decorators usually preserve the underlying function call, but let's verify logic directly.

def test_add():
    assert add.fn(1, 2) == 3
    assert add.fn(-1, -1) == -2

def test_subtract():
    assert subtract.fn(10, 5) == 5
    assert subtract.fn(0, 5) == -5

def test_multiply():
    assert multiply.fn(3, 4) == 12
    assert multiply.fn(0, 100) == 0

def test_divide():
    assert divide.fn(10, 2) == 5.0
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide.fn(10, 0)

def test_square():
    assert square.fn(5) == 25
    assert square.fn(-4) == 16

def test_sqrt():
    assert sqrt.fn(16) == 4.0
    with pytest.raises(ValueError, match="Cannot calculate square root of a negative number"):
        sqrt.fn(-1)

def test_factorial():
    assert factorial.fn(5) == 120
    assert factorial.fn(0) == 1
    with pytest.raises(ValueError, match="Factorial is not defined for negative numbers"):
        factorial.fn(-1)
