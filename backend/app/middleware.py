"""
🛡️ MIDDLEWARE DE SEGURIDAD AVANZADO
Protección contra ataques comunes y logging de seguridad
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime
import logging
import time
import uuid
from typing import Callable

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware que agrega headers de seguridad HTTP
    Protege contra vulnerabilidades comunes
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        response = await call_next(request)
        
        # Headers de seguridad estándar
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' 'unsafe-inline'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        # Header personalizado
        response.headers["X-Powered-By"] = "Axyra-Nomina/2.1.0"
        
        return response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que registra todas las requests con detalles de seguridad
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        # Generar ID único para la request
        request_id = str(uuid.uuid4())[:8]
        request.state.request_id = request_id
        
        # Información de la request
        start_time = time.time()
        
        # No loguear headers sensibles
        safe_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ['authorization', 'x-api-key', 'cookie']
        }
        
        logger.info(
            f"📨 REQUEST [{request_id}] {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown")[:100],
            }
        )
        
        try:
            response = await call_next(request)
            
            process_time = time.time() - start_time
            
            # Log de respuesta
            log_level = "warning" if response.status_code >= 400 else "info"
            logger_func = getattr(logger, log_level)
            
            logger_func(
                f"✅ RESPONSE [{request_id}] {response.status_code} ({process_time:.2f}s)",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )
            
            # Agregar header con ID de request
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"❌ ERROR [{request_id}] {str(e)} ({process_time:.2f}s)",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "process_time": process_time,
                },
                exc_info=True
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para rate limiting por IP
    """
    
    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.requests = {}  # {ip: [timestamps]}
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        minute_ago = current_time - 60
        
        # Inicializar lista si no existe
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Limpiar requests antiguas (más de 1 minuto)
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if ts > minute_ago
        ]
        
        # Verificar límite
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            logger.warning(f"⚠️  Rate limit excedido para IP: {client_ip}")
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "Demasiadas solicitudes. Intenta de nuevo en un minuto.",
                    "retry_after": 60
                }
            )
        
        # Agregar timestamp actual
        self.requests[client_ip].append(current_time)
        
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.requests[client_ip])
        )
        
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para manejo centralizado de errores
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            request_id = getattr(request.state, "request_id", "unknown")
            
            logger.error(
                f"❌ Excepción no manejada [{request_id}]: {str(exc)}",
                extra={"request_id": request_id},
                exc_info=True
            )
            
            # En desarrollo, mostrar detalles
            # En producción, mostrar mensaje genérico
            from app.config.settings import settings
            
            if settings.DEBUG:
                detail = str(exc)
            else:
                detail = "Error interno del servidor. Contacta a soporte."
            
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": "internal_server_error",
                    "detail": detail,
                    "request_id": request_id,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )


class CORSValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware para validar y loguear CORS
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        origin = request.headers.get("origin")
        
        if origin:
            logger.debug(f"🌐 CORS request from: {origin}")
        
        response = await call_next(request)
        
        if origin:
            cors_origin = response.headers.get("access-control-allow-origin")
            if cors_origin:
                logger.debug(f"✅ CORS permitido: {cors_origin}")
            else:
                logger.warning(f"⚠️  CORS bloqueado para: {origin}")
        
        return response


class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """
    Middleware para whitelist de IPs (opcional)
    """
    
    def __init__(self, app, whitelist: list = None):
        super().__init__(app)
        self.whitelist = whitelist or []
    
    async def dispatch(self, request: Request, call_next: Callable) -> any:
        if not self.whitelist:
            return await call_next(request)
        
        client_ip = request.client.host if request.client else "unknown"
        
        if client_ip not in self.whitelist:
            logger.warning(f"⚠️  IP no autorizada: {client_ip}")
            # En development, permitir; en production, bloquear
            from app.config.settings import settings
            if settings.is_production:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "IP no autorizada"}
                )
        
        return await call_next(request)
