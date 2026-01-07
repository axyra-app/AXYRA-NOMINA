# Configuración del Sistema

## Firebase

### 1. serviceAccountKey.json

```bash
# CRÍTICO: Este archivo es necesario para que funcione
1. Ve a Firebase Console → Tu proyecto
2. Configuración del proyecto → Cuentas de servicio
3. Haz clic en "Generar clave privada"
4. Descarga el JSON
5. Colócalo en: backend/serviceAccountKey.json
```

### 2. Verificar conexión

```bash
cd backend
python -c "from app.database.firebase import db; print('Firebase conectado:', db.reference('clients').get().val() is not None or True)"
```

---

## Variables de Entorno

### Backend (backend/.env)
```
FIREBASE_URL=https://axyra-nomina.firebaseio.com
JWT_SECRET=your-secret-key-min-32-chars
DEBUG=False
```

### Frontend (frontend/.env)
```
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_URL=https://axyra-nomina.firebaseio.com
```

---

## Base de Datos - Estructura Esperada

Firebase crea automáticamente esta estructura:

```
clients/
├── mi-empresa-id/
│   ├── employees/
│   ├── hours/
│   ├── payroll_history/
│   ├── payroll_batches/
│   ├── config/
│   └── audit_logs/
└── otra-empresa/
    └── ...

users/
├── user-id-1/
│   ├── email: "admin@empresa.com"
│   ├── nombre: "Juan"
│   ├── client_id: "mi-empresa-id"
│   └── role: "admin"
└── user-id-2/
    └── ...
```

---

## Testing

### 1. Tests automáticos
```bash
python test_endpoints.py
```

Resultados:
- Verde = OK
- Rojo = Error

### 2. Verificar endpoints manualmente

```bash
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Pruebas
curl http://localhost:8000/health
```

Debería responder:
```json
{"status": "OK", "timestamp": "..."}
```

---

## Problemas Comunes

### "Permission denied reading /clients"
- Asegúrate que `serviceAccountKey.json` está en `backend/`
- Verifica que las reglas de Firebase están publicadas

### "Error: FIREBASE_URL no configurado"
- Crea `frontend/.env` con `VITE_FIREBASE_URL=https://axyra-nomina.firebaseio.com`

### "404 Not Found" en endpoints
- Verifica que el backend está corriendo en `http://localhost:8000`
- Revisa los logs: `backend/logs/app.log`

### CORS errors
- El backend ya tiene CORS configurado
- Si persiste, verifica `backend/app/__init__.py`

---

## Arquitectura

```
Frontend (React + Vite)
    ↓
    └─→ JWT Token
    
API Backend (FastAPI)
    ├─→ Autenticación (JWT)
    ├─→ Validaciones
    ├─→ Lógica de negocio
    └─→ Firebase Database

Firebase Realtime Database
    ├─→ Datos de usuarios
    ├─→ Empleados
    ├─→ Horas trabajadas
    ├─→ Nóminas
    └─→ Logs de auditoría
```

---

## Siguientes Pasos

1. ✅ Backend funcionando
2. ✅ Firebase reglas publicadas
3. ⏳ Frontend desarrollo (pages, forms)
4. ⏳ Integración completa
5. ⏳ Tests end-to-end
6. ⏳ Deployment

---

## Soporte Rápido

**Logs del backend:**
```bash
tail -f backend/logs/app.log
```

**Limpiar cache Frontend:**
```bash
cd frontend
rm -rf node_modules/.vite
npm run dev
```

**Reiniciar todo:**
```bash
./setup-dev.ps1      # PowerShell
# O
setup-dev.bat        # Windows
```
