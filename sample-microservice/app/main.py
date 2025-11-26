from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import os
import uuid
import time
from typing import Optional

# Application startup time for uptime calculation
STARTUP_TIME = time.time()

app = FastAPI(
    title="Sample Microservice",
    description="A production-ready FastAPI service for CI/CD demo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

class HealthResponse(BaseModel):
    status: str = Field(..., example="healthy")
    version: str = Field(..., example="1.0.0")
    service_id: str = Field(..., example="a1b2c3d4")
    timestamp: str = Field(..., example="2024-01-01T00:00:00Z")

class EchoRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000, example="Hello World")

class EchoResponse(BaseModel):
    echo: str = Field(..., example="You said: Hello World")
    timestamp: str = Field(..., example="2024-01-01T00:00:00Z")
    request_id: str = Field(..., example="req_12345")

class ServiceInfoResponse(BaseModel):
    service: str = Field(..., example="sample-microservice")
    version: str = Field(..., example="1.0.0")
    environment: str = Field(..., example="production")
    service_id: str = Field(..., example="a1b2c3d4")
    uptime_seconds: float = Field(..., example=3600.5)

# Generate a unique service ID on startup
SERVICE_ID = str(uuid.uuid4())[:8]

@app.get("/", summary="Root endpoint", response_description="Welcome message")
async def root():
    """Root endpoint returning welcome message"""
    return {
        "message": "Welcome to Sample Microservice API",
        "service_id": SERVICE_ID,
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check():
    """Health check endpoint for load balancers and monitoring"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        service_id=SERVICE_ID,
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )

@app.post("/echo", response_model=EchoResponse, summary="Echo service", status_code=status.HTTP_200_OK)
async def echo_message(request: EchoRequest):
    """Echo back the provided message with metadata"""
    return EchoResponse(
        echo=f"You said: {request.message}",
        timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        request_id=str(uuid.uuid4())[:8]
    )

@app.get("/info", response_model=ServiceInfoResponse, summary="Service information")
async def service_info():
    """Service information and metadata"""
    return ServiceInfoResponse(
        service="sample-microservice",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development"),
        service_id=SERVICE_ID,
        uptime_seconds=time.time() - STARTUP_TIME
    )

@app.get("/metrics", summary="Basic metrics")
async def metrics():
    """Basic application metrics (would be expanded in production)"""
    return {
        "requests_served": 0,  # In production, this would be tracked
        "uptime_seconds": time.time() - STARTUP_TIME,
        "service_id": SERVICE_ID
    }

# Custom exception handlers
@app.exception_handler(500)
async def internal_server_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": str(uuid.uuid4())[:8]}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_config=None  # Use uvicorn's default logging
    )