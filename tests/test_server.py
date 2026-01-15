from mcp_server.server import add, subtract, multiply, divide, square, sqrt, factorial, calculate_sin
import pytest

def test_add():
    assert add(1, 2) == 3

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(2, 3) == 6

def test_divide():
    assert divide(6, 2) == 3
    with pytest.raises(ValueError):
        divide(1, 0)

def test_square():
    assert square(4) == 16

def test_sqrt():
    assert sqrt(16) == 4
    with pytest.raises(ValueError):
        sqrt(-1)

def test_factorial():
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-1)

def test_calculate_sin():
    assert calculate_sin(0) == 0
    import math
    assert calculate_sin(math.pi / 2) == 1
