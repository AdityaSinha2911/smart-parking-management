from fastapi import FastAPI
from sqlalchemy import text

from app.database.base import Base
from app.database.connection import engine
from app.models import User, Vehicle, ParkingSlot, Booking
from app.routes.users import router as users_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Smart Parking Management System",
    version="1.0.0"
)

# Include the users router to handle user-related endpoints
app.include_router(users_router)


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


@app.get("/health/db")
def database_health():

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar()
    }