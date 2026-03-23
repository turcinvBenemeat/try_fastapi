from fastapi import APIRouter

router = APIRouter(tags=["hello"])


@router.get("/hi")
def greet():
    return "Hello? World?"


@router.get("/hi/{name}")
def greet_by_name(name: str):
    return f"Hello? {name}?"


@router.get("/hello")
def hello_query(name: str):
    return f"Hello, {name}?"
