from fastapi import FastAPI

from app.database import Base, engine
from app import models
from app.routers.projects import router as projects_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Project Submission API",
    description="API for submitting, searching and moderating projects",
    version="1.0.0"
)


# Register project routes
app.include_router(projects_router)


@app.get("/")
def home():
    return {
        "message": "Project Submission API is running successfully"
    }