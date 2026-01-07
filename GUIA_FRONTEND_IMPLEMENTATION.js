// Guía de Implementación - Frontend Pages
// ==========================================
// Este archivo describe exactamente qué debe ir en cada página

// ============ 1. LoginPage ============
// Archivo: frontend/src/pages/auth/LoginPage.jsx
// Debe tener:

<LoginPage>
  Elementos de UI:
    - Header con logo
    - Card con formulario
    - Input: email (validar formato)
    - Input: password (type=password)
    - Button: "Iniciar Sesión"
    - Link: "¿No tienes cuenta? Registrate"
    - Toast para mensajes (error/success)

  Lógica:
    - Usar authService.login(email, password)
    - Si sucede, guardar token en localStorage
    - Redirigir a /dashboard
    - Si falla, mostrar error en Toast

  Estado:
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [loading, setLoading] = useState(false)
</LoginPage>

// ============ 2. RegisterPage ============
// Archivo: frontend/src/pages/auth/RegisterPage.jsx
// Debe tener:

<RegisterPage>
  Elementos:
    - Header con logo
    - Card con formulario
    - Input: email
    - Input: nombre
    - Input: client_id (empresa)
    - Input: password
    - Input: confirm password (validar que coincida)
    - Button: "Registrarse"
    - Link: "¿Ya tienes cuenta? Inicia sesión"
    - Validaciones en tiempo real

  Lógica:
    - Validar que passwords coincidan
    - Validar formato de email
    - Llamar a authService.register(data)
    - Si sucede, mostrar mensaje de éxito
    - Redirigir a /login después de 2 segundos
    - Si falla, mostrar error

  Estado:
    const [form, setForm] = useState({
      email: '',
      nombre: '',
      client_id: '',
      password: '',
      confirmPassword: ''
    })
    const [errors, setErrors] = useState({})
</RegisterPage>

// ============ 3. DashboardPage ============
// Archivo: frontend/src/pages/dashboard/DashboardPage.jsx
// Debe tener:

<DashboardPage>
  Elementos:
    - Greeting: "Bienvenido, {nombre}"
    - 4 Cards con KPIs:
      1. Total empleados (número)
      2. Horas este mes (número)
      3. Nóminas pendientes (número)
      4. Último pago (fecha)
    - Tabla: Últimas transacciones (5 más recientes)
    - Gráfico: Horas registradas (último mes)

  Lógica:
    - GET /employees → contar registros
    - GET /hours?month=current → sumar horas
    - GET /payroll?status=draft → contar pendientes
    - GET /payroll?limit=1 → última nómina
    - GET /hours?limit=10 → tabla de transacciones

  Estado:
    const [stats, setStats] = useState({
      totalEmployees: 0,
      hoursThisMonth: 0,
      pendingPayroll: 0,
      lastPaymentDate: null
    })
    const [recentTransactions, setRecentTransactions] = useState([])
</DashboardPage>

// ============ 4. EmployeesPage ============
// Archivo: frontend/src/pages/employees/EmployeesPage.jsx
// Debe tener:

<EmployeesPage>
  Elementos:
    - Header "Empleados" con Button "Nuevo Empleado"
    - Buscador (por nombre/cédula)
    - Filtros: Tipo (FIJO/TEMPORAL), Activo/Inactivo
    - Tabla con columnas:
      - Nombre
      - Cédula
      - Tipo
      - Salario
      - Acciones (Editar, Eliminar)
    - Modal de confirmación para eliminar
    - Paginación

  Lógica:
    - GET /employees → llenar tabla
    - DELETE /employees/{id} → eliminar
    - Filtrar en frontend o backend
    - Redirigir a /employees/new al crear

  Estado:
    const [employees, setEmployees] = useState([])
    const [filtros, setFiltros] = useState({
      search: '',
      tipo: '',
      activo: true
    })
    const [loading, setLoading] = useState(false)
    const [selectedId, setSelectedId] = useState(null)
</EmployeesPage>

// ============ 5. EmployeeFormPage ============
// Archivo: frontend/src/pages/employees/EmployeeFormPage.jsx
// Debe tener:

<EmployeeFormPage>
  Elementos:
    - Header "Nuevo Empleado" o "Editar Empleado"
    - Formulario con:
      - Input: Nombre *
      - Input: Cédula *
      - Input: Email
      - Input: Cargo
      - Input: Departamento
      - Select: Tipo (FIJO/TEMPORAL) *
      - Input: Salario *
      - Checkboxes:
        - Deducir salud
        - Deducir pensión
        - Deducir auxilio transporte
      - Textarea: Comentarios
      - Button: Guardar
      - Button: Cancelar
    - Validaciones en tiempo real
    - Indicador de errores

  Lógica:
    - Si hay ID en URL, GET /employees/{id} y llenar formulario
    - Si no hay ID, es crear nuevo
    - Validar campos requeridos (*)
    - POST /employees (crear) o PUT /employees/{id} (editar)
    - Si sucede, redirigir a /employees
    - Si falla, mostrar errores

  Estado:
    const [form, setForm] = useState({...})
    const [errors, setErrors] = useState({})
    const [loading, setLoading] = useState(false)
    const { id } = useParams()
</EmployeeFormPage>

// ============ 6. HoursPage ============
// Archivo: frontend/src/pages/hours/HoursPage.jsx
// Debe tener:

