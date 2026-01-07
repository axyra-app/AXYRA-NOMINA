"""
🔐 MÓDULO DE SEGURIDAD AVANZADO
Sistema de autenticación y validación profesional
Integración con Firebase + JWT mejorado
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, validator
import hashlib
import secrets
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()


class TokenData(BaseModel):
    """Modelo para datos del token JWT"""
    uid: str = Field(..., description="Firebase UID único del usuario")
    email: str = Field(..., description="Email del usuario")
    client_id: str = Field(..., description="ID del cliente")
    exp: datetime = Field(..., description="Tiempo de expiración")
    iat: datetime = Field(..., description="Tiempo de emisión")
    
    @validator('uid', 'email', 'client_id', pre=True)
    def validate_not_empty(cls, v):
        if not v or not str(v).strip():
            raise ValueError("Campo no puede estar vacío")
        return v


class TokenResponse(BaseModel):
    """Respuesta con token de acceso"""
    access_token: str = Field(..., description="JWT token")
    token_type: str = Field(default="bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Segundos hasta expiración")
    refresh_token: Optional[str] = Field(None, description="Token para renovar sesión")


class UserContext(BaseModel):
    """Contexto del usuario autenticado"""
    uid: str
    email: str
    client_id: str
    authenticated_at: datetime
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None


class SecurityConfig:
    """Configuración centralizada de seguridad"""
    
    # JWT
    ALGORITHM = settings.ALGORITHM
    SECRET_KEY = settings.SECRET_KEY
    ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    # Hash
    HASH_ALGORITHM = "sha256"
    
    # Rate limiting
    RATE_LIMIT_LOGIN = "5/minute"
    RATE_LIMIT_GENERAL = "100/minute"
    RATE_LIMIT_UPLOAD = "10/minute"
    
    @staticmethod
    def validate_secret_key() -> bool:
        """Valida que SECRET_KEY sea suficientemente fuerte"""
        if len(settings.SECRET_KEY) < 32:
            logger.warning("⚠️  SECRET_KEY es muy corta (< 32 caracteres). Usa una más fuerte en producción.")
            return False
        return True


def create_access_token(
    data: Dict[str, Any],
    expires_delta: Optional[timedelta] = None,
    client_id: str = None
) -> str:
    """
    Crea un JWT token de acceso profesional
    
    Args:
        data: Datos a incluir en el token
        expires_delta: Tiempo de expiración customizado
        client_id: ID del cliente
        
    Returns:
        JWT token codificado
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    # Agregar claims estándar
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access",
    })
    
    if client_id:
        to_encode["client_id"] = client_id
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            SecurityConfig.SECRET_KEY,
            algorithm=SecurityConfig.ALGORITHM
        )
        logger.info(f"✅ Token creado para usuario: {data.get('email')}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"❌ Error creando token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creando token de autenticación"
        )


