"""
Endpoints de gestión de empleados
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List
from app.models.employee import EmployeeCreate, EmployeeUpdate, Employee
from app.database.firebase import get_firebase
from app.utils.validators import (
    validar_cedula_colombiana,
    validar_nombre,
    validar_salario,
    validar_tipo_empleado
)
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(employee: EmployeeCreate, client_id: str = Query(...)):
    """Crea un nuevo empleado con validaciones"""
    try:
        # Validar cédula
        cedula_valida, msg_cedula = validar_cedula_colombiana(employee.cedula)
        if not cedula_valida:
            raise HTTPException(status_code=400, detail=f"Cédula: {msg_cedula}")
        
        # Validar nombre
        nombre_valido, msg_nombre = validar_nombre(employee.nombre)
        if not nombre_valido:
            raise HTTPException(status_code=400, detail=f"Nombre: {msg_nombre}")
        
        # Validar tipo
        tipo_valido, msg_tipo = validar_tipo_empleado(employee.tipo)
        if not tipo_valido:
            raise HTTPException(status_code=400, detail=f"Tipo: {msg_tipo}")
        
        # Validar salario (mínimo 1000000)
        salario_valido, msg_salario = validar_salario(employee.salario, 1000000)
        if not salario_valido:
            raise HTTPException(status_code=400, detail=f"Salario: {msg_salario}")
        
        firebase = get_firebase()
        employee_id = str(uuid.uuid4())
        
        # Si es TEMPORAL, no debe tener deducciones
        deducir_salud = employee.deducir_salud if employee.tipo == "FIJO" else False
        deducir_pension = employee.deducir_pension if employee.tipo == "FIJO" else False
        deducir_auxilioTransporte = employee.deducir_auxilioTransporte if employee.tipo == "FIJO" else False
        
        employee_data = {
            "id": employee_id,
            "client_id": client_id,
            "nombre": employee.nombre,
            "cedula": employee.cedula,
            "tipo": employee.tipo,
            "salario": employee.salario,
            "comentario": employee.comentario or "",
            "deducir_salud": deducir_salud,
            "deducir_pension": deducir_pension,
            "deducir_auxilioTransporte": deducir_auxilioTransporte,
            "deuda_consumos": employee.deuda_consumos,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }
        
        path = f"clients/{client_id}/employees/{employee_id}"
        firebase.write_data(path, employee_data)
        
        return Employee(**employee_data)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creando empleado: {str(e)}"
        )


@router.get("/", response_model=List[Employee])
async def list_employees(client_id: str = Query(...)):
    """Lista todos los empleados de un cliente"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/employees"
        employees_data = firebase.read_data(path)
        
        if not employees_data:
            return []
        
        employees = [Employee(**employee) for employee in employees_data.values()]
        return employees
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: str, client_id: str = Query(...)):
    """Obtiene un empleado específico"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/employees/{employee_id}"
        employee_data = firebase.read_data(path)
        
        if not employee_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        return Employee(**employee_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{employee_id}", response_model=Employee)
async def update_employee(
    employee_id: str,
    employee_update: EmployeeUpdate,
    client_id: str = Query(...)
):
    """Actualiza un empleado"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/employees/{employee_id}"
        
        # Obtener empleado actual
        current = firebase.read_data(path)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Actualizar solo campos proporcionados
        update_data = employee_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()
        
        # Si el tipo cambió a TEMPORAL, resetear deducciones
        employee_type = update_data.get("tipo", current.get("tipo"))
        if employee_type == "TEMPORAL":
            update_data["deducir_salud"] = False
            update_data["deducir_pension"] = False
            update_data["deducir_auxilioTransporte"] = False
        
        firebase.update_data(path, update_data)
        
        # Obtener datos actualizados
        updated = firebase.read_data(path)
        return Employee(**updated)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: str, client_id: str = Query(...)):
    """Elimina un empleado"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/employees/{employee_id}"
        
        # Verificar que existe
        employee = firebase.read_data(path)
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        firebase.delete_data(path)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
