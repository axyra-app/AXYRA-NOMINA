# 🔧 Guía de Configuración Vercel - Login Fix

## ❌ Problema Identificado

El login falla en `axyra-nomina.vercel.app` porque:

1. **Frontend**: `VITE_FIREBASE_*` variables son placeholders, no credenciales reales
2. **Backend**: Intenta cargar `serviceAccountKey.json` como archivo (no existe en Vercel)

## ✅ Solución: Actualizar Variables en Vercel

### PASO 1: Obtener Credenciales Firebase Reales

1. Ve a https://console.firebase.google.com
2. Selecciona proyecto `axyra-nomina`
3. Ve a **Configuración del proyecto** (⚙️)
4. Tab **"Cuentas de servicio"**
5. Haz click en **"Generar nueva clave privada"** (descarga JSON)
   - **IMPORTANTE**: Este JSON tiene credenciales sensibles - guárdalo seguro
   - **NUNCA** lo compartir ni pushearlo a git

6. En el mismo proyecto, tab **"Aplicaciones"**, busca tu app web
   - Encontrarás algo así:
   ```javascript
   const firebaseConfig = {
     apiKey: "AIza...",
     authDomain: "axyra-nomina.firebaseapp.com",
     projectId: "axyra-nomina",
     storageBucket: "axyra-nomina.appspot.com",
     messagingSenderId: "123456789",
     appId: "1:123456789:web:abc..."
   };
   ```

### PASO 2: Configurar Frontend en Vercel

Ve a https://vercel.com → Proyecto `axyra-nomina` → Settings → Environment Variables

**Agregar/Actualizar estas variables:**

```
VITE_API_URL = https://axyra-nomina-4o2f.vercel.app
VITE_FIREBASE_API_KEY = AIza... [de firebaseConfig]
VITE_FIREBASE_AUTH_DOMAIN = axyra-nomina.firebaseapp.com
VITE_FIREBASE_PROJECT_ID = axyra-nomina
VITE_FIREBASE_STORAGE_BUCKET = axyra-nomina.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID = 123456789 [de firebaseConfig]
VITE_FIREBASE_APP_ID = 1:123456789:web:abc... [de firebaseConfig]
VITE_FIREBASE_DATABASE_URL = https://axyra-nomina.firebaseio.com
VITE_FIREBASE_MEASUREMENT_ID = G-XXXXXXXXXX [opcional, si lo tienes]
```

> ⚠️ **Reemplaza los valores `[...]` con los reales de tu Firebase Console**

### PASO 3: Configurar Backend en Vercel

Ve a https://vercel.com → Proyecto `axyra-nomina-4o2f` → Settings → Environment Variables

**Agregar/Actualizar estas variables:**

```
DEBUG = false
ENVIRONMENT = production
SECRET_KEY = tu-clave-secreta-aqui-minimo-32-caracteres
ALLOWED_ORIGINS_STR = https://axyra-nomina.vercel.app,https://axyra-nomina-4o2f.vercel.app
FIREBASE_DATABASE_URL = https://axyra-nomina.firebaseio.com
FIREBASE_PROJECT_ID = axyra-nomina
FIREBASE_CREDENTIALS_JSON = [JSON COMPLETO del serviceAccountKey.json]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
RATE_LIMIT_ENABLED = true
LOG_LEVEL = INFO
```

### PASO 4: Preparar FIREBASE_CREDENTIALS_JSON

1. Abre el `serviceAccountKey.json` que descargaste
2. Copia **TODO el contenido JSON** (desde `{` hasta `}`)
3. En Vercel, en variable `FIREBASE_CREDENTIALS_JSON`:
   - Pega todo el JSON en una sola línea
   - O usa la opción de multi-line de Vercel si está disponible
   - ⚠️ **Asegúrate que esté como válido JSON**

**Ejemplo (estructura, NOT real values):**
```
{"type": "service_account", "project_id": "axyra-nomina", ...todo el resto...}
```

### PASO 5: Redeploy

En Vercel:
1. Frontend: Push a rama main O click "Redeploy"
2. Backend: Push a rama main O click "Redeploy"

Espera 2-3 minutos a que termine el deployment.

## 🧪 Test de Login Después

1. Ve a https://axyra-nomina.vercel.app/login
2. Abre **Developer Tools** (F12)
3. Tab **Console** - NO debe haber errores rojos de Firebase
4. Intenta login con email/password
5. En **Network** deberías ver:
   - ✅ POST a `/api/auth/login` con status **200**
   - ❌ NO debe haber 404 o 400 errors

## ⚠️ Errores Comunes

### "Cannot determine language" en Console
- **Causa**: `VITE_FIREBASE_DATABASE_URL` vacía o inválida
- **Solución**: Verifica que sea `https://axyra-nomina.firebaseio.com`

### 404 en `/api/auth/login`
- **Causa**: Backend deployment falló o URL incorrecta
- **Solución**: Verifica `VITE_API_URL = https://axyra-nomina-4o2f.vercel.app`

### CORS Error
- **Causa**: Frontend URL no está en `ALLOWED_ORIGINS_STR` del backend
- **Solución**: Asegúrate que incluye `https://axyra-nomina.vercel.app`

### "Invalid Credentials"
- **Causa**: `FIREBASE_CREDENTIALS_JSON` inválido en backend
- **Solución**: Verifica que sea JSON válido, copia todo el archivo sin editar

## Checklist Final

- [ ] Frontend `VITE_FIREBASE_*` tienen valores reales (NO placeholders)
- [ ] Backend `FIREBASE_CREDENTIALS_JSON` es JSON válido
- [ ] `ALLOWED_ORIGINS_STR` includes `https://axyra-nomina.vercel.app`
- [ ] `VITE_API_URL = https://axyra-nomina-4o2f.vercel.app`
- [ ] Ambos proyectos en Vercel redeployed
- [ ] Console browser NO tiene errores rojos
- [ ] Network tab muestra `POST /api/auth/login` con 200 OK

## 💡 Debugging

Si algo sigue fallando:

1. **Backend logs en Vercel**: Ve a Deployments → click último → "View Logs"
   - Busca si dice `[OK] Firebase initialized successfully`
   
2. **Frontend logs en Browser**:
   ```javascript
   // En console, ejecuta:
   console.log(import.meta.env)
   // Deberías ver VITE_FIREBASE_* con valores reales
   ```

3. **Check Firebase Admin SDK**:
   - En logs, si dice `Firebase credentials loaded from FIREBASE_CREDENTIALS_JSON`
   - Si NO aparece eso, la variable de entorno no llegó

