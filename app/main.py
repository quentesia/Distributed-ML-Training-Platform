from fastapi import FastAPI
import uvicorn

from app.config import settings
from app.database.connection import engine
from app.database.models import Base
from app.api import jobs

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Distributed ML Training Platform with Event-Driven Architecture"
)

app.include_router(jobs.router)

@app.get("/")
async def root():
    return {
        "message": "ML Training Pipeline API", 
        "status": "running",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=settings.debug)