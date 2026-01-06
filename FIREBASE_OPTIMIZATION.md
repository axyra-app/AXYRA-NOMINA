# 🔐 FIREBASE SECURITY & OPTIMIZATION GUIDE

## Reglas de Seguridad Firebase Recomendadas

```json
{
  "rules": {
    "usuarios": {
      "$uid": {
        ".read": "$uid === auth.uid",
        ".write": "$uid === auth.uid",
        ".validate": "root.child('usuarios').child($uid).exists() || newData.hasChildren(['email', 'nombre'])"
      }
    },
    "empresas": {
      "$clientId": {
        ".read": "root.child('usuarios').child(auth.uid).child('clientId').val() === $clientId",
        ".write": "root.child('usuarios').child(auth.uid).child('clientId').val() === $clientId",
        "empleados": {
          ".indexOn": ["cedula", "nombre", "email", "tipo"]
        },
        "horas": {
          ".indexOn": ["empleadoId", "fecha", "clientId"]
        },
        "nominas": {
          ".indexOn": ["empleadoId", "periodo", "clientId"]
        },
        "configuracion": {
          ".read": true,
          ".write": "root.child('usuarios').child(auth.uid).child('clientId').val() === $clientId"
        }
      }
    }
  }
}
```

## Índices Recomendados en Firebase Console

```
1. usuarios/
   - email (ascending)
   - clientId (ascending)

2. empresas/{clientId}/empleados/
   - cedula (ascending)
   - nombre (ascending)
   - email (ascending)
   - tipo (ascending)
   - activo (ascending)

3. empresas/{clientId}/horas/
   - empleadoId (ascending)
   - fecha (descending)
   - clientId (ascending)

4. empresas/{clientId}/nominas/
   - empleadoId (ascending)
   - periodo (descending)
   - clientId (ascending)
```

## Estructura de Datos Optimizada

```
{
  "usuarios": {
    "uid1": {
      "email": "admin@axyra.com",
      "nombre": "Juan",
      "clientId": "empresa1",
      "rol": "admin",
      "activo": true,
      "createdAt": 1000000
    }
  },
  "empresas": {
    "empresa1": {
      "nombre": "Mi Empresa",
      "nit": "123456789",
      "configuracion": {
        "horasRegulares": 48,
        "diasFeriados": 10,
        "periodoPago": "mensual",
        "tipoNomina": "colombiana"
      },
      "empleados": {
        "empl1": {
          "cedula": "123456789",
          "nombre": "Pedro",
          "email": "pedro@empresa.com",
          "tipo": "FIJO",
          "salario": 1000000,
          "deducir_salud": true,
          "deducir_pension": true,
          "activo": true
        }
      },
      "horas": {
        "hora1": {
          "empleadoId": "empl1",
          "fecha": "2026-01-06",
          "horasRegulares": 8,
          "horasExtras": 0,
          "registradoPor": "uid1",
          "timestamp": 1000000
        }
      },
      "nominas": {
        "nom1": {
          "empleadoId": "empl1",
          "periodo": "2026-01",
          "salarioBruto": 1000000,
          "deducciones": 200000,
          "neto": 800000,
          "estado": "pagada",
          "timestamp": 1000000
        }
      }
    }
  }
}
```

## Límites y Cuotas Firebase

### Realtime Database
- Conexiones simultáneas: 200
- Operaciones lectura/escritura por segundo: Ilimitado
- Tamaño máximo de registro: 16 MB
- Tamaño máximo de base datos: 100 GB (estándar)

### Authentication
- Cuentas activas: Ilimitado
- Operaciones API: $0.065 por 50k operaciones

## Optimización de Rendimiento

### 1. **Indexing**
```javascript
// ✅ BUENO - usa índices
db.ref('empresas').child(clientId).child('empleados')
  .orderByChild('tipo').equalTo('FIJO').on('value', ...)

// ❌ MALO - sin índice
db.ref('empresas').child(clientId).child('empleados')
  .orderByChild('salario').on('value', ...)
```

### 2. **Queries Eficientes**
```javascript
// ✅ BUENO
db.ref('horas')
  .orderByChild('empleadoId')
  .equalTo('empl1')
  .limitToLast(30)

// ❌ MALO
db.ref('horas').on('value', snapshot => {
  // Filtrar en memoria
  snapshot.val().filter(...)
})
```

### 3. **Desconectar Listeners**
```javascript
// IMPORTANTE: Siempre desconectar cuando no se usan
const ref = db.ref('data')
ref.on('value', callback)
// ... usar ...
ref.off('value', callback) // ✅ DESCONECTAR
```

## Monitoreo en Firebase Console

1. **Database → Realtime Database**
   - Revisar conexiones activas
   - Monitorear uso de ancho de banda
   - Verificar límites de operaciones

2. **Storage → Database Usage**
   - Datos almacenados (GB)
   - Descargas (GB)
   - Carga (GB)

3. **Analytics → Real Time**
   - Usuarios activos
   - Eventos más comunes
   - Performance del app

## Backup y Recovery

### Exportar datos
```bash
# Firebase CLI
firebase database:get / > backup.json

# O desde console: Realtime Database → Backup
```

### Restaurar datos
```bash
firebase database:set / backup.json
```

## Backup Automático

Firebase Standard hace backups automáticos:
- Diarios durante 30 días
- Semanales durante 1 año
- Disponibles en Firebase Console

## Seguridad - Mejores Prácticas

✅ **HACER**
- Usar Firebase Authentication
- Validar datos en reglas
- Limitar acceso por clientId
- Usar transacciones para datos críticos
- Revisar logs de seguridad

❌ **NO HACER**
- Exponer admin credentials
- Permitir lectura sin autenticación
- Guardar passwords en plain text
- Escribir datos sin validación
- Usar reglas demasiado permisivas

## Costo Mensual Estimado

Con 100 usuarios simultáneos:
- **Realtime Database**: ~$10-25/mes
- **Authentication**: ~$5/mes
- **Storage** (opcional): ~$5/mes
- **Total**: ~$20-35/mes

(Spark plan es gratuito para desarrollo)

---

**Última actualización:** Enero 6, 2026