def create_refresh_token(user_id: str, client_id: str = None) -> str:
    """
    Crea un token de refresco de larga duración
    
    Args:
        user_id: UID del usuario
        client_id: ID del cliente
        
    Returns:
        JWT refresh token
    """
    expires = datetime.utcnow() + timedelta(
        days=SecurityConfig.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    data = {
        "uid": user_id,
        "type": "refresh",
        "jti": secrets.token_urlsafe(16),  # JWT ID único
    }
    
    if client_id:
        data["client_id"] = client_id
    
    return jwt.encode(
        data,
        SecurityConfig.SECRET_KEY,
        algorithm=SecurityConfig.ALGORITHM
    )


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verifica y decodifica un JWT token
    
    Args:
        credentials: Credenciales HTTP Bearer
        
    Returns:
        Datos del token decodificado
        
    Raises:
        HTTPException: Si el token es inválido
    """
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            SecurityConfig.SECRET_KEY,
            algorithms=[SecurityConfig.ALGORITHM]
        )
        
        # Validaciones básicas
        uid: str = payload.get("uid")
        email: str = payload.get("email")
        token_type = payload.get("type", "access")
        
        if not uid or not email:
            logger.warning("❌ Token sin UID o email")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: datos incompletos"
            )
        
        if token_type != "access":
            logger.warning(f"❌ Token de tipo incorrecto: {token_type}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tipo de token inválido"
            )
        
        logger.debug(f"✅ Token verificado para: {email}")
        return payload
        
    except JWTError as e:
        logger.warning(f"❌ Error JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    except Exception as e:
        logger.error(f"❌ Error verificando token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error de autenticación"
        )


def get_current_user(token_data: Dict = Depends(verify_token)) -> UserContext:
    """
    Obtiene el contexto del usuario actual autenticado
    
    Args:
        token_data: Datos del token verificado
        
    Returns:
        Contexto del usuario
    """
    try:
        return UserContext(
            uid=token_data.get("uid"),
            email=token_data.get("email"),
            client_id=token_data.get("client_id", ""),
            authenticated_at=datetime.utcnow()
        )
    except Exception as e:
        logger.error(f"❌ Error obteniendo contexto de usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Error obteniendo información del usuario"
        )


def hash_password(password: str) -> str:
    """
    Genera hash seguro de contraseña
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash SHA256 + salt
    """
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations
    )
    return f"{salt}${pwd_hash.hex()}"


def verify_password(password: str, hash_stored: str) -> bool:
    """
    Verifica contraseña contra hash almacenado
    
    Args:
        password: Contraseña a verificar
        hash_stored: Hash almacenado
        
    Returns:
        True si coinciden
    """
    try:
        salt, pwd_hash = hash_stored.split('$')
        pwd_check = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        )
        return pwd_check.hex() == pwd_hash
    except Exception as e:
        logger.error(f"Error verificando contraseña: {str(e)}")
        return False


def generate_api_key(client_id: str, name: str = None) -> str:
    """
    Genera una API key segura para cliente
    
    Args:
        client_id: ID del cliente
        name: Nombre de la API key
        
    Returns:
        API key único
    """
    timestamp = datetime.utcnow().isoformat()
    api_key = secrets.token_urlsafe(32)
    return f"axyra_{client_id}_{api_key[:20]}"


class SecurityValidator:
    """Validadores de seguridad avanzados"""
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, str]:
        """Valida formato y seguridad de email"""
        import re
        
        if not email or len(email) > 255:
            return False, "Email inválido"
        
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return False, "Formato de email incorrecto"
        
        # Validar dominios sospechosos
        suspicious_domains = ['tempmail.', 'throwaway', 'guerrillamail', 'mailinator']
        if any(domain in email.lower() for domain in suspicious_domains):
            return False, "Email temporal no permitido"
        
        return True, "Email válido"
    
    @staticmethod
    def validate_password(password: str) -> tuple[bool, str]:
        """Valida fortaleza de contraseña"""
        if len(password) < 8:
            return False, "Mínimo 8 caracteres"
        
        if not any(c.isupper() for c in password):
            return False, "Debe contener mayúsculas"
        
        if not any(c.isdigit() for c in password):
            return False, "Debe contener números"
        
        if not any(c in "!@#$%^&*_-" for c in password):
            return False, "Debe contener caracteres especiales"
        
        return True, "Contraseña fuerte"
    
    @staticmethod
    def validate_client_id(client_id: str) -> tuple[bool, str]:
        """Valida formato de client_id"""
        if not client_id or len(client_id) < 3:
            return False, "Client ID inválido"
        
        if not client_id.replace("-", "").replace("_", "").isalnum():
            return False, "Client ID debe ser alfanumérico"
        
        return True, "Client ID válido"


# Inicializar validaciones de seguridad
def init_security():
    """Inicializa y valida configuración de seguridad"""
    logger.info("🔐 Inicializando módulo de seguridad...")
    
    if not SecurityConfig.validate_secret_key():
        logger.warning("⚠️  ADVERTENCIA: SECRET_KEY no es suficientemente fuerte")
    
    logger.info("✅ Módulo de seguridad inicializado correctamente")
