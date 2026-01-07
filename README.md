# Sistema de Nómina Axyra

**Estado:** Backend Ready | Frontend Ready | Firebase Rules Deployed  
**Versión:** 2.1.0

Sistema de gestión de nómina: FastAPI + React + Firebase

## Inicio Rápido

1. **Lee** [INICIO.md](INICIO.md) - 3 pasos simples

2. **Descarga** `serviceAccountKey.json` desde Firebase Console y coloca en `backend/`

3. **Ejecuta:**
```bash
setup-dev.bat          # Windows
# O
.\setup-dev.ps1        # PowerShell
```

4. **Inicia desarrollo:**
```bash
# Terminal 1
cd backend && python main.py

# Terminal 2
cd frontend && npm run dev
```

## Documentación

- **[INICIO.md](INICIO.md)** - Comienzo rápido
- **[CONFIGURACION.md](CONFIGURACION.md)** - Detalles técnicos y setup

## Endpoints Principales

**Autenticación:**
- `POST /auth/signup` - Registrar
- `POST /auth/login` - Iniciar sesión

**Empleados:**
- `GET /employees` - Listar
- `POST /employees` - Crear
- `PUT /employees/{id}` - Actualizar

**Horas:**
- `GET /hours` - Listar
- `POST /hours` - Registrar

**Nómina:**
- `GET /payroll` - Historial
- `POST /payroll/calculate` - Calcular

Todos requieren JWT token en header: `Authorization: Bearer <token>`

## Desarrollo

```bash
# Tests
python test_endpoints.py

# Backend logs
# Ver en: backend/logs/app.log

# Frontend dev
npm run dev    # http://localhost:5173
```

### Opción Rápida (Recomendado)
```bash
# Ejecutar setup automático
setup-dev.bat  # Windows Batch
.\setup-dev.ps1  # O PowerShell
```

### Documentación de Inicio
- **📖 Empieza aquí:** [README_INICIO_RAPIDO.md](README_INICIO_RAPIDO.md) - 5 min
- **📋 Índice de docs:** [DOCUMENTACION_INDEX.md](DOCUMENTACION_INDEX.md) - Todas las guías
- **✅ Checklist:** [LISTA_VERIFICACION.md](LISTA_VERIFICACION.md) - Paso a paso

---

## ✨ Características

- ✅ Gestión de empleados (FIJO y TEMPORAL)
- ✅ Registro de horas trabajadas
- ✅ Cálculo automático de nómina
- ✅ Deducciones por tipo de empleado
- ✅ Configuración flexible de horas y recargas
- ✅ Autenticación con Firebase
- ✅ Base de datos en tiempo real (Firebase Realtime DB)
- ✅ API RESTful completa
- ✅ Interfaz responsive con Tailwind CSS

---

## 🛠 Stack Técnico

**Backend:**
- FastAPI 0.109.0
- Python 3.11+
- Firebase Admin SDK
- Pydantic para validación

**Frontend:**
- React 18
- Vite
- Tailwind CSS
- Axios

**Base de Datos:**
- Firebase Realtime Database

**Hosting:**
- Vercel (recomendado)

---

## 🚀 Inicio Rápido

### Requisitos
- Python 3.11 o superior
- Node.js 18 o superior
- npm o yarn
- Cuenta de Firebase

### Instalación

**1. Clonar repositorio**
```bash
git clone https://github.com/tu-usuario/nomina-web.git
cd nomina-web
```

