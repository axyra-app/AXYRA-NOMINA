"""
Endpoints de cálculo y gestión de nóminas
"""

from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Dict
from app.models.payroll import PayrollCalculation, PayrollBatch
from app.models.hours import Hours
from app.business.calculations import PayrollCalculator
from app.database.firebase import get_firebase
from app.utils.validators import validar_periodo
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/payroll", tags=["payroll"])


@router.post("/calculate/{employee_id}")
async def calculate_employee_payroll(
    employee_id: str,
    periodo: str,
    client_id: str = Query(...),
):
    """
    Calcula la nómina de un empleado específico en un período con validaciones

    Args:
        client_id: ID del cliente
        employee_id: ID del empleado
        periodo: Período (YYYY-MM)

    Returns:
        dict: Cálculo completo de la nómina
    """
    try:
        # Validar período
        periodo_valido, msg_periodo = validar_periodo(periodo)
        if not periodo_valido:
            raise HTTPException(status_code=400, detail=f"Período: {msg_periodo}")
        
        # Validar employee_id
        if not employee_id or len(employee_id) < 1:
            raise HTTPException(status_code=400, detail="employee_id es requerido")
        
        firebase = get_firebase()

        # Obtener datos del empleado
        employee_path = f"clients/{client_id}/employees/{employee_id}"
        employee = firebase.read_data(employee_path)

        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )

        # Obtener configuración del cliente
        company_config = firebase.read_data(f"clients/{client_id}/config/company") or {}
        hours_config = firebase.read_data(f"clients/{client_id}/config/hours") or {}

        # Combinar configuración
        config = {
            **company_config,
            **hours_config,
        }

        # Obtener horas registradas en el período
        hours_query = firebase.read_data(f"clients/{client_id}/hours")
        horas_empleado = {}

        if hours_query:
            for hora_data in (hours_query if isinstance(hours_query, list) else [hours_query]):
                if (
                    hora_data.get("employee_id") == employee_id
                    and hora_data.get("quincena") == periodo
                ):
                    horas_empleado = hora_data
                    break

        # Si no hay registro de horas, usar ceros
        if not horas_empleado:
            horas_empleado = {
                "horas_ordinarias": 0,
                "recargo_nocturno": 0,
                "recargo_diurno_dominical": 0,
                "recargo_nocturno_dominical": 0,
                "hora_extra_diurna": 0,
                "hora_extra_nocturna": 0,
                "hora_diurna_dominical_o_festivo": 0,
                "hora_extra_diurna_dominical_o_festivo": 0,
                "hora_nocturna_dominical_o_festivo": 0,
                "hora_extra_nocturna_dominical_o_festivo": 0,
            }

        # Crear calculador
        calculator = PayrollCalculator(config)

        # Calcular nómina
        payroll = calculator.calcular_nomina(employee, horas_empleado, periodo)

        return {
            "success": True,
            "data": payroll
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculando nómina: {str(e)}"
        )


@router.post("/batch-calculate")
async def calculate_batch_payroll(
    client_id: str = Query(...),
    periodo: str = Query(...),
    employee_ids: List[str] = Query(None),  # Si es None, calcula para todos
):
    """
    Calcula nómina para múltiples empleados con validaciones

    Args:
        client_id: ID del cliente
        periodo: Período (YYYY-MM)
        employee_ids: Lista de IDs de empleados (opcional)

    Returns:
        dict: Lista de cálculos de nómina
    """
    try:
        # Validar período
        periodo_valido, msg_periodo = validar_periodo(periodo)
        if not periodo_valido:
            raise HTTPException(status_code=400, detail=f"Período: {msg_periodo}")
        
        firebase = get_firebase()

        # Obtener todos los empleados si no se especifican
        if not employee_ids:
            employees_data = firebase.read_data(f"clients/{client_id}/employees")
            employee_ids = [e["id"] for e in (employees_data.values() if isinstance(employees_data, dict) else [employees_data])]

        # Obtener configuración del cliente
        company_config = firebase.read_data(f"clients/{client_id}/config/company") or {}
        hours_config = firebase.read_data(f"clients/{client_id}/config/hours") or {}

        config = {
            **company_config,
            **hours_config,
        }

        calculator = PayrollCalculator(config)
        payrolls = []

        # Calcular nómina para cada empleado
        for emp_id in employee_ids:
            employee = firebase.read_data(f"clients/{client_id}/employees/{emp_id}")
            if not employee:
                continue

            horas_empleado = {}
            hours_data = firebase.read_data(f"clients/{client_id}/hours")

            if hours_data:
                for hora in (hours_data.values() if isinstance(hours_data, dict) else [hours_data]):
                    if (
                        hora.get("employee_id") == emp_id
                        and hora.get("quincena") == periodo
                    ):
                        horas_empleado = hora
                        break

            if not horas_empleado:
                horas_empleado = {
                    "horas_ordinarias": 0,
                    "recargo_nocturno": 0,
                    "recargo_diurno_dominical": 0,
                    "recargo_nocturno_dominical": 0,
                    "hora_extra_diurna": 0,
                    "hora_extra_nocturna": 0,
                    "hora_diurna_dominical_o_festivo": 0,
                    "hora_extra_diurna_dominical_o_festivo": 0,
                    "hora_nocturna_dominical_o_festivo": 0,
                    "hora_extra_nocturna_dominical_o_festivo": 0,
                }

            payroll = calculator.calcular_nomina(employee, horas_empleado, periodo)
            payrolls.append(payroll)

        # Calcular totales
        total_bruto = sum(p["total_bruto"] for p in payrolls)
        total_descuentos = sum(p["total_descuentos"] for p in payrolls)
        total_neto = sum(p["neto_a_pagar"] for p in payrolls)

        return {
            "success": True,
            "periodo": periodo,
            "cantidad_empleados": len(payrolls),
            "payrolls": payrolls,
            "totales": {
                "total_bruto": round(total_bruto, 2),
                "total_descuentos": round(total_descuentos, 2),
                "total_neto": round(total_neto, 2),
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en cálculo batch: {str(e)}"
        )


@router.get("/history")
async def get_payroll_history(
    client_id: str,
    employee_id: str = None,
    periodo: str = None,
):
    """
    Obtiene el historial de nóminas calculadas

    Args:
        client_id: ID del cliente
        employee_id: Filtro opcional por empleado
        periodo: Filtro opcional por período

    Returns:
        dict: Historial de nóminas
    """
    try:
        firebase = get_firebase()

        payrolls_data = firebase.read_data(f"clients/{client_id}/payroll_history") or {}

        # Filtrar resultados
        results = []
        for payroll in (payrolls_data.values() if isinstance(payrolls_data, dict) else [payrolls_data]):
            if employee_id and payroll.get("employee_id") != employee_id:
                continue
            if periodo and payroll.get("periodo") != periodo:
                continue
            results.append(payroll)

        return {
            "success": True,
            "total": len(results),
            "data": results
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo historial: {str(e)}"
        )


@router.post("/calculate/{employee_id}")
async def calculate_employee_payroll(
    client_id: str,
    employee_id: str,
    quincena: str,
    horas: Dict[str, float]
):
    """Calcula la nómina de un empleado específico"""
    try:
        firebase = get_firebase()
        
        # Obtener datos del empleado
        employee_path = f"clients/{client_id}/employees/{employee_id}"
        employee = firebase.read_data(employee_path)
        
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Empleado no encontrado"
            )
        
        # Obtener configuración del cliente
        config_path = f"clients/{client_id}/config"
        config = firebase.read_data(config_path) or DEFAULT_CONFIG
        
        # Calcular nómina
        payroll_data = calcular_nomina_empleado(
            empleado_id=employee_id,
            nombre=employee["nombre"],
            cedula=employee["cedula"],
            tipo=employee["tipo"],
            salario_base=employee["salario"],
            horas_dict=horas,
            config=config
        )
        
        return payroll_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/batch/{quincena}")
