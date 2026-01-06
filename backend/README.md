# Backend - Sistema de Nómina Axyra Web

Backend FastAPI para la plataforma web de gestión de nóminas.

## Estructura

```
backend/
├── app/
│   ├── api/              # Routers y endpoints
│   ├── business/         # Lógica de negocio (cálculos)
│   ├── config/           # Configuración y constantes
│   ├── database/         # Gestor de Firebase
│   ├── models/           # Modelos Pydantic
│   └── utils/            # Utilidades y validadores
├── main.py               # Punto de entrada
├── requirements.txt      # Dependencias
└── .env.example          # Variables de entorno
```

## Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Copiar archivo de configuración
cp .env.example .env

# Agregar Firebase credentials
# Copiar serviceAccountKey.json en la carpeta backend/
```

## Configuración

1. **Firebase**: Descarga tu archivo `serviceAccountKey.json` desde Firebase Console
2. **Variables de entorno**: Configura `.env` con tus valores
3. **Credenciales**: Coloca `serviceAccountKey.json` en la carpeta `backend/`

## Ejecución

```bash
# Desarrollo
python main.py

# O con uvicorn directamente
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`
- Documentación interactiva: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principales

### Autenticación
- `POST /api/auth/signup` - Registrar usuario
- `POST /api/auth/verify-token` - Verificar token
- `GET /api/auth/me` - Obtener usuario actual

### Empleados
- `POST /api/employees/` - Crear empleado
- `GET /api/employees/` - Listar empleados
- `GET /api/employees/{id}` - Obtener empleado
- `PUT /api/employees/{id}` - Actualizar empleado
- `DELETE /api/employees/{id}` - Eliminar empleado

### Horas
- `POST /api/hours/` - Registrar horas
- `GET /api/hours/{id}` - Obtener horas
- `PUT /api/hours/{id}` - Actualizar horas
- `DELETE /api/hours/{id}` - Eliminar horas

### Nómina
- `POST /api/payroll/calculate/{employee_id}` - Calcular nómina individual
- `POST /api/payroll/batch/{quincena}` - Calcular lote de nóminas
- `GET /api/payroll/batch/{quincena}/{batch_id}` - Obtener lote
- `PUT /api/payroll/batch/{quincena}/{batch_id}/status/{status}` - Actualizar estado

## Desarrollo

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=app

# Watch mode
pytest-watch
```
