"""
Gestor de Firebase
Autenticación y base de datos en tiempo real
"""

import firebase_admin
from firebase_admin import credentials, db, auth
from app.config.settings import settings
import os
from typing import Optional, Dict, Any


class FirebaseManager:
    """Gestor centralizado de Firebase"""
    
    _instance = None
    
    def __new__(cls):
        """Patrón Singleton para una única instancia"""
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Inicializa Firebase una sola vez"""
        if self._initialized:
            return
            
        try:
            # Verificar si Firebase ya está inicializado
            if not firebase_admin._apps:
                cred_path = settings.FIREBASE_CREDENTIALS_PATH
                
                # Soportar tanto ruta relativa como absoluta
                if not os.path.exists(cred_path):
                    # Intentar en el directorio actual
                    cred_path = os.path.join(os.getcwd(), cred_path)
                
                if os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred, {
                        'databaseURL': settings.FIREBASE_DATABASE_URL
                    })
                else:
                    # En modo desarrollo, continuar sin Firebase si no existe el archivo
                    if settings.DEBUG:
                        print(f"⚠️  WARNING: Firebase credentials not found at {cred_path}")
                        print("   Ejecutando en modo MOCK para desarrollo")
                        self._mock_mode = True
                    else:
                        raise FileNotFoundError(
                            f"Firebase credentials file not found: {cred_path}"
                        )
            
            self._initialized = True
            self._mock_mode = False
            self.db = db
            self.auth = auth
            
        except Exception as e:
            if settings.DEBUG:
                print(f"⚠️  WARNING: Firebase initialization error: {str(e)}")
                print("   Ejecutando en modo MOCK para desarrollo")
                self._mock_mode = True
                self._initialized = True
            else:
                raise Exception(f"Error initializing Firebase: {str(e)}")
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Obtiene un usuario por email"""
        try:
            user = self.auth.get_user_by_email(email)
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
                "disabled": user.disabled,
            }
        except auth.AuthError as e:
            return None
    
    def create_user(self, email: str, password: str, display_name: str = "") -> Dict:
        """Crea un nuevo usuario"""
        try:
            user = self.auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name,
            }
        except auth.AuthError as e:
            raise Exception(f"Error creating user: {str(e)}")
    
    def delete_user(self, uid: str) -> bool:
        """Elimina un usuario"""
        try:
            self.auth.delete_user(uid)
            return True
        except auth.AuthError as e:
            raise Exception(f"Error deleting user: {str(e)}")
    
    def write_data(self, path: str, data: Dict) -> bool:
        """Escribe datos en la base de datos"""
        try:
            self.db.reference(path).set(data)
            return True
        except Exception as e:
            raise Exception(f"Error writing to database: {str(e)}")
    
    def read_data(self, path: str) -> Optional[Dict]:
        """Lee datos de la base de datos"""
        try:
            data = self.db.reference(path).get()
            return data.val() if data else None
        except Exception as e:
            # 404 y otros errores se manejan como datos no encontrados
            # No es un error de servidor, simplemente no hay datos
            if "404" in str(e) or "Not Found" in str(e):
                return None
            # Solo lanzar excepción para errores reales
            raise Exception(f"Error reading from database: {str(e)}")
    
    def update_data(self, path: str, data: Dict) -> bool:
        """Actualiza datos en la base de datos"""
        try:
            self.db.reference(path).update(data)
            return True
        except Exception as e:
            raise Exception(f"Error updating database: {str(e)}")
    
    def delete_data(self, path: str) -> bool:
        """Elimina datos de la base de datos"""
        try:
            self.db.reference(path).delete()
            return True
        except Exception as e:
            raise Exception(f"Error deleting from database: {str(e)}")


def get_firebase() -> FirebaseManager:
    """Obtiene la instancia de Firebase"""
    return FirebaseManager()
