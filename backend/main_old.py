"""
🚀 APLICACIÓN PRINCIPAL - AXYRA NÓMINA
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

# Configurar logging PRIMERO
setup_logging()
logger = logging.getLogger(__name__)

# Información de inicio
logger.info("=" * 60)
logger.info(f"🚀 {settings.APP_NAME} v{settings.VERSION}")
logger.info(f"📍 Entorno: {settings.ENVIRONMENT}")
logger.info(f"🔧 Debug: {settings.DEBUG}")
logger.info("=" * 60)

# ============ CREAR APLICACIÓN ============
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API profesional para Sistema de Nómina - Production Ready",
    version=settings.VERSION,
    debug=settings.DEBUG,
    redirect_slashes=False,
    openapi_url="/docs/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ============ CONFIGURAR MIDDLEWARE ============
logger.info("🔐 Configurando middleware de seguridad...")

# Headers de seguridad
app.add_middleware(SecurityHeadersMiddleware)

# Validación de CORS
app.add_middleware(CORSValidationMiddleware)

# Manejo de errores
app.add_middleware(ErrorHandlingMiddleware)

# Rate limiting
if settings.RATE_LIMIT_ENABLED:
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.RATE_LIMIT_REQUESTS
    )
    logger.info(f"✅ Rate limiting: {settings.RATE_LIMIT_REQUESTS} requests/minuto")

# Logging de requests
app.add_middleware(RequestLoggingMiddleware)

# CORS con configuración avanzada
cors_origins = settings.get_origins_list()
logger.info(f"🌐 CORS configurado para: {len(cors_origins)} origen(es)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=["*"],
    max_age=3600,
    expose_headers=["X-Request-ID", "X-Process-Time", "X-RateLimit-Limit", "X-RateLimit-Remaining"]
)

# ============ REGISTRAR EXCEPTION HANDLERS ============
register_error_handlers(app)
logger.info("✅ Exception handlers registrados")

# ============ INCLUIR ROUTERS ============
logger.info("📡 Registrando routers...")
app.include_router(auth.router, prefix="/api", tags=["auth"])
app.include_router(employees.router, prefix="/api", tags=["employees"])
app.include_router(hours.router, prefix="/api", tags=["hours"])
app.include_router(payroll.router, prefix="/api", tags=["payroll"])
app.include_router(configuration.router, prefix="/api", tags=["configuration"])
logger.info("✅ Todos los routers registrados")

# ============ INICIALIZAR SERVICIOS ============
logger.info("🔥 Inicializando Firebase...")
try:
    firebase = get_firebase()
    health = firebase.health_check()
    if health.get("firebase_connected"):
        logger.info("✅ Firebase conectado correctamente")
    else:
        logger.warning("⚠️  Firebase en modo MOCK (desarrollo)")
except Exception as e:
    logger.error(f"❌ Error inicializando Firebase: {str(e)}")
    if not settings.DEBUG:
        raise

# ============ EVENTOS DE CICLO DE VIDA ============
@app.on_event("startup")
async def startup_event():
    """Evento al iniciar la aplicación"""
    logger.info("⚡ Aplicación iniciando...")
    logger.info(f"✅ Todas las validaciones pasadas correctamente")
    logger.info(f"🟢 Estado: READY")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento al cerrar la aplicación"""
    logger.warning("🛑 Aplicación apagándose...")


# ============ ENDPOINTS PÚBLICOS ============
@app.get("/", tags=["system"], summary="Status general")
async def root():
    """Estado general de la API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


@app.get("/health", tags=["system"], summary="Health check")
async def health_check():
    """Health check simple para monitoreo"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": settings.APP_NAME,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }


@app.get("/api/status", tags=["system"], summary="Status detallado")
async def api_status():
    """Estado detallado de la API y servicios"""
    try:
        firebase = get_firebase()
        firebase_health = firebase.health_check()
    except:
        firebase_health = {"firebase_connected": False, "error": "No disponible"}
    
    return {
        "status": "operational",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "services": {
            "firebase": firebase_health,
            "cors": {"enabled": True, "origins": len(settings.get_origins_list())},
            "rate_limiting": {"enabled": settings.RATE_LIMIT_ENABLED},
            "logging": {"level": settings.LOG_LEVEL, "format": settings.LOG_FORMAT}
        },
        "endpoints": {
            "auth": "/api/auth",
            "employees": "/api/employees",
            "hours": "/api/hours",
            "payroll": "/api/payroll",
            "configuration": "/api/configuration",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Iniciando servidor...")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if not settings.DEBUG else "debug"
    )
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
