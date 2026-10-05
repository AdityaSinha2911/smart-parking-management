from fastapi import FastAPI
import httpx


app = FastAPI(
    title="Smart Parking API Gateway",
    version="1.0.0"
)


USER_SERVICE = "http://user-service:8001"
PARKING_SERVICE = "http://parking-service:8002"
BOOKING_SERVICE = "http://booking-service:8003"


@app.get("/")
def root():
    return {
        "service": "api-gateway",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "api-gateway",
        "status": "healthy"
    }


@app.get("/users")
async def users():
    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{USER_SERVICE}/"
        )

        return response.json()


@app.get("/parking")
async def parking():
    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{PARKING_SERVICE}/"
        )

        return response.json()


@app.get("/bookings")
async def bookings():
    async with httpx.AsyncClient() as client:

        response = await client.get(
            f"{BOOKING_SERVICE}/"
        )

        return response.json()