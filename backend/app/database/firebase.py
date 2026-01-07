"""
[DB] GESTOR AVANZADO DE FIREBASE
Autenticacion, base de datos realtime y operaciones complejas
"""

import firebase_admin
from firebase_admin import credentials, db, auth
from app.config.settings import settings
import os
import json
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class FirebaseManager:
    """
    Gestor centralizado y singleton de Firebase
    Maneja autenticacion, lectura/escritura de datos y operaciones avanzadas
    """
    
    _instance = None
    _initialized = False
    _mock_mode = False
    
    def __new__(cls):
        """Patron Singleton: una unica instancia"""
        if cls._instance is None:
            cls._instance = super(FirebaseManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa Firebase una sola vez"""
        if self._initialized:
            return
        
        logger.info("[FIREBASE] Initializing Firebase Manager...")
        self._init_firebase()
        self._initialized = True
    
    def _init_firebase(self):
        """Logica de inicializacion de Firebase"""
        try:
            # Verificar si Firebase ya esta inicializado
            if firebase_admin._apps:
                logger.info("[OK] Firebase already initialized")
                self.db = db
                self.auth = auth
                self._mock_mode = False
                return
            
            cred = self._load_credentials()
            db_url = settings.get_database_url()
            
            if not db_url:
                logger.error("[ERROR] FIREBASE_DATABASE_URL not configured in .env")
                if settings.DEBUG:
                    logger.warning("[WARN] Firebase in MOCK mode (development)")
                    self._mock_mode = True
                else:
                    raise Exception("FIREBASE_DATABASE_URL required in .env")
                return
            
            if cred:
                logger.info(f"[INFO] Initializing Firebase with URL: {db_url}")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
                logger.info("[OK] Firebase initialized successfully")
                self.db = db
                self.auth = auth
                self._mock_mode = False
            elif settings.DEBUG:
                logger.warning("[WARN] Firebase in MOCK mode (credentials not found)")
                self._mock_mode = True
            else:
                raise Exception("Firebase credentials required in production")
                
        except Exception as e:
            logger.error(f"[ERROR] Error initializing Firebase: {str(e)}")
            logger.error("[ERROR] Check: 1) serviceAccountKey.json exists, 2) FIREBASE_DATABASE_URL in .env, 3) Firebase permissions")
            if not settings.DEBUG:
                raise
            self._mock_mode = True
            logger.warning("[WARN] Continuing in MOCK mode")
    
    def _load_credentials(self) -> Optional[credentials.Certificate]:
        """Carga credenciales de multiples fuentes"""
        
        # Opcion 1: Variable de entorno JSON
        if settings.FIREBASE_CREDENTIALS_JSON:
            try:
                cred_dict = json.loads(settings.FIREBASE_CREDENTIALS_JSON)
                logger.info("[OK] Credentials loaded from FIREBASE_CREDENTIALS_JSON")
                return credentials.Certificate(cred_dict)
            except json.JSONDecodeError:
                logger.warning("[ERROR] FIREBASE_CREDENTIALS_JSON invalid JSON")
        
        # Opcion 2: Archivo local
        cred_path = settings.FIREBASE_CREDENTIALS_PATH
        if not os.path.exists(cred_path):
            cred_path = os.path.join(os.getcwd(), cred_path)
        
        if os.path.exists(cred_path):
            try:
                logger.info(f"[OK] Credentials loaded from {cred_path}")
                return credentials.Certificate(cred_path)
            except Exception as e:
                logger.warning(f"[ERROR] Error loading credentials from file: {str(e)}")
        
        return None
    
    # ============ OPERACIONES DE LECTURA ============
    
    def read_data(self, path: str) -> Dict:
        """
        Lee datos de la base de datos
        
        Args:
            path: Ruta en la base de datos
            
        Returns:
            Diccionario con los datos o diccionario vacio si no existe
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Reading from {path}")
                return {}
            
            ref = self.db.reference(path)
            snapshot = ref.get()
            value = snapshot.val() if snapshot.val() is not None else {}
            
            logger.debug(f"[OK] Data read from {path}: {type(value).__name__}")
            return value if value is not None else {}
            
        except AttributeError as e:
            logger.warning(f"[WARN] Path '{path}' may not exist or Firebase not initialized properly: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"[ERROR] Error reading {path}: {str(e)}")
            if self._mock_mode:
                return {}
            raise
    
    # ============ OPERACIONES DE ESCRITURA ============
    
    def write_data(self, path: str, data: Dict) -> bool:
        """
        Escribe datos en la base de datos (sobrescribe)
        
        Args:
            path: Ruta en la base de datos
            data: Datos a escribir
            
        Returns:
            True si fue exitoso
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Writing to {path}")
                return True
            
            self.db.reference(path).set(data)
            logger.info(f"[OK] Data written to {path}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error writing to {path}: {str(e)}")
            raise
    
    def update_data(self, path: str, data: Dict) -> bool:
        """
        Actualiza datos (merge con existentes)
        
        Args:
            path: Ruta en la base de datos
            data: Datos a actualizar
            
        Returns:
            True si fue exitoso
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Updating {path}")
                return True
            
            self.db.reference(path).update(data)
            logger.info(f"[OK] Data updated at {path}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error updating {path}: {str(e)}")
            raise
    
    # ============ OPERACIONES DE ELIMINACION ============
    
    def delete_data(self, path: str) -> bool:
        """
        Elimina datos de la base de datos
        
        Args:
            path: Ruta en la base de datos
            
        Returns:
            True si fue exitoso
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Deleting {path}")
                return True
            
            self.db.reference(path).delete()
            logger.info(f"[OK] Data deleted from {path}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error deleting {path}: {str(e)}")
            raise
    
    # ============ OPERACIONES BATCH ============
    
    def batch_write(self, operations: List[Dict[str, Any]]) -> bool:
        """
        Realiza multiples operaciones en batch
        
        Args:
            operations: Lista de dict con {'path': path, 'operation': 'set'|'update'|'delete', 'data': dict}
            
        Returns:
            True si fue exitoso
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Batch with {len(operations)} operations")
                return True
            
            updates = {}
            for op in operations:
                path = op.get('path')
                operation = op.get('operation', 'set')
                data = op.get('data', {})
                
                if operation == 'delete':
                    updates[path] = None
                else:  # 'set' or 'update'
                    updates[path] = data
            
            self.db.reference().update(updates)
            logger.info(f"[OK] Batch of {len(operations)} operations completed")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error in batch write: {str(e)}")
            raise
    
    # ============ OPERACIONES ESPECIALES DE USUARIO ============
    
    def find_user_by_email(self, email: str) -> Optional[Dict]:
        """Busca usuario por email"""
        try:
            users = self.read_data("users")
            if users:
                for user_id, user_data in users.items():
                    if user_data.get("email") == email:
                        return user_data
            return None
            
        except Exception as e:
            logger.error(f"[ERROR] Error getting user by email: {str(e)}")
            raise
    
    def register_user_auth(self, email: str, password: str, display_name: str) -> Dict:
        """
        Crea un nuevo usuario en Firebase Authentication
        
        Args:
            email: Email del usuario
            password: Contraseña sin encriptar
            display_name: Nombre completo del usuario
            
        Returns:
            Diccionario con uid y datos del usuario
        """
        try:
            if self._mock_mode:
                logger.debug("[MOCK] Creating user in Firebase Auth")
                return {"uid": email.split("@")[0], "email": email, "display_name": display_name}
            
            # Crear usuario en Firebase Authentication
            user = self.auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            
            logger.info(f"[OK] User created in Firebase Auth: {email} (UID: {user.uid})")
            return {
                "uid": user.uid,
                "email": user.email,
                "display_name": user.display_name
            }
            
        except Exception as e:
            logger.error(f"[ERROR] Error creating user in Firebase Auth: {str(e)}")
            raise
    
    def initialize_user_data(self, uid: str, email: str, display_name: str) -> bool:
        """
        Inicializa la estructura de datos de un nuevo usuario en Realtime Database
        
        Args:
            uid: UID del usuario
            email: Email del usuario
            display_name: Nombre del usuario
            
        Returns:
            True si fue exitoso
        """
        try:
            # Estructura de configuración por defecto
            default_config = {
                "company": {
                    "name": "Mi Empresa",
                    "rfc": "",
                    "address": "",
                    "phone": "",
                    "email": email
                },
                "hours": {
                    "daily_hours": 8,
                    "weekly_hours": 40,
                    "hourly_rate": 0,
                    "overtime_multiplier": 1.5
                },
                "payroll": {
                    "payment_method": "transfer",
                    "payment_day": 15,
                    "currency": "MXN",
                    "fiscal_regime": ""
                }
            }
            
            # Crear datos base del usuario
            self.write_data(f"users/{uid}", {
                "email": email,
                "display_name": display_name,
                "uid": uid,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "is_active": True,
                "configuration": default_config
            })
            
            # Crear colecciones vacías
            self.write_data(f"users/{uid}/employees", {})
            self.write_data(f"users/{uid}/hours", {})
            self.write_data(f"users/{uid}/payroll", {})
            self.write_data(f"users/{uid}/logs", {
                "_initialized": datetime.now().isoformat()
            })
            
            logger.info(f"[OK] User data structure initialized: {email} (UID: {uid})")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error initializing user data: {str(e)}")
            raise
    
    def create_user(self, email: str, user_data: Dict) -> str:
        """
        Crea nuevo usuario en Realtime Database
        
        Args:
            email: Email del usuario
            user_data: Datos del usuario
            
        Returns:
            UID del usuario creado
        """
        try:
            uid = user_data.get("uid", email.split("@")[0])
            self.write_data(f"users/{uid}", {
                **user_data,
                "created_at": datetime.now().isoformat()
            })
            logger.info(f"[OK] User created: {email}")
            return uid
            
        except Exception as e:
            logger.error(f"[ERROR] Error creating user: {str(e)}")
            raise
    
    def get_user_by_uid(self, uid: str) -> Optional[Dict]:
        """Obtiene usuario por UID"""
        try:
            return self.read_data(f"users/{uid}")
        except Exception as e:
            logger.error(f"[ERROR] Error getting user by UID: {str(e)}")
            raise
    
    def update_user(self, uid: str, updates: Dict) -> bool:
        """Actualiza datos del usuario"""
        try:
            updates["updated_at"] = datetime.now().isoformat()
            return self.update_data(f"users/{uid}", updates)
        except Exception as e:
            logger.error(f"[ERROR] Error updating user: {str(e)}")
            raise
    
    # ============ OPERACIONES DE PAGINACION ============
    
    def read_paginated(self, path: str, limit: int = 50, offset: int = 0) -> Dict:
        """
        Lee datos con paginacion
        
        Args:
            path: Ruta en la base de datos
            limit: Cantidad de registros
            offset: Cantidad a saltar
            
        Returns:
            Diccionario con 'data' y 'metadata'
        """
        try:
            if self._mock_mode:
                return {"data": [], "total": 0, "limit": limit, "offset": offset}
            
            all_data = self.read_data(path) or {}
            
            # Convertir a lista si es dict
            if isinstance(all_data, dict):
                items = list(all_data.items())
            else:
                items = all_data if isinstance(all_data, list) else []
            
            total = len(items)
            paginated = items[offset:offset + limit]
            
            return {
                "data": paginated,
                "total": total,
                "limit": limit,
                "offset": offset,
                "pages": (total + limit - 1) // limit
            }
            
        except Exception as e:
            logger.error(f"[ERROR] Error in paginated read: {str(e)}")
            raise
    
    # ============ OPERACIONES DE SEGURIDAD ============
    
    def set_user_claims(self, uid: str, claims: Dict) -> bool:
        """
        Asigna custom claims a un usuario (requiere Admin SDK)
        
        Args:
            uid: UID del usuario
            claims: Dict con claims a asignar
            
        Returns:
            True si fue exitoso
        """
        try:
            if self._mock_mode:
                logger.debug(f"[MOCK] Setting claims for {uid}")
                return True
            
            self.auth.set_custom_user_claims(uid, claims)
            logger.info(f"[OK] Custom claims set for user {uid}")
            return True
            
        except Exception as e:
            logger.error(f"[ERROR] Error setting user claims: {str(e)}")
            raise
    
    # ============ OPERACIONES DE SALUD ============
    
    def health_check(self) -> bool:
        """
        Verifica conexion a Firebase
        
        Returns:
            True si esta conectado, False si es mock
        """
        try:
            if self._mock_mode:
                logger.debug("[MOCK] Health check performed")
                return False
            
            # Intento de lectura simple
            self.db.reference(".info/connected").get()
            logger.info("[OK] Firebase health check passed")
            return True
            
        except Exception as e:
            logger.error(f"[WARN] Firebase health check failed: {str(e)}")
            return False


# ============ SINGLETON GLOBAL ============

_firebase_instance = None


def get_firebase() -> FirebaseManager:
    """
    Obtiene la instancia global de FirebaseManager
    
    Returns:
        Instancia singleton de FirebaseManager
    """
    global _firebase_instance
    if _firebase_instance is None:
        _firebase_instance = FirebaseManager()
    return _firebase_instance
