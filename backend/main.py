"""
Aplicación principal - FastAPI Backend
Sistema de Nómina Axyra Web
Production Ready
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api import auth, employees, hours, payroll, configuration

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API para Sistema de Nómina Axyra - Production Ready",
    version="1.0.0",
    debug=settings.DEBUG,
    redirect_slashes=False,
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS con políticas más estrictas en producción
cors_origins = settings.ALLOWED_ORIGINS if isinstance(settings.ALLOWED_ORIGINS, list) else [settings.ALLOWED_ORIGINS]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)

# Incluir routers
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(employees.router, prefix="/api", tags=["employees"])
app.include_router(hours.router, prefix="/api", tags=["hours"])
app.include_router(payroll.router, prefix="/api", tags=["payroll"])
app.include_router(configuration.router, prefix="/api", tags=["configuration"])

logger.info(f"Starting {settings.APP_NAME} - Version 1.0.0")

@app.get("/")
async def root():
    """Endpoint raíz - API Status"""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "running",
        "environment": "production" if not settings.DEBUG else "development",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "service": settings.APP_NAME
    }

@app.get("/api/status")
async def api_status():
    """Detailed API status"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "endpoints": {
            "auth": "/api/auth",
            "employees": "/api/employees",
            "hours": "/api/hours",
            "payroll": "/api/payroll",
            "configuration": "/api/configuration"
        }
    }

@app.on_event("startup")
async def startup_event():
    """Eventos de inicio"""
    logger.info(f"{settings.APP_NAME} iniciada correctamente")

@app.on_event("shutdown")
async def shutdown_event():
    """Eventos de cierre"""
    logger.info(f"{settings.APP_NAME} cerrada")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )
