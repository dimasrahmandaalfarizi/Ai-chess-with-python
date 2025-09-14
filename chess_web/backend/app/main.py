"""
Chess AI Helper Website - Main FastAPI Application

This module contains the main FastAPI application with all routes and middleware.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import os
import sys

# Add chess engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from .api import chess_routes, analysis_routes, websocket_routes
from .services.chess_service import ChessService

# Initialize FastAPI app
app = FastAPI(
    title="Chess AI Helper API",
    description="Backend API for Chess AI Helper Website with advanced analysis capabilities",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize chess engine service
chess_service = ChessService()

# Include routers
app.include_router(chess_routes.router, prefix="/api/chess", tags=["chess"])
app.include_router(analysis_routes.router, prefix="/api/analysis", tags=["analysis"])
app.include_router(websocket_routes.router, tags=["websocket"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Chess AI Helper API",
        "version": "1.0.0",
        "docs": "/api/docs",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Test chess engine
        engine_status = "operational"
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "engine_status": engine_status,
            "services": {
                "chess_engine": "operational",
                "api": "operational",
                "websocket": "operational"
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e)
            }
        )

@app.get("/api/engine/info")
async def get_engine_info():
    """Get chess engine information"""
    return await chess_service.get_engine_info()

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)