**2. Backend**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
# Editar .env con tus credenciales de Firebase
python main.py
```

**3. Frontend**
```bash
cd frontend
npm install
cp .env.example .env.local
# Editar .env.local con tu URL de API
npm run dev
```

**Acceso:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Docs API: http://localhost:8000/docs

---

## 📁 Estructura del Proyecto

```
nomina-web/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   ├── models/        # Modelos Pydantic
│   │   ├── business/      # Lógica de negocio
│   │   ├── database/      # Firebase Manager
│   │   ├── utils/         # Validadores
│   │   └── config/        # Configuración
│   └── serviceAccountKey.json
│
├── frontend/
│   ├── src/
│   │   ├── pages/         # Páginas
│   │   ├── components/    # Componentes
│   │   ├── services/      # API services
│   │   ├── context/       # Context API
│   │   ├── hooks/         # Custom hooks
│   │   └── styles/        # Estilos globales
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.cjs
│
├── .gitignore
├── README.md
└── FIREBASE_SECURITY_RULES.json
```

---

## 📚 Documentación

Para información detallada, ver:
- [Guía de Deployment a Vercel](./VERCEL_DEPLOYMENT_GUIDE.md)
- [Estado Final del Proyecto](./ESTADO_FINAL_PROYECTO.md)
- [Implementación Completa](./IMPLEMENTACION_COMPLETA.md)
- [Guía de Testing](./TESTING_GUIDE.md)

---

## 🔐 Variables de Entorno

### Backend (.env)

```
DEBUG=false
APP_NAME=Sistema de Nómina Axyra
FIREBASE_DATABASE_URL=https://tu-proyecto.firebaseio.com
FIREBASE_CREDENTIALS_PATH=./serviceAccountKey.json
SECRET_KEY=tu-clave-secreta
ALLOWED_ORIGINS=http://localhost:5173,https://tu-frontend.vercel.app
```

### Frontend (.env.local)

```
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

---

## 📊 API Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/employees` | Crear empleado |
| GET | `/api/employees/` | Listar empleados |
| PUT | `/api/employees/{id}` | Actualizar empleado |
| DELETE | `/api/employees/{id}` | Eliminar empleado |
| POST | `/api/hours` | Registrar horas |
| GET | `/api/hours/` | Listar horas |
| POST | `/api/payroll/calculate/{employee_id}` | Calcular nómina |
| POST | `/api/payroll/batch-calculate` | Calcular nómina múltiple |
| GET | `/api/config/system` | Obtener configuración |
| PUT | `/api/config/hours` | Actualizar config horas |

Ver documentación completa en `/docs` (Swagger UI)

---

## 🚀 Deployment

### Vercel (Recomendado)

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Deploy backend
cd backend
vercel --prod

# 4. Deploy frontend
cd frontend
vercel --prod
```

Ver [VERCEL_DEPLOYMENT_GUIDE.md](./VERCEL_DEPLOYMENT_GUIDE.md) para instrucciones detalladas.

---

## 📋 Checklist de Producción

- [x] Backend sin errores de sintaxis
- [x] Frontend compilando correctamente
- [x] Variables de entorno configuradas
- [x] Firebase conectado
- [x] CORS configurado
- [x] Validaciones implementadas
- [x] Manejo de errores global
- [ ] SSL certificado (automático en Vercel)
- [ ] Backups automáticos
- [ ] Monitoring y logging

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

## 👨‍💻 Autor

Juan Francisco  
Enero 2026

---

## 📞 Soporte

Para reportar bugs o solicitar features, abrir un issue en GitHub.

---

## ✅ Estado Actual

**Versión:** 2.0.0  
**Production:** Listo ✅  
**Testing:** Completado ✅  
**Documentación:** Completa ✅  
**Deployment:** Preparado ✅
|----------|-----|--------|
| Frontend | http://localhost:5174 | 5174 |
| Backend | http://localhost:8000 | 8000 |
| API Docs | http://localhost:8000/docs | 8000 |

---

## 📁 Estructura

```
.
├── backend/
│   ├── main.py              # Punto de entrada
│   ├── requirements.txt      # Dependencias Python
│   └── app/
│       ├── api/             # Endpoints (auth, employees, hours, payroll)
│       ├── models/          # Modelos de datos
│       ├── business/        # Lógica de negocio
│       ├── database/        # Conexión Firebase
│       ├── config/          # Configuración
│       └── utils/           # Validaciones
│
└── frontend/
    ├── package.json         # Dependencias Node
    ├── vite.config.js       # Configuración Vite
    ├── tailwind.config.js   # Tailwind CSS
    └── src/
        ├── pages/           # Páginas (Auth, Dashboard, Employees, Hours, Payroll)
        ├── components/      # Componentes reutilizables
        ├── services/        # API y Firebase
        ├── hooks/           # Custom hooks
        ├── context/         # State management
        └── styles/          # Estilos globales
