from fastapi import APIRouter

from app.schemas.responses import PingResponse

router = APIRouter(tags=["root"])


@router.get("/")
def index():
    return {"Hello": "World"}


@router.get("/ping", response_model=PingResponse)
def ping():
    return PingResponse(ping="pong")
