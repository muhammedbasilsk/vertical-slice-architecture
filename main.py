"""FastAPI application with vertical slice architecture."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from shared.database import init_db
from features.users.endpoints import router as users_router
from features.orders.endpoints import router as orders_router

# Initialize database
init_db()

# Create FastAPI application
app = FastAPI(
    title="Vertical Slice Architecture API",
    description="A FastAPI application demonstrating vertical slice architecture with User and Order entities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to Vertical Slice Architecture API",
        "docs": "/api/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected"
    }


# Register feature routers
app.include_router(users_router, prefix=f"/api/{settings.api_version}")
app.include_router(orders_router, prefix=f"/api/{settings.api_version}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
