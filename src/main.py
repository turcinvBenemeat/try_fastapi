from fastapi import FastAPI
import uvicorn

# These will be your future imports as the project grows:
# from src.web import api_router
# from src.db import database
# from src.service import business_logic

def create_app() -> FastAPI:
    """
    Application factory to initialize the FastAPI instance.
    """
    application = FastAPI(
        title="FastAPI Project Template",
        description="A structured project using a clean architecture (src/ layout).",
        version="1.0.0"
    )

    @application.get("/", tags=["Health"])
    async def root():
        """
        Root endpoint to check if the API is running.
        """
        return {
            "status": "online",
            "message": "FastAPI server is running correctly.",
            "docs": "/docs"
        }

    # This is where you will register routers from src/web/ later
    # application.include_router(api_router)

    return application

app = create_app()

if __name__ == "__main__":
    # Note: Using "main:app" assumes execution from within the 'src' directory.
    # For global execution, use: uvicorn src.main:app --reload
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )