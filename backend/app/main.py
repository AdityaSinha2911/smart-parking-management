from fastapi import FastAPI
from sqlalchemy import text

from app.database.connection import engine


app = FastAPI(
    title="Smart Parking Management System",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Smart Parking API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

# Check the health of the database
@app.get("/health/db")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar()
    }