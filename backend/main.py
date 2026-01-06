"""
Aplicación principal - FastAPI Backend
Sistema de Nómina Axyra Web
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api import auth, employees, hours, payroll, configuration

# Crear aplicación
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API para Sistema de Nómina Axyra",
    version=settings.VERSION,
    debug=settings.DEBUG,
    redirect_slashes=False
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router)
app.include_router(employees.router)
app.include_router(hours.router)
app.include_router(payroll.router)
app.include_router(configuration.router)


@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
