from fastapi import FastAPI, HTTPException

from app.calculator import add, divide, multiply, subtract

app = FastAPI(title="Hello Agent API")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello, Agent!"}


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/calculator/add")
async def add_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": add(a, b)}


@app.get("/api/calculator/subtract")
async def subtract_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": subtract(a, b)}


@app.get("/api/calculator/multiply")
async def multiply_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": multiply(a, b)}


@app.get("/api/calculator/divide")
async def divide_numbers(a: float, b: float) -> dict[str, float]:
    try:
        result = divide(a, b)
    except ZeroDivisionError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    return {"result": result}
