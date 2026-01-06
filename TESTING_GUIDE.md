# Guía de Pruebas - Sistema AXYRA Nómina Web

## ✅ Estado Actual del Sistema

El sistema ha sido actualizado con las siguientes correcciones:

### 1. **Correcciones de Sesión**
- ✅ Removido el interceptor que causaba logout automático en errores 401
- ✅ Token de autenticación se mantiene correctamente en localStorage
- ✅ Sesión persiste al recargar la página

### 2. **Correcciones de API**
- ✅ Removidos trailing slashes de todos los servicios (307 redirects eliminados)
- ✅ Manejo correcto de errores 404 en Firebase (retorna datos vacíos en lugar de 500)
- ✅ Todos los endpoints respondiendo correctamente

### 3. **Mejoras de UI**
- ✅ Creada página separada para crear empleados (`/employees/new`)
- ✅ Formulario con validaciones completas
- ✅ Navegación mejorada
- ✅ Todas las rutas protegidas correctamente

---

## 🧪 Pasos de Prueba

### Paso 1: Iniciar el Sistema

#### Terminal 1 - Backend
```bash
cd "c:\Users\juanf\OneDrive\Escritorio\NOMINA WEB\backend"
python main.py
```
Debería ver: `Uvicorn running on http://0.0.0.0:8000`

#### Terminal 2 - Frontend
```bash
cd "c:\Users\juanf\OneDrive\Escritorio\NOMINA WEB\frontend"
npm run dev
```
Debería ver: `http://localhost:5173` - VITE v5.4.21 ready in...

#### Verificación
- Abra: http://localhost:5173
- Debería ver la Landing Page

### Paso 2: Prueba de Autenticación

1. **Registro de Usuario Nuevo**
   - Click en "Registrar" 
   - Ingrese: email y contraseña
   - Click "Registrarse"
   - **Resultado esperado**: Redirige al dashboard

2. **Login**
   - Click en "Login"
   - Ingrese credenciales
   - Click "Iniciar Sesión"
   - **Resultado esperado**: Abre dashboard sin errores

3. **Persistencia de Sesión**
   - Estando en el dashboard, presione F5 (recargar)
   - **Resultado esperado**: Permanece en el dashboard SIN volver al login

### Paso 3: Prueba de Creación de Empleado (CRÍTICA)

1. **Navegar a Empleados**
   - Click en "Empleados" en el menú lateral
   - Debería ver lista de empleados (vacía si es primera vez)

2. **Crear Nuevo Empleado**
   - Click en botón "Registrar Nuevo Empleado"
   - **Debería abrir formulario en `/employees/new`**
   - NO debería recargar la página completa

3. **Llenar Formulario**
   - **Información Personal:**
     - Nombre: "Juan García"
     - Cédula: "1234567890"
   
   - **Información Laboral:**
     - Tipo: "FIJO"
     - Comentario: "Desarrollador Senior"
   
   - **Información Salarial:**
     - Salario: "3000000"
     - Deuda de Consumos: "0"
   
   - **Deducciones:**
     - Marque: Salud, Pensión, Auxilios de Transporte
   
   - Click "Guardar Empleado"

4. **Verificación de Creación**
   - **Resultado esperado 1**: Empleado aparece en lista
   - **Resultado esperado 2**: SESIÓN PERMANECE ACTIVA (esto es lo importante)
   - **Resultado esperado 3**: NO redirige al login
   - **Resultado esperado 4**: Puede crear otro empleado inmediatamente

### Paso 4: Prueba de Validación de Horas

1. **Navegar a Horas**
   - Click en "Horas" en el menú lateral

2. **Intentar Crear Horas Inválidas**
   - Intente ingresar horas que superen los límites:
     - Total > 24 horas/día
     - Horas ordinarias > 12
     - Recargo nocturno > 8
   
   - **Resultado esperado**: Error claro del servidor con validación

### Paso 5: Prueba de Rutas Protegidas

1. **Logout**
   - Haga logout (si hay botón)
   - O cierre sesión manually: `localStorage.removeItem('authToken')`

2. **Intente Acceder a Rutas Protegidas**
   - Intente acceder a: `http://localhost:5173/dashboard`
   - **Resultado esperado**: Redirige a `/login`

---

## 🔍 Verificaciones Técnicas

### Verificar Token en DevTools

En Google Chrome DevTools (F12):
1. Vaya a "Application" → "Local Storage"
2. Debería ver:
   - `authToken`: token JWT de Firebase
   - `user`: objeto JSON con datos del usuario

### Verificar Requests de API

En Google Chrome DevTools (F12), pestaña "Network":
1. Cree un empleado
2. Vea el POST a `/api/employees`
3. **Debería tener**: `Authorization: Bearer [token]`
4. **Respuesta**: 200 OK

### Verificar que NO hay 307 Redirects

En Network tab:
- Todos los requests a `/api/` deberían ser 200, 201, 400, 401, etc.
- NO deberían haber 307 Temporary Redirect

---

## 📋 Checklist de Validación

- [ ] Backend arranca sin errores en puerto 8000
- [ ] Frontend arranca en http://localhost:5173
- [ ] Puede registrarse e ingresar sin problemas
- [ ] Sesión persiste al recargar página (F5)
- [ ] Puede navegar a `/employees`
- [ ] Botón "Registrar Nuevo Empleado" abre formulario (no recarga)
- [ ] Puede llenar y enviar formulario
- [ ] Empleado aparece en lista SIN cerrar sesión
- [ ] Puede crear otro empleado inmediatamente
- [ ] Token está en localStorage
- [ ] NO hay 307 redirects en Network tab
- [ ] Rutas protegidas redirigen al login cuando no autenticado

---

## 🐛 Si Encuentras Problemas

### Problema: "403 Forbidden" al crear empleado
- **Causa**: Reglas de Firebase denegando acceso
- **Solución**: Verificar que `client_id` en request coincida con los datos del usuario

### Problema: "407 Temporary Redirect"
- **Causa**: Aún hay trailing slashes en algunos servicios
- **Solución**: Verificar que routes en `employeeService.js` NO tengan `/` al final

### Problema: Sesión se cierra en cualquier error
- **Causa**: Interceptor aún tiene logout automático
- **Solución**: Asegurar que `api.js` NO tiene logout en error handlers

### Problema: Dashboard en blanco con loading infinito
- **Causa**: Backend retorna 500 en lugar de datos vacíos
- **Solución**: Verificar que `firebase.py` maneja 404 correctamente

### Problema: "Cannot read property 'length' of undefined"
- **Causa**: Servicio retorna undefined en lugar de array
- **Solución**: Agregar `.catch()` en servicios para retornar array vacío

---

## 📞 Debugging

Si necesitas más información de errores, abre la consola del navegador (F12 → Console) y busca:

```javascript
// Ver token
console.log(localStorage.getItem('authToken'))

// Ver usuario
console.log(JSON.parse(localStorage.getItem('user')))

// Ver último error
console.log(localStorage.getItem('lastError'))
```

---

## 🎯 Próximos Pasos

Una vez validado que la creación de empleados funciona:

1. **Crear HoursPage funcional**
   - Similar a EmployeeFormPage pero para horas
   - Validación de límites de horas

2. **Crear PayrollPage funcional**
   - Mostrar cálculos de nómina
   - Generar reportes

3. **Implementar Update/Delete**
   - Editar empleados existentes
   - Eliminar con confirmación

4. **Testing de Integración**
   - Probar flujo completo: crear empleado → registrar horas → calcular nómina

---

**Última actualización**: 2024 - Sistema en fase de pruebas
