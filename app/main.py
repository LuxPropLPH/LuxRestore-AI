from fastapi import FastAPI
from app.api.routes import router
from app.config.logger import setup_logging

setup_logging()

app = FastAPI(
    title="LuxRestore-AI",
    description="API for LuxRestore-AI",
    version="0.1.0"
)

app.include_router(router)

@app.get("/")
def read_root() -> dict[str, str]:
    return {
        "project": "LuxRestore-AI",
        "version": "0.1.0"
    }

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}
