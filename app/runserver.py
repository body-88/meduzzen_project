import uvicorn

from app.core.config import settings


def run_uvicorn_server():
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=True,
    )
    
if __name__ == "__main__":
    run_uvicorn_server()