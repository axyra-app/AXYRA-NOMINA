# 🌐 CONFIGURAR DOMINIO PERSONALIZADO EN VERCEL

## Opción 1: Usar un Dominio Personalizado

### Paso 1: Comprar Dominio
- Ir a: Namecheap, GoDaddy, Google Domains, etc.
- Buscar tu dominio (ej: axyra-nomina.com)
- Comprar por 1 año mínimo

### Paso 2: Configurar en Vercel (Frontend)

1. **Vercel Dashboard**
   ```
   Tu Proyecto Frontend → Settings → Domains
   ```

2. **Agregar Dominio**
   - Click "Add Domain"
   - Ingresar: `app.axyra-nomina.com`
   - Click "Add"

3. **Configurar DNS**
   - Vercel te mostrará records a agregar
   - Ir a tu proveedor de dominio
   - Agregar los records DNS de Vercel
   - Esperar 24-48 horas para propagación

### Paso 3: Configurar en Vercel (Backend)

1. **Vercel Dashboard**
   ```
   Tu Proyecto Backend → Settings → Domains
   ```

2. **Agregar Dominio**
   - Click "Add Domain"
   - Ingresar: `api.axyra-nomina.com`
   - Seguir instrucciones de DNS

### Paso 4: Actualizar Variables de Entorno

**Frontend - Vercel Variables**
```
VITE_API_URL=https://api.axyra-nomina.com
```

**Backend - Vercel Variables**
```
ALLOWED_ORIGINS=["https://app.axyra-nomina.com"]
```

---

## Opción 2: Usar Vercel Subdomain (Gratis)

Vercel proporciona automáticamente:
- Frontend: `axyra-nomina-frontend.vercel.app`
- Backend: `axyra-nomina-backend.vercel.app`

No requiere configuración adicional.

---

## Opción 3: Usar Cloudflare (Recomendado)

### Ventajas:
- DNS ultra rápido
- SSL automático
- Cacheo de contenido estático
- DDoS protection gratuito

### Pasos:

1. **Registrar en Cloudflare**
   ```
   https://www.cloudflare.com/
   Sign Up → Agregar sitio
   ```

2. **Cambiar Nameservers**
   - En tu registrador (Namecheap, etc)
   - Cambiar nameservers a los de Cloudflare
   - Esperar 24 horas

3. **Crear Records A**
   ```
   Type: CNAME
   Name: app
   Target: tu-frontend.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)
   
   Type: CNAME
   Name: api
   Target: tu-backend.vercel.app
   TTL: Auto
   Proxy: Proxied (orange cloud)
   ```

4. **Configurar Vercel**
   - En Vercel → Settings → Domains
   - Agregar: `app.axyra-nomina.com`
   - Vercel auto-detectará Cloudflare

---

## SSL/HTTPS

✅ **Automático en Vercel**
- Todos los dominios obtienen SSL gratuito
- Renovación automática
- Toma ~10 minutos en aplicarse

---

## Verificar Configuración

```bash
# Verificar que el dominio apunta a Vercel
nslookup app.axyra-nomina.com

# Verificar certificado SSL
curl -I https://app.axyra-nomina.com

# Verificar API
curl -I https://api.axyra-nomina.com/health
```

---

## Configuración Final Recomendada

```
┌─────────────────────────────────────────────────┐
│          ESTRUCTURA DE DOMINIOS                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  🌐 axyra-nomina.com (raíz)                     │
│     ↓                                            │
│  📱 app.axyra-nomina.com (Frontend)             │
│     ↓                                            │
│  api.axyra-nomina.com (Backend API)             │
│     ↓                                            │
│  docs.axyra-nomina.com (API Docs) [opcional]    │
│     ↓                                            │
│  admin.axyra-nomina.com (Admin) [opcional]      │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## Costos Aproximados

| Concepto | Costo | Frecuencia |
|----------|-------|-----------|
| Dominio | $10-15 | Anual |
| Vercel | $0-20 | Mensual |
| Cloudflare | $0 | - |
| **Total Mínimo** | **~$10** | **Mensual** |

---

## Troubleshooting

### Domain no conecta
- Verificar DNS propagación: `nslookup dominio.com`
- Esperar 24-48 horas
- Verificar records en Cloudflare/Vercel

### SSL no se aplica
- Esperar 10 minutos
- Limpiar caché del navegador
- Reintentar en 1 hora

### API no responde
- Verificar ALLOWED_ORIGINS en Backend
- Verificar variables de entorno
- Revisar logs en Vercel Dashboard

---

## Soporte

- **Vercel Docs**: https://vercel.com/docs/concepts/projects/domains
- **Cloudflare Docs**: https://developers.cloudflare.com/
- **Mi Equipo**: Contactar para soporte
