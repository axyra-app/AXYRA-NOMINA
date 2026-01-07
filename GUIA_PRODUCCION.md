# 🚀 Guía de Producción - Axyra Nómina

**Estado:** Listo para producción  
**Última actualización:** 7 de enero de 2026

---

## 📋 Checklist Pre-Producción

### Backend
- ✅ FastAPI configurado y funcionando
- ✅ JWT authentication implementado
- ✅ Firebase conectado y validado
- ✅ Inicialización de datos de usuario en signup
- ✅ CORS configurado
- ✅ Validaciones de entrada implementadas
- ✅ Manejo de errores profesional
- ✅ Logs estructurados

### Frontend
- ✅ React + Vite optimizado
- ✅ Rutas protegidas implementadas
- ✅ Design responsivo y profesional
- ✅ Términos y Condiciones
- ✅ Política de Privacidad
- ✅ Integración con Firebase Auth
- ✅ Manejo de errores de conexión
- ✅ Datos de demostración removidos

### Base de Datos
- ✅ Firebase Realtime Database configurado
- ✅ Security Rules publicadas
- ✅ Estructura de datos inicializada en signup

---

## 🔧 Pasos para Desplegar en Producción

### 1. Comprar Dominio

1. Ir a un registrador de dominios (GoDaddy, Namecheap, Google Domains, etc.)
2. Buscar y comprar tu dominio (ej: `axyra-nomina.com`, `miempresa-nomina.com`, etc.)
3. Configurar los DNS para apuntar a Vercel

### 2. Configurar DNS en el Registrador

En tu registrador de dominios, crea los siguientes registros:

```
Tipo: A
Nombre: @
Valor: 76.76.19.0

Tipo: CNAME
Nombre: www
Valor: cname.vercel.com

Tipo: CNAME
Nombre: api (opcional para backend separado)
Valor: cname-api.vercel.com
```

### 3. Agregar Dominio a Vercel

1. Ir a [vercel.com](https://vercel.com)
2. Seleccionar el proyecto `axyra-nomina`
3. Ir a Settings → Domains
4. Agregar tu dominio (ej: `axyra-nomina.com`)
5. Vercel automáticamente generará certificado SSL

### 4. Opción A: Backend en Vercel (Recomendado)

Para desplegar el backend en la misma instancia de Vercel:

```bash
# En la raíz del proyecto
git push origin main
```

Vercel detectará automáticamente la estructura monorepo y compilará ambos.

### 4. Opción B: Backend en Servicio Separado (Railway/Render)

Si prefieres un servidor separado:

#### Con Railway.app:
1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar repositorio GitHub
3. Seleccionar rama `main`
4. Seleccionar carpeta `backend`
5. Railway detectará Python y compilará automáticamente
6. Copiar la URL del backend (ej: `https://api-prod-xyz.railway.app`)
7. Actualizar `frontend/.env.production`:
   ```
   VITE_API_URL=https://api-prod-xyz.railway.app
   ```

#### Con Render.com:
1. Crear cuenta en [render.com](https://render.com)
2. Crear nuevo Web Service
3. Conectar repositorio
4. Configurar:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
   - Root directory: `backend`
5. Deploy
6. Copiar URL y actualizar frontend

### 5. Configurar Variables de Entorno en Vercel

En Vercel (Settings → Environment Variables):

```
VITE_API_URL=https://tu-dominio.com
VITE_FIREBASE_API_KEY=tu_api_key
VITE_FIREBASE_AUTH_DOMAIN=axyra-nomina.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=axyra-nomina
VITE_FIREBASE_STORAGE_BUCKET=axyra-nomina.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=tu_sender_id
VITE_FIREBASE_APP_ID=tu_app_id
VITE_FIREBASE_DATABASE_URL=https://axyra-nomina.firebaseio.com
```

### 6. Validar Certificado SSL

1. Ir a tu dominio en navegador
2. Verificar que aparece 🔒 candado verde
3. Si no aparece, esperar 15-30 minutos a que se propague

---

## 🔒 Seguridad en Producción

### Firebase Security Rules

Las security rules ya están configuradas para:
- ✅ Proteger datos de usuarios
- ✅ Permitir lectura/escritura solo a propietarios
- ✅ Registro de auditoría
- ✅ Validaciones de estructura

### HTTPS

- ✅ Certificado SSL automático de Vercel
- ✅ Redirección HTTP → HTTPS automática
- ✅ HSTS habilitado

### Backend

- ✅ JWT tokens con expiración
- ✅ Validaciones de entrada sanitizadas
- ✅ Rate limiting recomendado (agregar en producción)
- ✅ CORS configurado

---

## 📊 Monitoreo en Producción

### Logs

**Vercel:** Settings → Analytics and Monitoring

**Firebase:** Console → Realtime Database → Rules

### Errores de Usuarios

En tu aplicación, implementar:
```javascript
// Sentry para error tracking (opcional)
import * as Sentry from "@sentry/react"

Sentry.init({
  dsn: "https://tu-sentry-dsn@sentry.io/123456"
})
```

### Métricas

- Usar Google Analytics 4
- Monitorear tiempo de carga
- Trackear conversiones

---

## 🚨 Troubleshooting

### Backend no responde en producción

1. Verificar que la URL está correcta en `.env.production`
2. Comprobar que el backend está desplegado
3. Ver logs en Vercel/Railway/Render

```bash
# En local, probar:
curl https://tu-backend.com/health
```

### Errores CORS

Si ves errores de CORS:

```javascript
// El backend debe tener:
cors_origins = ["https://tu-dominio.com"]
```

### Database no conecta

1. Verificar Firebase credentials
2. Comprobar que Firebase está en el mismo proyecto
3. Validar Security Rules

---

## 📞 Soporte en Producción

Para reportar bugs o issues:

```
Email: support@axyra.com
Teléfono: [Tu teléfono]
Sitio web: https://tu-dominio.com
```

---

## ⚡ Optimizaciones Futuras

1. **Caché:** Implementar Redis
2. **CDN:** Cloudflare para assets
3. **Database:** Migrar a PostgreSQL si necesitas más escala
4. **Auth:** Agregar 2FA
5. **Backup:** Automated backups diarios
6. **Testing:** Tests automatizados en CI/CD

---

## 📝 Checklist Final Pre-Lanzamiento

- [ ] Dominio comprado y configurado
- [ ] SSL certificado instalado
- [ ] Variables de entorno configuradas
- [ ] Datos de prueba limpios
- [ ] Términos y Condiciones aceptados
- [ ] Política de Privacidad accesible
- [ ] Todos los endpoints probados
- [ ] Navegación responsive verificada
- [ ] Error handling validado
- [ ] Performance aceptable
- [ ] Backups automáticos configurados
- [ ] Plan de soporte definido

---

## 🎉 ¡Listo para Producción!

Una vez completes este checklist, tu aplicación está lista para usuarios reales.

**Éxito! 🚀**
