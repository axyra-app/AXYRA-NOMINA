# Checklist Final - Sistema de Nómina

## ANTES DE EMPEZAR

- [ ] He leído INICIO.md
- [ ] Entiendo que necesito serviceAccountKey.json
- [ ] Tengo acceso a Firebase Console

---

## PASO 1: FIREBASE SETUP (10 min)

- [ ] 1. Abierto Firebase Console
- [ ] 2. Seleccioné proyecto "axyra-nomina"
- [ ] 3. Fui a Configuración → Cuentas de servicio
- [ ] 4. Hice clic en "Generar clave privada"
- [ ] 5. Descargué el archivo JSON
- [ ] 6. Guardé en: `backend/serviceAccountKey.json`
- [ ] 7. Verifiqué que el archivo existe (3 KB aprox)

---

## PASO 2: INSTALAR DEPENDENCIAS (5 min)

**Opción A - Automático:**
- [ ] 1. Abierto terminal en la carpeta del proyecto
- [ ] 2. Ejecuté: `setup-dev.bat`
- [ ] 3. Esperé a que termine (sin errores)
- [ ] 4. Cerré la terminal

**O Opción B - Manual:**
- [ ] 1. `cd backend && pip install -r requirements.txt`
- [ ] 2. Esperé a que termine
- [ ] 3. `cd ../frontend && npm install`
- [ ] 4. Esperé a que termine

---

## PASO 3: VERIFICAR SETUP (5 min)

- [ ] 1. Abierto terminal en la carpeta del proyecto
- [ ] 2. Ejecuté: `python verificar_sistema.py`
- [ ] 3. Veo mayoría verde (✓)
- [ ] 4. No hay errores críticos (✗)

Si hay errores:
- [ ] Consulté CONFIGURACION.md sección "Problemas Comunes"
- [ ] Resolví el problema

---

## PASO 4: INICIAR BACKEND (2 min)

- [ ] 1. Abierto terminal 1
- [ ] 2. Ejecuté: `cd backend`
- [ ] 3. Ejecuté: `python main.py`
- [ ] 4. Veo mensaje "Uvicorn running on http://0.0.0.0:8000"
- [ ] 5. Sin errores en la terminal

---

## PASO 5: INICIAR FRONTEND (2 min)

- [ ] 1. Abierto terminal 2 (Nueva terminal)
- [ ] 2. Ejecuté: `cd frontend`
- [ ] 3. Ejecuté: `npm run dev`
- [ ] 4. Veo mensaje "Local: http://localhost:5173"
- [ ] 5. Sin errores en la terminal

---

## PASO 6: PROBAR EN NAVEGADOR (3 min)

- [ ] 1. Abierto navegador en http://localhost:5173
- [ ] 2. Veo la página de Landing (Sistema de Nómina Axyra)
- [ ] 3. Puedo hacer clic en "Iniciar Sesión"
- [ ] 4. Cargo la página de login
- [ ] 5. Sin errores en Console (F12 → Console)

---

## SISTEMA OPERATIVO ✓

- [ ] Backend: http://localhost:8000/health = OK
- [ ] Frontend: http://localhost:5173 = Cargando
- [ ] Firebase: Conectado automáticamente

---

## PRÓXIMO: DESARROLLO FRONTEND

Ahora debes implementar las 9 páginas:

- [ ] 1. LoginPage - Formulario de login
- [ ] 2. RegisterPage - Formulario de registro
- [ ] 3. DashboardPage - Panel principal
- [ ] 4. EmployeesPage - Lista de empleados
- [ ] 5. EmployeeFormPage - Crear/editar empleado
- [ ] 6. HoursPage - Registrar horas
- [ ] 7. PayrollPage - Gestión de nóminas
- [ ] 8. ConfigurationPage - Configuración
- [ ] 9. LandingPage - Página inicio

**Guía:** Lee GUIA_FRONTEND_IMPLEMENTATION.js

---

## RECURSOS

| Necesidad | Recurso |
|-----------|---------|
| Empezar | INICIO.md |
| Problemas técnicos | CONFIGURACION.md |
| Status actual | ESTADO_ACTUAL.md |
| Implementar página | GUIA_FRONTEND_IMPLEMENTATION.js |
| Resumen visual | ESTADO_FINAL.txt |
| Testing | test_endpoints.py |
| Verificación | verificar_sistema.py |

---

## NOTAS

```
Si ves errores CORS:
→ El backend ya está configurado
→ Reinicia backend: Ctrl+C y python main.py

Si ves errores de Firebase:
→ Verifica que serviceAccountKey.json existe
→ Verifica que Firebase Console está activo

Si ves errores de timeout:
→ Verifica que ambos (backend y frontend) están corriendo
→ Revisa en diferentes terminales

Si Node falla:
→ Ejecuta: npm cache clean --force
→ Ejecuta: npm install nuevamente
```

---

## ESTADO FINAL

Cuando termines TODOS los pasos anteriores:

✓ Backend corriendo en 8000
✓ Frontend corriendo en 5173
✓ Firebase conectado
✓ Puedes ver la app en navegador
✓ Puedes navegar entre páginas
✓ Listo para empezar desarrollo

---

## ESTIMADO DE TIEMPO

- Setup Firebase: 10 min
- Instalar deps: 5 min
- Verificar: 5 min
- Iniciar: 4 min
- Probar: 3 min
- **TOTAL: 27 minutos aprox**

Después de esto, es puro desarrollo frontend (4-6 horas).

---

**¡Éxito con tu Sistema de Nómina!**
