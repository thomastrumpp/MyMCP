import pytest

from mcp_server.server import add, calculate_sin, divide, factorial, multiply, sqrt, square, subtract


def test_add() -> None:
    assert add(1, 2) == 3

def test_subtract() -> None:
    assert subtract(5, 3) == 2

def test_multiply() -> None:
    assert multiply(2, 3) == 6

def test_divide() -> None:
    assert divide(6, 2) == 3
    with pytest.raises(ValueError):
        divide(1, 0)

def test_square() -> None:
    assert square(4) == 16

def test_sqrt() -> None:
    assert sqrt(16) == 4
    with pytest.raises(ValueError):
        sqrt(-1)

def test_factorial() -> None:
    assert factorial(5) == 120
    with pytest.raises(ValueError):
        factorial(-1)

def test_calculate_sin() -> None:
    assert calculate_sin(0) == 0
    import math
    assert calculate_sin(math.pi / 2) == 1
