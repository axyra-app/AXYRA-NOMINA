"""
[MAIN] APLICACIÓN PRINCIPAL - AXYRA NÓMINA
Backend profesional con FastAPI
Versión 2.1.0 - Production Ready
"""

import logging
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.logging_config import setup_logging
from app.api import auth, employees, hours, payroll, configuration
from app.middleware import (
    SecurityHeadersMiddleware,
    RequestLoggingMiddleware,
    RateLimitMiddleware,
    ErrorHandlingMiddleware,
    CORSValidationMiddleware
)
from app.exceptions import register_error_handlers
from app.database.firebase import get_firebase
from datetime import datetime

# Configurar logging PRIMERO
setup_logging()
logger = logging.getLogger(__name__)

# Información de inicio
logger.info("=" * 60)
logger.info(f"[STARTUP] {settings.APP_NAME} v{settings.VERSION}")
logger.info(f"[ENV] Environment: {settings.ENVIRONMENT}")
logger.info(f"[CONFIG] Debug: {settings.DEBUG}")
logger.info("=" * 60)

# ============ CREAR APLICACIÓN ============
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API profesional para Sistema de Nómina",
    version=settings.VERSION,
    debug=settings.DEBUG,
    redirect_slashes=False,
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============ CONFIGURAR MIDDLEWARE ============
logger.info("[SECURITY] Configuring security middleware...")

# Security Headers Middleware
app.add_middleware(SecurityHeadersMiddleware)

# CORS Middleware con configuración dinámica
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=["*"],
)

# Validation y otras capas
app.add_middleware(CORSValidationMiddleware)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(RequestLoggingMiddleware)

# ============ REGISTRAR EXCEPTION HANDLERS ============
logger.info("[HANDLERS] Registering exception handlers...")
register_error_handlers(app)

# ============ INCLUIR ROUTERS ============
logger.info("[ROUTERS] Including API routers...")
app.include_router(auth.router, prefix="")
app.include_router(employees.router, prefix="")
app.include_router(hours.router, prefix="")
app.include_router(payroll.router, prefix="")
app.include_router(configuration.router, prefix="")

logger.info(f"[OK] 5 routers included successfully")

# ============ EVENTOS DE APLICACIÓN ============
@app.on_event("startup")
async def startup_event():
    """Inicialización de la aplicación"""
    try:
        firebase = get_firebase()
        health = firebase.health_check()
        logger.info("[DB] Firebase connected successfully")
        logger.info(f"[OK] {settings.APP_NAME} started in {settings.ENVIRONMENT}")
    except Exception as e:
        logger.error(f"[ERROR] Startup error: {str(e)}")
        raise


@app.on_event("shutdown")
async def shutdown_event():
    """Cierre limpio de la aplicación"""
    logger.info(f"[SHUTDOWN] {settings.APP_NAME} closing...")


# ============ ENDPOINTS DE ESTADO ============
@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "endpoints": {
            "health": "/health",
            "status": "/api/status",
            "auth": "/api/auth",
            "employees": "/api/employees",
            "hours": "/api/hours",
            "payroll": "/api/payroll",
            "configuration": "/api/config",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check simple"""
    try:
        firebase = get_firebase()
        firebase_status = firebase.health_check()
        return {
            "status": "healthy",
            "service": settings.APP_NAME,
            "version": settings.VERSION,
            "timestamp": datetime.now().isoformat(),
            "firebase": "connected" if firebase_status else "disconnected"
        }
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


@app.get("/api/status")
async def api_status():
    """Status endpoint detallado del sistema"""
    try:
        firebase = get_firebase()
        firebase_health = firebase.health_check()
        
        return {
            "status": "operational",
            "timestamp": datetime.now().isoformat(),
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "services": {
                "firebase": "connected" if firebase_health else "disconnected",
                "cors": {
                    "enabled": True,
                    "origins_count": len(settings.ALLOWED_ORIGINS)
                },
                "rate_limiting": {
                    "enabled": settings.RATE_LIMIT_ENABLED,
                    "requests_limit": settings.RATE_LIMIT_REQUESTS
                },
                "logging": {
                    "level": settings.LOG_LEVEL,
                    "format": settings.LOG_FORMAT
                }
            },
            "features": {
                "jwt_authentication": "enabled",
                "request_logging": "enabled",
                "error_handling": "enabled",
                "batch_operations": "enabled",
                "pagination": "enabled"
            },
            "endpoints_available": 5
        }
    except Exception as e:
        logger.error(f"Status endpoint error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


# ============ RUN ============
if __name__ == "__main__":
    import uvicorn
    
    logger.info("[STARTUP] Starting uvicorn server...")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug",
        access_log=True
    )
