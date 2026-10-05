from fastapi import FastAPI

app = FastAPI(
    title="Booking Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "booking-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "booking-service",
        "status": "healthy"
    }