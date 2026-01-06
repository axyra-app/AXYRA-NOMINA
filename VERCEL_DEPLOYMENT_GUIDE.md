# 🚀 Guía de Deployment a Vercel

## Estado: ✅ LISTO PARA PRODUCCIÓN

El backend está completamente funcional y listo para ser desplegado a Vercel.

---

## Paso 1: Preparar el Proyecto

```bash
# 1. Asegúrate de que el código esté actualizado
cd "c:\Users\juanf\OneDrive\Escritorio\NOMINA WEB"
git status

# 2. Verifica que no hay cambios sin guardar
git add .
git commit -m "Backend production-ready: 307, 500, 422 errors fixed"

# 3. Push a tu repositorio
git push origin main  # o tu rama principal
```

---

## Paso 2: Configurar Vercel

### Opción A: Usando Vercel CLI

```bash
# Instalar Vercel CLI
npm i -g vercel

# Login en Vercel
vercel login

# Deploy desde la raíz del proyecto
vercel --cwd backend

# Selecciona opciones:
# - Project name: nomina-web-backend
# - Framework: Other
# - Output directory: ./
# - Build command: (dejar en blanco)
# - Install command: pip install -r requirements.txt
```

### Opción B: Usando Vercel Web

1. Ve a [vercel.com](https://vercel.com)
2. Click en "New Project"
3. Importa tu repositorio de GitHub
4. Configura:
   - **Root Directory:** `backend`
   - **Framework:** Other
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** `./`
   - **Install Command:** `pip install -r requirements.txt`

---

## Paso 3: Configurar Variables de Entorno en Vercel

En el panel de Vercel, ve a "Settings" → "Environment Variables"

Agregar estas variables:

```
DEBUG = false
APP_NAME = Sistema de Nómina Axyra
VERSION = 2.0.0
FIREBASE_DATABASE_URL = https://tu-proyecto.firebaseio.com
FIREBASE_CREDENTIALS_PATH = ./serviceAccountKey.json
SECRET_KEY = [generar-clave-aleatoria-fuerte]
ALLOWED_ORIGINS = https://tu-frontend.vercel.app,https://tunominio.com
```

### Para `FIREBASE_CREDENTIALS_PATH`:
Necesitas subir el archivo `serviceAccountKey.json` a Vercel. Hay varias formas:

**Opción 1: Como variable de entorno (recomendado)**
```
FIREBASE_CREDENTIALS_JSON = {copiar todo el contenido del JSON aquí}
```

Luego modificar `firebase.py`:
```python
import json
import os

if os.getenv('FIREBASE_CREDENTIALS_JSON'):
    cred_dict = json.loads(os.getenv('FIREBASE_CREDENTIALS_JSON'))
    cred = credentials.Certificate(cred_dict)
```

**Opción 2: Subir como archivo en el repositorio**
- Agregar `serviceAccountKey.json` al `.gitignore` del proyecto
- NO subir archivos de credenciales a Git por seguridad
- Usar la Opción 1 en su lugar

---

## Paso 4: Crear archivo `vercel.json`

Crear en la raíz del proyecto backend:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

---

## Paso 5: Verificar Dependencias

```bash
# Asegúrate que requirements.txt tenga todo necesario
cat backend/requirements.txt
```

Debe incluir:
```
fastapi==0.109.0
uvicorn==0.27.0
firebase-admin==6.4.0
pydantic==2.5.3
python-multipart==0.0.6
pydantic-settings==2.1.0
python-dotenv==1.0.0
pydantic-core==2.14.6
httpx==0.25.2
```

---

## Paso 6: Actualizar CORS en Frontend

Una vez que tengas la URL de Vercel (ej: `https://nomina-backend.vercel.app`), actualiza en frontend:

```javascript
// frontend/src/services/api.js
const API_URL = import.meta.env.VITE_API_URL || 
  (process.env.NODE_ENV === 'production' 
    ? 'https://nomina-backend.vercel.app'
    : 'http://localhost:8000')

// O agregar variable de entorno:
// VITE_API_URL=https://nomina-backend.vercel.app
```

---

## Paso 7: Deploy del Frontend

```bash
cd frontend

# Si usas Vercel CLI
vercel

# O subir a Vercel directamente desde el dashboard
# Settings → Environment Variables
# VITE_API_URL = https://tu-backend.vercel.app
```

---

## Verificación Post-Deploy

```bash
# 1. Health check
curl https://tu-backend.vercel.app/health

# 2. Documentación API
https://tu-backend.vercel.app/docs

# 3. Crear un empleado
curl -X POST https://tu-backend.vercel.app/api/employees/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","cedula":"12345678","tipo":"FIJO","salario":2000000}' \
  -G --data-urlencode "client_id=default-client"

# 4. Listar empleados
curl https://tu-backend.vercel.app/api/employees/ \
  -G --data-urlencode "client_id=default-client"
```

---

## Troubleshooting

### Error: "Cannot find module 'fastapi'"
```
Solución: requirements.txt no se instaló correctamente
- Verifica que pip está en PATH
- Ejecuta: pip install -r requirements.txt localmente primero
```

### Error: "Firebase credentials not found"
```
Solución: FIREBASE_CREDENTIALS_JSON no está configurada
- Usa la Opción 1 de variables de entorno
- Copia el contenido completo del JSON
```

### Error: 500 en endpoints
```
Solución: Variables de entorno no configuradas
- Ve a Vercel Dashboard
- Redeploy después de agregar variables
```

### Error: CORS
```
Solución: ALLOWED_ORIGINS no incluye el frontend
- Actualiza: ALLOWED_ORIGINS=https://tu-frontend.vercel.app
- Redeploy
```

---

## Logs en Vercel

Para ver logs en tiempo real:
```bash
vercel logs https://tu-backend.vercel.app --follow
```

O en el dashboard: "Deployments" → Tu deployment → "Logs"

---

## Configuración de Produción Recomendada

```python
# En settings.py para producción:
DEBUG = False  # ✅ Ya configurado en .env
ALLOWED_ORIGINS = [
    "https://tu-dominio.com",
    "https://www.tu-dominio.com",
    "https://app.tu-dominio.com",
]
SECRET_KEY = "genera-una-clave-de-32-caracteres-aleatoria"
```

---

## ✅ Checklist Pre-Deploy

- [ ] `main.py` con `redirect_slashes=False` ✅
- [ ] `requirements.txt` actualizado ✅
- [ ] `vercel.json` creado ✅
- [ ] Variables de entorno configuradas en Vercel
- [ ] Firebase credentials lista (como JSON en variable de entorno)
- [ ] CORS configurado con dominios correctos
- [ ] Frontend apunta a URL correcta del backend
- [ ] Pruebas locales pasadas ✅

---

## 🚀 Deploy Final

```bash
# 1. Commit de cambios
git add .
git commit -m "Deploy production-ready"
git push origin main

# 2. En Vercel, el deploy es automático
# o ejecutar manualmente:
vercel --prod
```

¡Listo! Tu aplicación estará en producción en minutos.

