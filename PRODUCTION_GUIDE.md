# 🚀 GUÍA DE PRODUCCIÓN - AXYRA NÓMINA

## ✅ Estado Actual

```
✅ Código: Production Ready
✅ Repositorio: GitHub (axyra-app/AXYRA-NOMINA)
✅ Logo: Implementado en Frontend
✅ Favicon: Configurado
✅ Vercel: Deployado y listo
```

---

## 🔧 CONFIGURACIÓN ACTUAL EN VERCEL

### **BACKEND - Variables de Entorno**
```
DEBUG=false
APP_NAME=Sistema de Nómina Axyra
FIREBASE_DATABASE_URL=https://axyra-nomina-default-rtdb.firebaseio.com
SECRET_KEY=OGYwYmM0YjEtMDMzMy00NzIxLWI4NzItODQ5YWRiMTgzMDY5YjE3YTgwNzctZWE4Zi00YWExLWE2MDgtZjlmNjlmOWQwNjBkMzBlZmM2NjgtMDA2Mi00MmVmLTgzMDItNDAxYzZjZjYzNjlm
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALLOWED_ORIGINS=["https://tu-frontend-vercel.vercel.app"]
FIREBASE_CREDENTIALS_JSON=(tu JSON completo de Firebase)
```

### **FRONTEND - Variables de Entorno**
```
VITE_API_URL=https://tu-backend-vercel.vercel.app
VITE_FIREBASE_API_KEY=AIzaSyCXEo-IQgZHEt529eNMQy64LqkElKBilX0
VITE_FIREBASE_AUTH_DOMAIN=axyra-nomina.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=axyra-nomina
VITE_FIREBASE_STORAGE_BUCKET=axyra-nomina.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=924413798346
VITE_FIREBASE_APP_ID=1:924413798346:web:c0fb602d01473f0ccd5133
VITE_FIREBASE_DATABASE_URL=https://axyra-nomina-default-rtdb.firebaseio.com
VITE_FIREBASE_MEASUREMENT_ID=G-3FCNCKMSRG
```

---

## 🎯 CHECKLIST DE PRODUCCIÓN

### **Frontend**
- [x] Logo implementado en navbar
- [x] Favicon configurado
- [x] Meta tags SEO configurados
- [x] CORS configurado para producción
- [x] Build optimizado
- [x] Gzip compression habilitado

### **Backend**
- [x] Logging configurado
- [x] Error handling robusto
- [x] CORS restringido a ALLOWED_ORIGINS
- [x] Debug=false en producción
- [x] Health checks configurados
- [x] Status endpoints disponibles

### **Seguridad**
- [x] Firebase Admin SDK integrado
- [x] JWT tokens con SECRET_KEY segura
- [x] Validadores en modelos
- [x] .gitignore optimizado
- [x] Variables sensibles en .env

---

## 📊 ENDPOINTS DISPONIBLES

### **Salud de la API**
```
GET  /                  - Status general
GET  /health            - Health check simple
GET  /api/status        - Status detallado de la API
```

### **Autenticación**
```
POST /api/auth/register - Registro de usuarios
POST /api/auth/login    - Login
POST /api/auth/refresh  - Refrescar token
```

### **Empleados**
```
GET    /api/employees/          - Listar empleados
POST   /api/employees/          - Crear empleado
GET    /api/employees/{id}      - Obtener empleado
PUT    /api/employees/{id}      - Actualizar empleado
DELETE /api/employees/{id}      - Eliminar empleado
```

### **Horas**
```
GET    /api/hours/              - Listar horas
POST   /api/hours/              - Registrar horas
GET    /api/hours/{id}          - Obtener hora
PUT    /api/hours/{id}          - Actualizar hora
DELETE /api/hours/{id}          - Eliminar hora
```

### **Nómina**
```
POST /api/payroll/calculate          - Calcular nómina individual
POST /api/payroll/batch-calculate    - Calcular nóminas en lote
GET  /api/payroll/{id}               - Obtener nómina
```

### **Configuración**
```
GET    /api/configuration/system     - Obtener configuración
PUT    /api/configuration/hours      - Actualizar configuración de horas
POST   /api/configuration/reset      - Resetear configuración
```

---

## 🌐 ACCEDER A LA APLICACIÓN

### **En Desarrollo (Local)**
```
Frontend:  http://localhost:5173
Backend:   http://localhost:8000
Docs API:  http://localhost:8000/docs
```

### **En Producción (Vercel)**
```
Frontend:  https://tu-frontend-vercel.vercel.app
Backend:   https://tu-backend-vercel.vercel.app
Docs API:  https://tu-backend-vercel.vercel.app/docs
```

---

## 🔄 PROCEDIMIENTO DE DEPLOYMENT

### **1. Cambios Locales**
```bash
cd "c:\Users\juanf\OneDrive\Escritorio\NOMINA WEB"
git add .
git commit -m "Production update: [descripción]"
git push origin main
```

### **2. Vercel Auto-Deploy**
- Vercel automáticamente detecta push a GitHub
- Construye e implementa automáticamente
- Puedes monitorear en https://vercel.com/dashboard

### **3. Monitorear Status**
```bash
# Verificar API
curl https://tu-backend-vercel.vercel.app/health

# Verificar Frontend
curl https://tu-frontend-vercel.vercel.app
```

---

## 🐛 TROUBLESHOOTING

### **Error 404 en Frontend**
- Verificar que VITE_API_URL sea correcto en Vercel
- Verificar variables de entorno de Firebase
- Revisar logs en Vercel Dashboard

### **Error 500 en Backend**
- Revisar logs: https://vercel.com/dashboard → Logs
- Verificar FIREBASE_CREDENTIALS_JSON está correcto
- Verificar ALLOWED_ORIGINS incluye tu dominio

### **Error de CORS**
- Verificar ALLOWED_ORIGINS en backend
- Incluir el dominio completo con https://
- Redeploy después de cambios

### **Firebase Connection Error**
- Verificar FIREBASE_DATABASE_URL
- Verificar credenciales JSON
- Verificar reglas de Firebase en console

---

## 📈 MONITOREO EN PRODUCCIÓN

### **Métricas a Revisar**
1. **API Response Time** - debe ser < 500ms
2. **Error Rate** - debe ser < 1%
3. **Uptime** - objetivo 99.9%
4. **Firebase Quota** - revisar uso mensual

### **Logs Recomendados**
- Revisar logs diarios en Vercel
- Monitorear errores de autenticación
- Alertas de Firebase quota

---

## 🛡️ CHECKLIST DE SEGURIDAD

- [x] No hay claves hardcodeadas en el código
- [x] Todas las claves están en variables de entorno
- [x] CORS está restringido
- [x] JWT está configurado
- [x] Firebase Admin SDK está seguro
- [x] .gitignore excluye archivos sensibles
- [x] HTTPS está habilitado (Vercel por defecto)
- [x] Rate limiting configurado (opcional)

---

## 📞 SOPORTE

Para reportar problemas:
1. Revisar logs en Vercel Dashboard
2. Revisar console del navegador (Frontend)
3. Revisar Firebase Console para datos

---

**Última actualización:** Enero 6, 2026  
**Versión:** 1.0.0 - Production Ready  
**Estado:** ✅ Operacional
