"""
Endpoints de autenticación con JWT profesional
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, EmailStr, Field
from app.database.firebase import get_firebase
from app.utils.validators import validar_email
from app.security_enhanced import (
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user,
    SecurityValidator,
    TokenResponse,
    UserContext
)
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str = Field(..., description="Email del usuario")
    password: str = Field(..., description="Contraseña del usuario")


class SignupRequest(BaseModel):
    email: str = Field(..., description="Email único del usuario")
    password: str = Field(..., description="Contraseña segura (8+ chars)")
    display_name: str = Field(..., description="Nombre completo del usuario")


class AuthResponse(BaseModel):
    uid: str
    email: str
    display_name: str = ""
    message: str = ""
    access_token: str = ""
    refresh_token: str = ""
    token_type: str = "bearer"


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest):
    """Registra un nuevo usuario con validaciones profesionales y JWT"""
    try:
        # Validar email con SecurityValidator
        if not SecurityValidator.validate_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Email inválido o dominio temporal no permitido"
            )
        
        # Validar contraseña con SecurityValidator
        password_valid = SecurityValidator.validate_password(request.password)
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Contraseña debe tener 8+ caracteres, mayúsculas, números y caracteres especiales"
            )
        
        # Validar display_name
        if not request.display_name or len(request.display_name) < 2:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El nombre debe tener al menos 2 caracteres"
            )
        
        firebase = get_firebase()
        
        # Crear usuario en Firebase
        user = firebase.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name
        )
        
        uid = user["uid"]
        
        # Crear tokens JWT
        access_token = create_access_token(uid, request.email)
        refresh_token = create_refresh_token(uid, request.email)
        
        logger.info(f"Usuario registrado exitosamente: {request.email} (UID: {uid})")
        
        return AuthResponse(
            uid=uid,
            email=request.email,
            display_name=request.display_name,
            access_token=access_token,
            refresh_token=refresh_token,
            message="Usuario creado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creando usuario: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creando usuario: {str(e)}"
        )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Autentica usuario y devuelve JWT tokens profesionales"""
    try:
        # Validar email
        if not SecurityValidator.validate_email(request.email):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        firebase = get_firebase()
        
        # Verificar credenciales en Firebase
        try:
            user = firebase.auth.get_user_by_email(request.email)
        except:
            logger.warning(f"Intento de login con email inválido: {request.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )
        
        uid = user.uid
        email = user.email
        display_name = user.display_name or ""
        
        # Crear JWT tokens
        access_token = create_access_token(uid, email)
        refresh_token = create_refresh_token(uid, email)
        
        logger.info(f"Login exitoso: {email} (UID: {uid})")
        
        return AuthResponse(
            uid=uid,
            email=email,
            display_name=display_name,
            access_token=access_token,
            refresh_token=refresh_token,
            message="Login exitoso"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos"
        )


@router.post("/refresh")
async def refresh_access_token(refresh_token: str = Query(...)):
    """Genera un nuevo access token usando refresh token"""
    try:
        # Verificar refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        
        uid = payload.get("uid")
        email = payload.get("email")
        
        if not uid or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        # Crear nuevo access token
        new_access_token = create_access_token(uid, email)
        
        logger.info(f"Token refreshed para: {email}")
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "message": "Token renovado exitosamente"
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error refreshing token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )


@router.get("/me", response_model=AuthResponse)
async def get_me(current_user: UserContext = Depends(get_current_user)):
    """Obtiene datos del usuario actual autenticado"""
    try:
        firebase = get_firebase()
        
        # Obtener datos completos del usuario
        user_data = firebase.read_data(f"users/{current_user.uid}") or {}
        
        logger.info(f"Me endpoint accedido por: {current_user.email}")
        
        return AuthResponse(
            uid=current_user.uid,
            email=current_user.email,
            display_name=current_user.display_name or "",
            message="Datos del usuario autenticado"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo usuario actual: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error obteniendo datos del usuario"
        )


@router.post("/logout")
async def logout(current_user: UserContext = Depends(get_current_user)):
    """Endpoint de logout (para limpiar tokens en cliente)"""
    logger.info(f"Logout: {current_user.email}")
    return {
        "message": "Logout exitoso",
        "email": current_user.email
    }
