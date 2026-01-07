#!/usr/bin/env python3
"""
Script de Inicialización y Verificación - Sistema de Nómina Axyra
Verifica que todo está configurado y listo para funcionar
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime

class Verificador:
    def __init__(self):
        self.root = Path(__file__).parent
        self.errors = []
        self.warnings = []
        self.success = []
        
    def log_success(self, msg):
        print(f"✓ {msg}")
        self.success.append(msg)
    
    def log_warning(self, msg):
        print(f"⚠ {msg}")
        self.warnings.append(msg)
    
    def log_error(self, msg):
        print(f"✗ {msg}")
        self.errors.append(msg)
    
    def check_files(self):
        """Verifica que existan los archivos necesarios"""
        print("\n[1] Verificando archivos...")
        
        files = {
            'backend/.env': 'Configuración del backend',
            'backend/main.py': 'Aplicación principal',
            'backend/requirements.txt': 'Dependencias Python',
            'frontend/.env': 'Configuración del frontend',
            'frontend/package.json': 'Dependencias Node',
        }
        
        for path, desc in files.items():
            full_path = self.root / path
            if full_path.exists():
                self.log_success(f"{desc}: {path}")
            else:
                self.log_error(f"Falta {desc}: {path}")
    
    def check_serviceaccount(self):
        """Verifica serviceAccountKey.json"""
        print("\n[2] Verificando serviceAccountKey...")
        
        path = self.root / 'backend' / 'serviceAccountKey.json'
        if path.exists():
            try:
                with open(path) as f:
                    data = json.load(f)
                    if 'project_id' in data and 'private_key' in data:
                        self.log_success("serviceAccountKey.json válido")
                    else:
                        self.log_error("serviceAccountKey.json corrupto")
            except Exception as e:
                self.log_error(f"Error leyendo serviceAccountKey: {e}")
        else:
            self.log_warning("serviceAccountKey.json no encontrado - Firebase no funcionará")
    
    def check_env_files(self):
        """Verifica variables de entorno"""
        print("\n[3] Verificando variables de entorno...")
        
        # Backend
        backend_env = self.root / 'backend' / '.env'
        if backend_env.exists():
            content = backend_env.read_text()
            if 'FIREBASE_DATABASE_URL' in content:
                self.log_success("Backend .env configurado")
            else:
                self.log_error("Backend .env incompleto")
        else:
            self.log_error("Falta backend/.env")
        
        # Frontend
        frontend_env = self.root / 'frontend' / '.env'
        if frontend_env.exists():
            content = frontend_env.read_text()
            if 'VITE_API_URL' in content:
                self.log_success("Frontend .env configurado")
            else:
                self.log_error("Frontend .env incompleto")
        else:
            self.log_error("Falta frontend/.env")
    
    def check_dependencies(self):
        """Verifica dependencias instaladas"""
        print("\n[4] Verificando dependencias...")
        
        # Python
        try:
            import fastapi
            self.log_success("FastAPI instalado")
        except:
            self.log_warning("FastAPI no instalado - ejecuta: pip install -r requirements.txt")
        
        try:
            import firebase_admin
            self.log_success("Firebase Admin SDK instalado")
        except:
            self.log_warning("Firebase Admin SDK no instalado")
        
        # Node
        node_modules = self.root / 'frontend' / 'node_modules'
        if node_modules.exists():
            self.log_success("Frontend dependencias instaladas")
        else:
            self.log_warning("Frontend dependencias no instaladas - ejecuta: cd frontend && npm install")
    
    def check_backend_running(self):
        """Verifica si el backend está corriendo"""
        print("\n[5] Verificando backend...")
        
        try:
            resp = requests.get("http://localhost:8000/health", timeout=2)
            if resp.status_code == 200:
                self.log_success("Backend está corriendo en http://localhost:8000")
                return True
            else:
                self.log_warning("Backend no responde correctamente")
        except:
            self.log_warning("Backend no está corriendo - ejecuta: cd backend && python main.py")
        
        return False
    
    def check_frontend_ready(self):
        """Verifica si frontend está listo"""
        print("\n[6] Verificando frontend...")
        
        vite_config = self.root / 'frontend' / 'vite.config.js'
        if vite_config.exists():
            self.log_success("Configuración de Vite encontrada")
        else:
            self.log_error("Falta vite.config.js")
        
        app_jsx = self.root / 'frontend' / 'src' / 'App.jsx'
        if app_jsx.exists():
            self.log_success("App.jsx encontrado")
        else:
            self.log_error("Falta src/App.jsx")
    
    def generate_report(self):
        """Genera reporte final"""
        print("\n" + "=" * 60)
        print("REPORTE DE VERIFICACIÓN")
        print("=" * 60)
        
        total = len(self.success) + len(self.warnings) + len(self.errors)
        print(f"\n✓ Exitoso: {len(self.success)}")
        print(f"⚠ Advertencias: {len(self.warnings)}")
        print(f"✗ Errores: {len(self.errors)}")
        
        if self.errors:
            print("\nERRORES A RESOLVER:")
            for err in self.errors:
                print(f"  - {err}")
        
        if self.warnings:
            print("\nADVERTENCIAS:")
            for warn in self.warnings:
                print(f"  - {warn}")
        
        print("\n" + "=" * 60)
        
        if not self.errors:
            print("ESTADO: Sistema listo para desarrollar")
            print("\nProximos pasos:")
            print("1. Terminal 1: cd backend && python main.py")
            print("2. Terminal 2: cd frontend && npm run dev")
            print("3. Abre http://localhost:5173")
        else:
            print("ESTADO: Hay errores que resolver")
            return False
        
        print("=" * 60 + "\n")
        return True
    
    def run(self):
        """Ejecuta todas las verificaciones"""
        print("\nSistema de Nómina Axyra - Verificación de Setup")
        print("=" * 60)
        
        self.check_files()
        self.check_serviceaccount()
        self.check_env_files()
        self.check_dependencies()
        self.check_backend_running()
        self.check_frontend_ready()
        
        success = self.generate_report()
        return success

if __name__ == '__main__':
    verificador = Verificador()
    success = verificador.run()
    sys.exit(0 if success else 1)
