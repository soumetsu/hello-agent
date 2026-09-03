import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.mark.parametrize(
    ("path", "a", "b", "expected"),
    [
        ("add", 2, 3, 5),
        ("subtract", 7, 4, 3),
        ("multiply", 6, 5, 30),
        ("divide", 9, 4, 2.25),
    ],
)
def test_calculator_path(
    path: str,
    a: float,
    b: float,
    expected: float,
) -> None:
    response = client.get(f"/api/calculator/{path}", params={"a": a, "b": b})

    assert response.status_code == 200
    assert response.json() == {"result": expected}


def test_division_by_zero_returns_client_error() -> None:
    response = client.get("/api/calculator/divide", params={"a": 10, "b": 0})

    assert response.status_code == 400
    assert response.json() == {"detail": "Cannot divide by zero."}


def test_query_parameters_must_be_numeric() -> None:
    response = client.get(
        "/api/calculator/add",
        params={"a": "not-a-number", "b": 2},
    )

    assert response.status_code == 422
