# ⚡ SETUP DESPUÉS DE CLONAR

Instrucciones para configurar el proyecto después de clonarlo desde GitHub.

## 1️⃣ Backend Setup

```bash
cd backend

# Crear virtual environment
python -m venv .venv

# Activar venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cp .env.example .env

# Editar .env con tus valores:
# - FIREBASE_DATABASE_URL
# - FIREBASE_CREDENTIALS_PATH (ruta a serviceAccountKey.json)
```

## 2️⃣ Frontend Setup

```bash
cd frontend

# Instalar dependencias
npm install

# Crear archivo .env.local
cp .env.example .env.local

# Editar .env.local con tu API URL:
# VITE_API_URL=http://localhost:8000 (desarrollo)
# VITE_API_URL=https://tu-backend.vercel.app (producción)
```

## 3️⃣ Firebase Setup

1. Ir a [Firebase Console](https://console.firebase.google.com)
2. Crear nuevo proyecto o usar uno existente
3. Habilitar autenticación con Email/Password
4. Crear Realtime Database en modo producción
5. Descargar credenciales (Service Account JSON)
6. Copiar `serviceAccountKey.json` a `backend/`

## 4️⃣ Ejecutar en Desarrollo

**Terminal 1 - Backend:**
```bash
cd backend
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
python main.py
# Debería ver: Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
# Debería ver: Local: http://localhost:5173
```

## 5️⃣ Verificación

- [ ] Backend en http://localhost:8000
- [ ] Docs API en http://localhost:8000/docs
- [ ] Health check: `curl http://localhost:8000/health`
- [ ] Frontend en http://localhost:5173
- [ ] Sin errores en consola

## 🚀 Deployment a Vercel

Ver [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md)

## 📝 Notas

- `.venv` está en `.gitignore` - se crea localmente
- `serviceAccountKey.json` está en `.gitignore` - agregar manualmente
- `node_modules` está en `.gitignore` - se instala con `npm install`
- `.env` está en `.gitignore` - crear desde `.env.example`

