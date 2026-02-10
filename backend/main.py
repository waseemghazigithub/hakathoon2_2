"""
FastAPI application entry point for Task Management API.

Implements FR-001 (FastAPI application structure) and FR-012 (CORS configuration).
"""
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from db import dispose_engine, create_db_and_tables
from routes.tasks import router as tasks_router
from routes.auth import router as auth_router
from routes.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifespan context manager for application startup and shutdown.

    Handles:
    - Startup: (No special startup actions needed for now)
    - Shutdown: Dispose database engine and close connections

    Note: Database tables are created via Alembic migrations, not on startup.
    """
    # Startup
    await create_db_and_tables()
    print(f"🚀 Starting Task Management API (Environment: {settings.environment})")
    print(f"📊 Database: Connected")
    print(f"🔒 Authentication: JWT with Better Auth")
    print(f"🌐 CORS: Allowing {settings.frontend_url}")

    yield

    # Shutdown
    print("🛑 Shutting down Task Management API")
    await dispose_engine()
    print("✅ Database connections closed")


# Initialize FastAPI application
app = FastAPI(
    title="Task Management API",
    version="1.0.0",
    description="Secure task management with JWT authentication and user data isolation",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Test route to verify docs update
@app.get("/api/test-docs", tags=["Admin"])
async def test_docs():
    return {"message": "Docs are working"}

# Register routes
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(chat_router)


# Configure CORS middleware (FR-012)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Temporarily allow all for debugging docs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global exception handler for HTTPException (T019)
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Standardize HTTPException responses with consistent error format.

    Error format (FR-008):
    {
        "detail": "Human-readable error message",
        "status_code": 400,
        "error_type": "validation_error"
    }
    """
    error_type_map = {
        400: "validation_error",
        401: "authentication_error",
        403: "authorization_error",
        404: "not_found_error",
        500: "internal_server_error",
    }

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "error_type": error_type_map.get(exc.status_code, "error"),
        },
    )


# Validation exception handler for RequestValidationError (T020)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Standardize validation error responses with detailed error information.

    Returns 400 Bad Request with validation details for frontend consumption.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Validation error",
            "status_code": 400,
            "error_type": "validation_error",
            "errors": exc.errors(),  # Detailed validation errors from Pydantic
        },
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.

    Returns 200 OK if application is running.
    """
    return {
        "status": "healthy",
        "environment": settings.environment,
        "version": "1.0.0",
    }


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint with API information.

    Redirects users to interactive API documentation at /docs.
    """
    return {
        "message": "Task Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Routes registered above
