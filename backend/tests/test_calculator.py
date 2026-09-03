import pytest

from app.calculator import add, divide, multiply, subtract


def test_addition() -> None:
    assert add(2, 3) == 5


def test_addition_with_a_negative_value() -> None:
    assert add(-2, 3) == 1


def test_subtraction() -> None:
    assert subtract(7, 4) == 3


def test_multiplication() -> None:
    assert multiply(6, 5) == 30


def test_division() -> None:
    assert divide(9, 4) == 2.25


def test_division_by_zero() -> None:
    with pytest.raises(ZeroDivisionError, match="Cannot divide by zero"):
        divide(10, 0)
