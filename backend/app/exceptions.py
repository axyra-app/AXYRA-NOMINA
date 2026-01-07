"""
⚠️ GESTOR DE ERRORES Y EXCEPCIONES
Manejo centralizado de errores con logging profesional
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import traceback

logger = logging.getLogger(__name__)


class APIError(Exception):
    """Excepción base para errores de API"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        error_code: str = "bad_request",
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationAPIError(APIError):
    """Error de validación"""
    def __init__(self, message: str, details: Optional[Dict] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="validation_error",
            details=details
        )


class AuthenticationAPIError(APIError):
    """Error de autenticación"""
    def __init__(self, message: str = "No autorizado"):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="authentication_error"
        )


class AuthorizationAPIError(APIError):
    """Error de autorización"""
    def __init__(self, message: str = "No tiene permisos"):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="authorization_error"
        )


class NotFoundAPIError(APIError):
    """Error recurso no encontrado"""
    def __init__(self, resource: str = "Recurso", resource_id: str = ""):
        message = f"{resource} no encontrado"
        if resource_id:
            message += f": {resource_id}"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="not_found"
        )


class ConflictAPIError(APIError):
    """Error de conflicto"""
    def __init__(self, message: str):
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="conflict"
        )


class RateLimitAPIError(APIError):
    """Error de rate limiting"""
    def __init__(self, retry_after: int = 60):
        super().__init__(
            message="Demasiadas solicitudes. Intenta de nuevo después.",
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="rate_limit_exceeded",
            details={"retry_after": retry_after}
        )


class DatabaseAPIError(APIError):
    """Error de base de datos"""
    def __init__(self, message: str = "Error de base de datos"):
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="database_error"
        )


class ExternalServiceAPIError(APIError):
    """Error en servicio externo"""
    def __init__(self, service: str, message: str = ""):
        full_message = f"Error en {service}"
        if message:
            full_message += f": {message}"
        super().__init__(
            message=full_message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="external_service_error"
        )


def format_error_response(
    error: APIError,
    request_id: str = None
) -> Dict[str, Any]:
    """Formatea respuesta de error de manera consistente"""
    
    response = {
        "error": error.error_code,
        "message": error.message,
        "status_code": error.status_code,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if request_id:
        response["request_id"] = request_id
    
    if error.details:
        response["details"] = error.details
    
    return response


def register_error_handlers(app: FastAPI):
    """Registra todos los manejadores de errores en la app"""
    
    # Manejador para APIError
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError):
        request_id = getattr(request.state, "request_id", None)
        
        log_level = "warning" if exc.status_code < 500 else "error"
        logger_func = getattr(logger, log_level)
        
        logger_func(
            f"🔴 APIError [{request_id}]: {exc.error_code} - {exc.message}",
            extra={
                "request_id": request_id,
                "error_code": exc.error_code,
                "status_code": exc.status_code,
            }
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content=format_error_response(exc, request_id)
        )
    
    # Manejador para errores de validación Pydantic
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        request_id = getattr(request.state, "request_id", None)
        
        # Extraer detalles de errores
        error_details = []
        for error in exc.errors():
            error_details.append({
                "field": ".".join(str(x) for x in error["loc"][1:]),
                "type": error["type"],
                "message": error["msg"]
            })
        
        logger.warning(
            f"⚠️  Validation Error [{request_id}]: {len(error_details)} errores",
            extra={
                "request_id": request_id,
                "errors": error_details
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "validation_error",
                "message": "Error en validación de datos",
                "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "details": error_details,
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # Manejador para excepciones genéricas (fallback)
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        request_id = getattr(request.state, "request_id", None)
        
        logger.error(
            f"❌ Excepción no manejada [{request_id}]: {str(exc)}",
            extra={
                "request_id": request_id,
                "error_type": type(exc).__name__,
            },
            exc_info=True
        )
        
        # En desarrollo, mostrar traceback completo
        from app.config.settings import settings
        
        if settings.DEBUG:
            detail = {
                "error_type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc().split('\n')
            }
        else:
            detail = "Error interno del servidor. Contacta a soporte si el problema persiste."
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "internal_server_error",
                "message": "Error interno del servidor",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "request_id": request_id,
                "detail": detail if settings.DEBUG else None,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
