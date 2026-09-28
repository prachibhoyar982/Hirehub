from fastapi import FastAPI

from app.routers import applications
from app.routers import job
from app.routers.user import router as user_router

from app.database.database import Base, engine

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="HireHub API",
    description="A job portal backend API built with FastAPI and PostgreSQL",
    version="1.0.0"
)


app.include_router(job.router)
app.include_router(user_router)
app.include_router(applications.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "HireHub API is running"
    }