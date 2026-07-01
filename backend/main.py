from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import practice, dashboard
from contextlib import asynccontextmanager

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production backend for PrepPal AI Capstone",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc UI
)

# Standard CORS configuration for future frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registering modular routers
app.include_router(practice.router, prefix="/practice", tags=["Practice"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}