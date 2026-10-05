from fastapi import FastAPI

app = FastAPI(
    title="User Service",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "service": "user-service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "user-service",
        "status": "healthy"
    }