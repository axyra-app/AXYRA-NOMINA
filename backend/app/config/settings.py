"""
⚙️ CONFIGURACIÓN AVANZADA - AXYRA NÓMINA
Gestión centralizada de variables de entorno y configuración profesional
"""

from pydantic_settings import BaseSettings
from pydantic import Field, field_validator
from pathlib import Path
import os
from typing import Optional, List


class Settings(BaseSettings):
    """Configuración global de la aplicación con validaciones"""
    
    # ============ APLICACIÓN ============
    APP_NAME: str = Field(default="Sistema de Nómina Axyra", description="Nombre de la aplicación")
    DEBUG: bool = Field(default=False, description="Modo debug (NUNCA True en producción)")
    VERSION: str = Field(default="2.1.0", description="Versión de la aplicación")
    ENVIRONMENT: str = Field(default="development", description="Entorno: development, staging, production")
    
    # ============ FIREBASE ============
    FIREBASE_CREDENTIALS_PATH: str = Field(default="serviceAccountKey.json", description="Ruta a credenciales Firebase")
    FIREBASE_DATABASE_URL: str = Field(default="", description="URL de base de datos realtime Firebase")
    FIREBASE_CREDENTIALS_JSON: Optional[str] = Field(default=None, description="Credenciales JSON en variable de entorno")
    FIREBASE_PROJECT_ID: str = Field(default="", description="ID del proyecto Firebase")
    
    # ============ SEGURIDAD ============
    SECRET_KEY: str = Field(
        default="cambiar-en-produccion-minimo-32-caracteres",
        description="Clave secreta para JWT (mínimo 32 caracteres)"
    )
    ALGORITHM: str = Field(default="HS256", description="Algoritmo para JWT")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, description="Minutos de expiración del token")
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7, description="Días de expiración del refresh token")
    
    # ============ CORS ============
    ALLOWED_ORIGINS_STR: str = Field(
        default="http://localhost:3000,http://localhost:5173",
        description="Orígenes permitidos (separados por comas)"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True, description="Permitir credenciales en CORS")
    
    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_STR.split(",")]
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Métodos HTTP permitidos"
    )
    
    # ============ RATE LIMITING ============
    RATE_LIMIT_ENABLED: bool = Field(default=True, description="Habilitar rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(default=100, description="Requests por ventana de tiempo")
    RATE_LIMIT_WINDOW_SECONDS: int = Field(default=60, description="Ventana de tiempo en segundos")
    
    # ============ LOGGING ============
    LOG_LEVEL: str = Field(default="INFO", description="Nivel de logging")
    LOG_FORMAT: str = Field(default="json", description="Formato de logs: json o text")
    LOG_FILE: Optional[str] = Field(default="logs/app.log", description="Archivo de log")
    
    # ============ VALIDACIONES ============
    @field_validator('DEBUG')
    @classmethod
    def validate_debug_production(cls, v, info):
        """Evita DEBUG=True en producción"""
        env = info.data.get('ENVIRONMENT', 'development')
        if v and env == 'production':
            raise ValueError("❌ DEBUG no puede ser True en PRODUCCIÓN")
        return v
    
    @field_validator('SECRET_KEY')
    @classmethod
    def validate_secret_key(cls, v):
        """Valida que SECRET_KEY sea suficientemente fuerte"""
        if len(v) < 32:
            raise ValueError("❌ SECRET_KEY debe tener mínimo 32 caracteres")
        if v == "cambiar-en-produccion-minimo-32-caracteres":
            raise ValueError("❌ Debes cambiar SECRET_KEY antes de producción")
        return v
    
    @field_validator('ENVIRONMENT')
    @classmethod
    def validate_environment(cls, v):
        """Valida que environment sea válido"""
        valid_envs = ['development', 'staging', 'production']
        if v not in valid_envs:
            raise ValueError(f"❌ ENVIRONMENT debe ser uno de: {valid_envs}")
        return v.lower()
    
    @field_validator('FIREBASE_DATABASE_URL')
    @classmethod
    def validate_firebase_url(cls, v):
        """Valida formato de URL Firebase"""
        if v and not v.endswith('.firebaseio.com'):
            raise ValueError("❌ FIREBASE_DATABASE_URL inválida (debe terminar en .firebaseio.com)")
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = "ignore"  # Ignorar variables extras en .env
    
    @property
    def is_production(self) -> bool:
        """Verifica si está en producción"""
        return self.ENVIRONMENT == 'production'
    
    @property
    def is_development(self) -> bool:
        """Verifica si está en desarrollo"""
        return self.ENVIRONMENT == 'development'
    
    def get_database_url(self) -> str:
        """Obtiene URL de base de datos con validación"""
        if not self.FIREBASE_DATABASE_URL:
            raise ValueError("❌ FIREBASE_DATABASE_URL no configurada")
        return self.FIREBASE_DATABASE_URL
    
    def get_origins_list(self) -> List[str]:
        """Obtiene lista de orígenes permitidos"""
        return self.ALLOWED_ORIGINS if isinstance(self.ALLOWED_ORIGINS, list) else []


# Crear instancia de configuración global
try:
    settings = Settings()
    print(f"[OK] Settings loaded: {settings.ENVIRONMENT} (v{settings.VERSION})")
except ValueError as e:
    print(f"[ERROR] Settings error: {str(e)}")
    raise
