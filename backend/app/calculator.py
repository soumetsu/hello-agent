"""Framework-free arithmetic operations for Hello Agent."""

Number = int | float


def add(left: Number, right: Number) -> Number:
    """Return the sum of two numbers."""
    return left + right


def subtract(left: Number, right: Number) -> Number:
    """Return the difference between two numbers."""
    return left - right


def multiply(left: Number, right: Number) -> Number:
    """Return the product of two numbers."""
    return left * right


def divide(left: Number, right: Number) -> float:
    """Return the quotient of two numbers.

    Raises:
        ZeroDivisionError: If the right operand is zero.
    """
    if right == 0:
        raise ZeroDivisionError("Cannot divide by zero.")

    return left / right