<HoursPage>
  Elementos:
    - Header "Horas Trabajadas"
    - Filtros:
      - Select: Empleado
      - Input: Quincena (YYYY-MM)
    - Button: "Registrar Horas"
    - Tabla con columnas:
      - Fecha
      - Empleado
      - Horas ordinarias
      - Recargos
      - Deuda
      - Acciones (Editar, Eliminar)
    - Formulario modal para crear/editar:
      - Select: Empleado
      - Input: Fecha (date picker)
      - Input: Quincena
      - Inputs: Todos los tipos de horas
      - Input: Deuda
      - Input: Motivo deuda
      - Button: Guardar

  Lógica:
    - GET /hours → llenar tabla
    - GET /employees → select de empleados
    - POST /hours → crear registro
    - PUT /hours/{id} → actualizar
    - DELETE /hours/{id} → eliminar

  Estado:
    const [hours, setHours] = useState([])
    const [employees, setEmployees] = useState([])
    const [filtros, setFiltros] = useState({
      employee_id: '',
      quincena: ''
    })
    const [modalOpen, setModalOpen] = useState(false)
</HoursPage>

// ============ 7. PayrollPage ============
// Archivo: frontend/src/pages/payroll/PayrollPage.jsx
// Debe tener:

<PayrollPage>
  Elementos:
    - Header "Nómina"
    - Tabs: "Historial" | "Generar Nómina"
    
    Tab 1 - Historial:
      - Filtro: Quincena (select)
      - Tabla:
        - Empleado
        - Salario base
        - Total bruto
        - Deducciones
        - Neto a pagar
        - Estado
        - Acciones (Ver, PDF, Eliminar)
      - Paginación
    
    Tab 2 - Generar:
      - Input: Quincena a procesar
      - Button: "Generar Nóminas"
      - Spinner mientras procesa
      - Mensaje de éxito
      - Preview de datos a procesar

  Lógica:
    - GET /payroll → historial
    - POST /payroll/calculate → generar
    - GET /payroll/batch?quincena=X → datos del lote
    - Mostrar estados: draft, approved, paid, processed
    - Formatear dinero con 2 decimales

  Estado:
    const [payroll, setPayroll] = useState([])
    const [selectedQuincena, setSelectedQuincena] = useState('')
    const [generatingTab, setGeneratingTab] = useState(false)
    const [currentTab, setCurrentTab] = useState('historial')
</PayrollPage>

// ============ 8. ConfigurationPage ============
// Archivo: frontend/src/pages/configuration/ConfigurationPage.jsx
// Debe tener:

<ConfigurationPage>
  Elementos:
    - Header "Configuración"
    - 3 Secciones:
    
    Section 1 - Empresa:
      - Input: Nombre empresa
      - Input: NIT
      - Input: Dirección
      - Input: Ciudad
      - Input: Teléfono
      - Input: Email
      - Input: Logo URL (opcional)
    
    Section 2 - Horas:
      - Input: Día de inicio de quincena
      - Input: Horas diarias
      - Input: Valor hora ordinaria
      - Input: Valor hora dominical
      - Checkbox: Auto actualizar
    
    Section 3 - Deducciones:
      - Input: % Salud
      - Input: % Pensión
      - Input: Auxilio transporte (valor)
      - Input: % Fondo solidario
    
    - Button: "Guardar Cambios"
    - Toast: Confirmación de guardado
    - Spinner mientras guarda

  Lógica:
    - GET /configuration → llenar formulario
    - PUT /configuration → guardar cambios
    - Validar porcentajes (0-100)
    - Validar números positivos
    - Mostrar estado de guardado

  Estado:
    const [config, setConfig] = useState({
      company: {...},
      hours: {...},
      deductions: {...}
    })
    const [loading, setLoading] = useState(false)
    const [isDirty, setIsDirty] = useState(false)
</ConfigurationPage>

// ============ 9. LandingPage ============
// Archivo: frontend/src/pages/auth/LandingPage.jsx
// Debe tener:

<LandingPage>
  Elementos:
    - Header con navegación
    - Hero section:
      - Título: "Sistema de Nómina Axyra"
      - Descripción
      - Button: "Iniciar Sesión"
      - Button: "Registrarse"
    - Features section (4-6 características)
    - Footer con info

  Lógica:
    - Si usuario está autenticado, redirigir a /dashboard
    - Links a /login y /register
</LandingPage>


// ============ DEPENDENCIAS COMUNES ============

// Todos las páginas necesitan:
import { useNavigate } from 'react-router-dom'
import { useAuth } from '@/hooks/useAuth'
import Toast from '@/components/Toast'
import { useState, useEffect } from 'react'

// Para llamadas API:
import * as employeeService from '@/services/employeeService'
import * as hoursService from '@/services/hoursService'
import * as payrollService from '@/services/payrollService'
import * as authService from '@/services/authService'

// Para estado global:
import { useAuthStore } from '@/context/store'


// ============ ESTRUCTURA DE FORMULARIOS ============

// Patrón recomendado:
const handleSubmit = async (e) => {
  e.preventDefault()
  
  // Validar
  const newErrors = validate(form)
  if (Object.keys(newErrors).length > 0) {
    setErrors(newErrors)
    return
  }
  
  try {
    setLoading(true)
    
    if (isEdit) {
      await service.update(id, form)
      Toast.success('Actualizado exitosamente')
    } else {
      await service.create(form)
      Toast.success('Creado exitosamente')
    }
    
    navigate('/back-path')
  } catch (err) {
    Toast.error(err.response?.data?.detail || 'Error al guardar')
    setErrors({ submit: err.message })
  } finally {
    setLoading(false)
  }
}


// ============ PRÓXIMOS PASOS ============

// 1. Copiar esta guía
// 2. Para cada página:
//    - Implementar UI (componentes)
//    - Implementar lógica (estados, efectos)
//    - Implementar API calls
//    - Probar manualmente
// 3. Integración completa
// 4. Testing
// 5. Deploy

// Tiempo estimado: 4-6 horas para todo
