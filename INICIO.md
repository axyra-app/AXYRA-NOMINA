# Inicio Rápido - Sistema de Nómina Axyra

## Paso 1: Firebase Setup (10 min)

```bash
1. Firebase Console → Tu proyecto
2. Configuración → Cuentas de servicio
3. Generar clave privada → Descargar JSON
4. Guardar como: backend/serviceAccountKey.json
```

**CRÍTICO:** Sin este archivo no funciona nada.

---

## Paso 2: Instalar Dependencias (5 min)

**Opción A - Windows Batch:**
```bash
setup-dev.bat
```

**Opción B - PowerShell:**
```bash
.\setup-dev.ps1
```

**Opción C - Manual:**
```bash
cd backend && pip install -r requirements.txt
cd ../frontend && npm install
```

---

## Paso 3: Iniciar (1 min)

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Abre en navegador:** http://localhost:5173

---

## Verificar que funciona

```bash
# Ver estado completo
python verificar_sistema.py

# Backend health check
curl http://localhost:8000/health

# Frontend debe cargar sin errores
# http://localhost:5173
```

---

## Documentación

- **[CONFIGURACION.md](CONFIGURACION.md)** - Detalles y troubleshooting
- **[ESTADO_ACTUAL.md](ESTADO_ACTUAL.md)** - Qué está listo y qué falta
- **[README.md](README.md)** - Información general

---

## ¡Listo!

Backend en http://localhost:8000  
Frontend en http://localhost:5173  
Firebase conectado automáticamente

[ ] He ejecutado setup-dev.bat
[ ] Tengo Python 3.12+
[ ] Tengo Node.js 18+
[ ] Tengo npm instalado
[ ] Entiendo la arquitectura (leyendo este archivo)
```

---

## 🎯 ESTADO ACTUAL

✅ **Backend:** Completamente arreglado y operativo  
✅ **Frontend:** Configurado y listo  
⏳ **Firebase:** Necesita verificación (5 min)  

---

## 📊 LO QUE SE LOGRÓ HOY

1. ✅ **Corrección de errores GET** - Todos los endpoints arreglados
2. ✅ **Documentación completa** - 10 documentos profesionales
3. ✅ **Scripts de setup** - Inicialización automática
4. ✅ **Suite de pruebas** - Testing automatizado
5. ✅ **Guías paso a paso** - Para cada rol de usuario

---

## 🚀 PRÓXIMO PASO

**EJECUTA AHORA:**
```bash
setup-dev.bat
```

O si prefieres PowerShell:
```powershell
.\setup-dev.ps1
```

**Luego sigue las instrucciones en pantalla.**

---

## 💡 TIPS

✅ El backend y frontend deben correr simultáneamente  
✅ Backend en Terminal 1: `cd backend && python main.py`  
✅ Frontend en Terminal 2: `cd frontend && npm run dev`  
✅ Los logs están en: `backend/logs/app.log`  
✅ Ejecuta pruebas: `python test_endpoints.py`  

---

## 🆘 PROBLEMAS?

1. **"¿Qué hago?"** → Lee [README_INICIO_RAPIDO.md](README_INICIO_RAPIDO.md)
2. **"No funciona X"** → Ve a [PROYECTO_GUIA_COMPLETA.md](PROYECTO_GUIA_COMPLETA.md) → Busca "Solución de Problemas"
3. **"Necesito setup Firebase"** → Lee [FIREBASE_CONFIG_GUIDE.md](FIREBASE_CONFIG_GUIDE.md)
4. **"Quiero entender el código"** → Lee [FLUJOS_Y_ARQUITECTURA.md](FLUJOS_Y_ARQUITECTURA.md)

---

## 🎓 APRENDE LA ESTRUCTURA

```
Tu Sistema de Nómina tiene 3 partes:

1. FRONTEND (React + Vite)
   ├─ Interfaz visual
   ├─ Login/Signup
   ├─ Dashboard
   └─ Corre en: http://localhost:5173

2. BACKEND (FastAPI + Python)
   ├─ API REST
   ├─ Autenticación JWT
   ├─ Lógica de nómina
   └─ Corre en: http://localhost:8000

3. BASE DE DATOS (Firebase)
   ├─ Realtime Database
   ├─ Autenticación
   └─ En: https://axyra-nomina.firebaseio.com
```

---

## 📈 ARQUITECTURA

```
Browser (React)
     ↓ HTTP + JWT
FastAPI Backend
     ↓
Firebase Database
```

Muy simple. Todo está documentado en [FLUJOS_Y_ARQUITECTURA.md](FLUJOS_Y_ARQUITECTURA.md)

---

## 🏁 EMPIEZA

1. 🛠️ Ejecuta: `setup-dev.bat`
2. 📖 Lee: [README_INICIO_RAPIDO.md](README_INICIO_RAPIDO.md)
3. ✅ Sigue: [LISTA_VERIFICACION.md](LISTA_VERIFICACION.md)
4. 🚀 ¡Desarrolla!

---

**¿Listo? ¡Vamos!** 🎉

Próximo paso: **Ejecuta `setup-dev.bat` o `setup-dev.ps1`**

---

*Para más información, ver [DOCUMENTACION_INDEX.md](DOCUMENTACION_INDEX.md)*
