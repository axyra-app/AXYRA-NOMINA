"""
Endpoints para gestión de horas trabajadas con autenticación JWT
"""

from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import List, Dict
from app.models.hours import HoursCreate, HoursUpdate, Hours
from app.database.firebase import get_firebase
from app.security_enhanced import get_current_user, UserContext
from app.utils.validators import validar_periodo, validar_horas_trabajo
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/hours", tags=["hours"])


@router.post("/", response_model=Hours, status_code=status.HTTP_201_CREATED)
async def create_hours(
    hours: HoursCreate,
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Registra horas trabajadas para un empleado con validaciones (requiere autenticación JWT)"""
    try:
        # Validar período
        periodo_valido, msg_periodo = validar_periodo(hours.quincena)
        if not periodo_valido:
            raise HTTPException(status_code=400, detail=f"Período: {msg_periodo}")
        
        # Validar que employee_id no esté vacío
        if not hours.employee_id or len(hours.employee_id) < 1:
            raise HTTPException(status_code=400, detail="employee_id es requerido")
        
        # Validar horas completo según legislación colombiana
        horas_validas, msg_horas = validar_horas_trabajo({
            'horas_ordinarias': hours.horas_ordinarias or 0,
            'recargo_nocturno': hours.recargo_nocturno or 0,
            'recargo_diurno_dominical': hours.recargo_diurno_dominical or 0,
            'recargo_nocturno_dominical': hours.recargo_nocturno_dominical or 0,
            'hora_extra_diurna': hours.hora_extra_diurna or 0,
            'hora_extra_nocturna': hours.hora_extra_nocturna or 0,
            'hora_diurna_dominical_o_festivo': hours.hora_diurna_dominical_o_festivo or 0,
            'hora_extra_diurna_dominical_o_festivo': hours.hora_extra_diurna_dominical_o_festivo or 0,
            'hora_extra_nocturna_dominical_o_festivo': hours.hora_extra_nocturna_dominical_o_festivo or 0,
            'hora_nocturna_dominical_o_festivo': hours.hora_nocturna_dominical_o_festivo or 0,
        })
        if not horas_validas:
            raise HTTPException(status_code=400, detail=f"Validación de horas: {msg_horas}")
        
        firebase = get_firebase()
        hours_id = str(uuid.uuid4())
        
        hours_data = {
            "id": hours_id,
            "client_id": client_id,
            "employee_id": hours.employee_id,
            "fecha": hours.fecha,
            "quincena": hours.quincena,
            "horas_ordinarias": hours.horas_ordinarias or 0,
            "recargo_nocturno": hours.recargo_nocturno or 0,
            "recargo_diurno_dominical": hours.recargo_diurno_dominical or 0,
            "recargo_nocturno_dominical": hours.recargo_nocturno_dominical or 0,
            "hora_extra_diurna": hours.hora_extra_diurna or 0,
            "hora_extra_nocturna": hours.hora_extra_nocturna or 0,
            "hora_diurna_dominical_o_festivo": hours.hora_diurna_dominical_o_festivo or 0,
            "hora_extra_diurna_dominical_o_festivo": hours.hora_extra_diurna_dominical_o_festivo or 0,
            "hora_nocturna_dominical_o_festivo": hours.hora_nocturna_dominical_o_festivo or 0,
            "hora_extra_nocturna_dominical_o_festivo": hours.hora_extra_nocturna_dominical_o_festivo or 0,
            "motivo_deuda": hours.motivo_deuda or "",
            "valor_deuda": hours.valor_deuda or 0,
            "notas": hours.notas or "",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "created_by": current_user.uid,
        }
        
        path = f"clients/{client_id}/hours/{hours_id}"
        firebase.write_data(path, hours_data)
        
        logger.info(f"Horas {hours_id} registradas por {current_user.email}")
        return Hours(**hours_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registrando horas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error registrando horas: {str(e)}"
        )


@router.get("/", response_model=List[Hours])
async def list_hours(
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Lista todas las horas registradas de un cliente (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} listando horas del cliente {client_id}")
        
        firebase = get_firebase()
        path = f"clients/{client_id}/hours"
        hours_data = firebase.read_data(path)
        
        if not hours_data:
            return []
        
        hours_list = []
        if isinstance(hours_data, dict):
            for hour_id, hour in hours_data.items():
                if isinstance(hour, dict):
                    try:
                        hours_list.append(Hours(**hour))
                    except Exception as e:
                        logger.warning(f"Error parsing hours record {hour_id}: {str(e)}")
        return hours_list
    except Exception as e:
        logger.error(f"Error listando horas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{hours_id}", response_model=Hours)
async def get_hours(
    hours_id: str,
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Obtiene un registro de horas (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} obteniendo horas {hours_id}")
        
        firebase = get_firebase()
        path = f"clients/{client_id}/hours/{hours_id}"
        hours_data = firebase.read_data(path)
        
        if not hours_data or not isinstance(hours_data, dict):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de horas no encontrado"
            )
        
        return Hours(**hours_data)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error obteniendo horas: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/employee/{employee_id}/quincena/{quincena}")
async def get_hours_by_employee_quincena(
    client_id: str,
    employee_id: str,
    quincena: str
):
    """Obtiene las horas de un empleado en una quincena específica"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/hours"
        all_hours = firebase.read_data(path)
        
        if not all_hours or not isinstance(all_hours, dict):
            return None
        
        # Filtrar por empleado y quincena
        for hours_id, hours_data in all_hours.items():
            if isinstance(hours_data, dict) and (hours_data.get("employee_id") == employee_id and 
                hours_data.get("quincena") == quincena):
                try:
                    return Hours(**hours_data)
                except Exception as e:
                    logger.warning(f"Error parsing hours record {hours_id}: {str(e)}")
        
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{hours_id}", response_model=Hours)
async def update_hours(
    client_id: str,
    hours_id: str,
    hours_update: HoursUpdate
):
    """Actualiza un registro de horas"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/hours/{hours_id}"
        
        # Obtener registro actual
        current = firebase.read_data(path)
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de horas no encontrado"
            )
        
        # Actualizar solo campos proporcionados
        update_data = hours_update.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now().isoformat()
        
        firebase.update_data(path, update_data)
        
        # Obtener datos actualizados
        updated = firebase.read_data(path)
        return Hours(**updated)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{hours_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_hours(hours_id: str, client_id: str = Query(...)):
    """Elimina un registro de horas"""
    try:
        firebase = get_firebase()
        path = f"clients/{client_id}/hours/{hours_id}"
        
        # Verificar que existe
        hours_data = firebase.read_data(path)
        if not hours_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro de horas no encontrado"
            )
        
        firebase.delete_data(path)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
