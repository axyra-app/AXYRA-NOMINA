# Frontend - Sistema de Nómina Axyra Web

Frontend React + Tailwind CSS para la plataforma web de gestión de nóminas.

## Estructura

```
frontend/
├── src/
│   ├── components/       # Componentes reutilizables
│   ├── pages/            # Páginas (rutas)
│   ├── services/         # Servicios API
│   ├── hooks/            # Custom hooks
│   ├── context/          # Estado global (Zustand)
│   ├── styles/           # Estilos CSS
│   ├── App.jsx           # Componente principal
│   └── main.jsx          # Punto de entrada
├── vite.config.js        # Configuración Vite
├── tailwind.config.js    # Configuración Tailwind
├── package.json          # Dependencias
└── index.html            # HTML principal
```

## Instalación

```bash
# Instalar dependencias
npm install

# Crear archivo de configuración
cp .env.example .env
```

## Variables de Entorno

Crear archivo `.env`:

```env
VITE_API_URL=http://localhost:8000
VITE_FIREBASE_API_KEY=your_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_auth_domain
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_storage_bucket
VITE_FIREBASE_MESSAGING_SENDER_ID=your_sender_id
VITE_FIREBASE_APP_ID=your_app_id
VITE_FIREBASE_DATABASE_URL=your_database_url
```

## Desarrollo

```bash
# Servidor de desarrollo
npm run dev

# Build para producción
npm run build

# Preview del build
npm run preview
```

## Principales Características

### Autenticación
- Login con Firebase
- Gestión de tokens
- Protección de rutas

### Gestión de Empleados
- CRUD completo
- Búsqueda y filtros
- Validación de datos

### Registro de Horas
- Interfaz intuitiva
- Validación de límites
- Histórico de cambios

### Cálculo de Nóminas
- Cálculo individual
- Cálculo en lote
- Diferentes estados
- Exportación de reportes

### Dashboard
- Estadísticas en tiempo real
- Gráficos de tendencias
- Resumen de nóminas

## Componentes Principales

```
App.jsx
├── LoginPage
├── MainLayout
│   ├── Navbar
│   ├── Sidebar
│   └── Content
│       ├── DashboardPage
│       ├── EmployeesPage
│       ├── HoursPage
│       └── PayrollPage
```