```

---

## 🔧 Variables de Entorno

### Backend - `backend/.env`
```
FIREBASE_DATABASE_URL=https://tu-proyecto.firebaseio.com
```

### Frontend - `frontend/.env`
```
VITE_FIREBASE_DATABASE_URL=https://tu-proyecto.firebaseio.com
```

---

## 📚 Características

### 🔐 Autenticación
- Email/Password
- Sessions persistentes
- Logout automático

### 👥 Empleados
- CRUD completo
- Validación de cédula
- Validación de email
- Histórico de cambios

### ⏰ Horas Trabajadas
- Registro diario
- Máx. 24 horas/día
- Validación de períodos
- Histórico

### 💰 Nóminas
- Cálculo automático
- Validación de datos
- **Exportación a PDF**
- Desglose por concepto

### 📊 Dashboard
- Resumen en tiempo real
- Estadísticas
- Acceso rápido

---

## 🧪 Testing

### Crear un empleado (POST)
```bash
curl -X POST http://localhost:8000/api/employees \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "default-client",
    "nombre": "Juan",
    "apellido": "Pérez",
    "cedula": "12345678",
    "email": "juan@example.com",
    "salario": 1000000,
    "puesto": "Developer"
  }'
```

### Obtener empleados (GET)
```bash
curl http://localhost:8000/api/employees?client_id=default-client
```

### Ver documentación interactiva
```
http://localhost:8000/docs
```

---

## 🔗 Integración Firebase

**BD:** Firebase Realtime Database  
**Auth:** Firebase Authentication  
**Patrón:** Backend proxy (seguridad)

**Estructura de datos:**
```
clients/
└── default-client/
    ├── employees/
    ├── hours/
    └── payroll/
```

---

## 📋 Checklist Final

- [x] Backend API funcionando
- [x] Frontend funcionando
- [x] Firebase Auth configurado
- [x] Realtime Database conectada
- [x] Validaciones implementadas
- [x] Error handling global
- [x] Retry logic
- [x] PDF export
- [x] Docs completada
- [x] Sistema listo para producción

---

## ⚡ Performance

- **Backend:** FastAPI (asincrónico, ultrarrápido)
- **Frontend:** React + Vite (bundling optimizado)
- **Base de datos:** Firebase (cloud-native)
- **Retries:** Exponential backoff (evita sobrecargar)

---

## 💳 Costos

Con 1 cliente (~100 empleados, ~5MB):

- **Firebase Auth:** Gratis hasta 50,000 usuarios
- **Realtime Database:** Gratis hasta 100 conexiones simultáneas
- **Almacenamiento:** Gratis hasta 1GB

**Total: $0/mes** en free tier

---

## 📞 Soporte

Si algo no funciona:

1. Revisa `TROUBLESHOOTING_FIREBASE.md`
2. Verifica las variables `.env`
3. Asegúrate que Firebase Rules estén publicadas
4. Reinicia ambos servidores

---

## 🎯 Próximos Pasos

1. **Testing exhaustivo** - Crear múltiples empleados, horas, nóminas
2. **Validación de datos** - Verificar cálculos correctos
3. **Deployment** - Heroku, AWS, Google Cloud, etc.
4. **Backups** - Configurar backups automáticos Firebase
5. **Monitoreo** - Vigilar uso de cuotas

---

**Versión:** 2.0.0  
**Estado:** ✅ Producción Ready  
**Última actualización:** Enero 2026