async def calculate_batch_payroll(
    client_id: str,
    quincena: str,
    horas_batch: Dict[str, Dict[str, float]]
):
    """Calcula nómina para múltiples empleados"""
    try:
        firebase = get_firebase()
        
        # Obtener todos los empleados del cliente
        employees_path = f"clients/{client_id}/employees"
        employees_data = firebase.read_data(employees_path)
        
        if not employees_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No hay empleados registrados"
            )
        
        # Obtener configuración
        config_path = f"clients/{client_id}/config"
        config = firebase.read_data(config_path) or DEFAULT_CONFIG
        
        # Calcular nómina para cada empleado
        payrolls = []
        total_neto = 0
        total_bruto = 0
        
        for employee_id, employee in employees_data.items():
            horas = horas_batch.get(employee_id, {})
            
            payroll_data = calcular_nomina_empleado(
                empleado_id=employee_id,
                nombre=employee["nombre"],
                cedula=employee["cedula"],
                tipo=employee["tipo"],
                salario_base=employee["salario"],
                horas_dict=horas,
                config=config
            )
            
            payrolls.append(payroll_data)
            total_neto += payroll_data["neto"]
            total_bruto += payroll_data["total_bruto"]
        
        # Guardar lote en Firebase
        batch_id = str(uuid.uuid4())
        batch_path = f"clients/{client_id}/payroll_batches/{quincena}/{batch_id}"
        
        batch_data = {
            "id": batch_id,
            "client_id": client_id,
            "quincena": quincena,
            "payrolls": payrolls,
            "total_neto": total_neto,
            "total_bruto": total_bruto,
            "cantidad_empleados": len(payrolls),
            "created_at": datetime.now().isoformat(),
            "estado": "BORRADOR"
        }
        
        firebase.write_data(batch_path, batch_data)
        
        return batch_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/batch/{quincena}/{batch_id}")
async def get_payroll_batch(quincena: str, batch_id: str, client_id: str = Query(...)):
    """Obtiene un lote de nómina"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/payroll_batches/{quincena}/{batch_id}"
        batch = firebase.read_data(path)
        
        if not batch:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lote de nómina no encontrado"
            )
        
        return batch
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/batch/{quincena}/{batch_id}/status/{new_status}")
async def update_batch_status(
    quincena: str,
    batch_id: str,
    new_status: str,
    client_id: str = Query(...)
):
    """Actualiza el estado de un lote (BORRADOR, PAGADA, ANULADA)"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/payroll_batches/{quincena}/{batch_id}"
        
        # Validar estado
        valid_statuses = ["BORRADOR", "PAGADA", "ANULADA"]
        if new_status not in valid_statuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado inválido. Debe ser uno de: {', '.join(valid_statuses)}"
            )
        
        firebase.update_data(path, {
            "estado": new_status,
            "updated_at": datetime.now().isoformat()
        })
        
        batch = firebase.read_data(path)
        return batch
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/batches/{quincena}")
async def list_batches_by_quincena(quincena: str, client_id: str = Query(...)):
    """Lista todos los lotes de una quincena"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/payroll_batches/{quincena}"
        batches_data = firebase.read_data(path)
        
        if not batches_data:
            return []
        
        return [batch for batch in batches_data.values()]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
