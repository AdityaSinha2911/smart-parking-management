from fastapi import FastAPI

app = FastAPI(
    title="Parking Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "parking-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "parking-service",
        "status": "healthy"
    }