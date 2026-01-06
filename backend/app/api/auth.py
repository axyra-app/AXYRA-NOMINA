"""
Endpoints de autenticación
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.database.firebase import get_firebase
from app.utils.validators import validar_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


class SignupRequest(BaseModel):
    email: str
    password: str
    display_name: str


class AuthResponse(BaseModel):
    uid: str
    email: str
    display_name: str = ""
    message: str = ""


@router.post("/signup", response_model=AuthResponse)
async def signup(request: SignupRequest):
    """Registra un nuevo usuario con validaciones"""
    try:
        # Validar email
        email_valido, msg_email = validar_email(request.email)
        if not email_valido:
            raise HTTPException(status_code=400, detail=f"Email: {msg_email}")
        
        # Validar contraseña
        if not request.password or len(request.password) < 6:
            raise HTTPException(
                status_code=400,
                detail="Contraseña debe tener al menos 6 caracteres"
            )
        
        # Validar display_name
        if not request.display_name or len(request.display_name) < 2:
            raise HTTPException(
                status_code=400,
                detail="El nombre debe tener al menos 2 caracteres"
            )
        
        firebase = get_firebase()
        user = firebase.create_user(
            email=request.email,
            password=request.password,
            display_name=request.display_name
        )
        return AuthResponse(
            uid=user["uid"],
            email=user["email"],
            display_name=user.get("display_name", ""),
            message="Usuario creado exitosamente"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creando usuario: {str(e)}"
        )


@router.post("/verify-token")
async def verify_token(token: str):
    """Verifica un token de Firebase"""
    try:
        firebase = get_firebase()
        decoded_token = firebase.auth.verify_id_token(token)
        return {
            "uid": decoded_token["uid"],
            "email": decoded_token.get("email", ""),
            "valid": True
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )


@router.get("/me")
async def get_current_user(token: str):
    """Obtiene el usuario actual"""
    try:
        firebase = get_firebase()
        decoded_token = firebase.auth.verify_id_token(token)
        uid = decoded_token["uid"]
        
        # Obtener datos del usuario desde la BD
        user_data = firebase.read_data(f"users/{uid}")
        
        return {
            "uid": uid,
            "email": decoded_token.get("email"),
            "user_data": user_data
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
