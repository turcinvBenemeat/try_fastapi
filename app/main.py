from fastapi import FastAPI

from app.routers import hello, root

app = FastAPI(title="Try FastAPI", version="0.1.0")
app.include_router(root.router)
app.include_router(hello.router)
