from fastapi import FastAPI

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