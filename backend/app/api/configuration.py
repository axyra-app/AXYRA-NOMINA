"""
API Router para Configuraciones del Sistema con autenticación JWT
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from app.models import CompanyConfig, HourConfiguration, ConfigurationUpdate, SystemSettings
from app.database.firebase import get_firebase
from app.security_enhanced import get_current_user, UserContext
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/config",
    tags=["Configuration"],
    responses={404: {"description": "Not found"}},
)


@router.get("/system")
async def get_system_config(
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Obtiene la configuración completa del sistema (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} obteniendo configuración del sistema")
        
        firebase = get_firebase()
        
        # Obtener configuración de empresa
        company_data = firebase.read_data(f"clients/{client_id}/config/company") or {}
        company = {
            "empresa_nombre": company_data.get("empresa_nombre", "Mi Empresa"),
            "empresa_nit": company_data.get("empresa_nit", ""),
            "empresa_direccion": company_data.get("empresa_direccion", ""),
            "salario_minimo_legal": company_data.get("salario_minimo_legal", 1423500),
            "auxilio_transporte": company_data.get("auxilio_transporte", 100000),
            "descuento_salud_porcentaje": company_data.get("descuento_salud_porcentaje", 4.0),
            "descuento_pension_porcentaje": company_data.get("descuento_pension_porcentaje", 4.0),
        }
        
        # Obtener configuración de horas
        hours_data = firebase.read_data(f"clients/{client_id}/config/hours") or {}
        hours = {
            "client_id": client_id,
            "valor_hora_ordinaria": hours_data.get("valor_hora_ordinaria", 1423500 / 240),
            "horas_por_config": hours_data.get("horas_por_config", {}),
            "updated_at": hours_data.get("updated_at"),
        }
        
        return {
            "company": company,
            "hours": hours
        }
        
    except Exception as e:
        logger.error(f"Error obteniendo configuración: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@router.put("/company")
async def update_company_config(
    config: CompanyConfig,
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Actualiza la configuración de la empresa (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} actualizando configuración de empresa")
        
        firebase = get_firebase()
        
        config_data = {
            "empresa_nombre": config.empresa_nombre,
            "empresa_nit": config.empresa_nit,
            "empresa_direccion": config.empresa_direccion,
            "salario_minimo_legal": config.salario_minimo_legal,
            "auxilio_transporte": config.auxilio_transporte,
            "descuento_salud_porcentaje": config.descuento_salud_porcentaje,
            "descuento_pension_porcentaje": config.descuento_pension_porcentaje,
            "updated_by": current_user.uid,
        }
        
        firebase.write_data(f"clients/{client_id}/config/company", config_data)
        logger.info(f"Configuración de empresa actualizada por {current_user.email}")
        
        return {
            "message": "Configuración de empresa actualizada correctamente",
            "data": config_data
        }
        
    except Exception as e:
        logger.error(f"Error actualizando configuración: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/hours")
async def update_hours_config(
    config: HourConfiguration,
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Actualiza la configuración de horas y recargas (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} actualizando configuración de horas")
        
        firebase = get_firebase()
        from datetime import datetime
        
        # Convertir horas_por_config a diccionario si viene como Pydantic models
        horas_dict = {}
        if isinstance(config.horas_por_config, dict):
            for key, value in config.horas_por_config.items():
                if hasattr(value, 'dict'):
                    horas_dict[key] = value.dict()
                else:
                    horas_dict[key] = value
        
        config_data = {
            "valor_hora_ordinaria": config.valor_hora_ordinaria,
            "horas_por_config": horas_dict,
            "updated_at": str(datetime.now()),
            "updated_by": current_user.uid,
        }
        
        firebase.write_data(f"clients/{client_id}/config/hours", config_data)
        logger.info(f"Configuración de horas actualizada por {current_user.email}")
        
        return {
            "message": "Configuración de horas actualizada correctamente",
            "data": config_data
        }
        
    except Exception as e:
        logger.error(f"Error actualizando configuración: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error actualizando config: {str(e)}")


@router.post("/reset-defaults")
async def reset_defaults(
    client_id: str = Query(...),
    current_user: UserContext = Depends(get_current_user)
):
    """Reinicia las configuraciones a valores por defecto (requiere autenticación JWT)"""
    try:
        logger.info(f"Usuario {current_user.email} reiniciando configuración a defaults")
        
        firebase = get_firebase()
        from datetime import datetime
        
        # Valores por defecto
        default_company = {
            "empresa_nombre": "Mi Empresa",
            "empresa_nit": "",
            "empresa_direccion": "",
            "salario_minimo_legal": 1423500,
            "auxilio_transporte": 100000,
            "descuento_salud_porcentaje": 4.0,
            "descuento_pension_porcentaje": 4.0,
        }
        
        default_hours = {
            "valor_hora_ordinaria": 1423500 / 240,
            "horas_por_config": {
                "Ordinarias": {"nombre": "Ordinarias", "recargo_porcentaje": 0, "aplica_fijo": True, "aplica_temporal": True},
                "Recargo Nocturno": {"nombre": "Recargo Nocturno", "recargo_porcentaje": 35, "aplica_fijo": True, "aplica_temporal": True},
                "Recargo Diurno Dominical": {"nombre": "Recargo Diurno Dominical", "recargo_porcentaje": 75, "aplica_fijo": True, "aplica_temporal": True},
                "Recargo Nocturno Dominical": {"nombre": "Recargo Nocturno Dominical", "recargo_porcentaje": 110, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Extra Diurna": {"nombre": "Hora Extra Diurna", "recargo_porcentaje": 25, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Extra Nocturna": {"nombre": "Hora Extra Nocturna", "recargo_porcentaje": 75, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Diurna Dominical o Festivo": {"nombre": "Hora Diurna Dominical o Festivo", "recargo_porcentaje": 80, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Extra Diurna Dominical o Festivo": {"nombre": "Hora Extra Diurna Dominical o Festivo", "recargo_porcentaje": 105, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Nocturna Dominical o Festivo": {"nombre": "Hora Nocturna Dominical o Festivo", "recargo_porcentaje": 110, "aplica_fijo": True, "aplica_temporal": True},
                "Hora Extra Nocturna Dominical o Festivo": {"nombre": "Hora Extra Nocturna Dominical o Festivo", "recargo_porcentaje": 185, "aplica_fijo": True, "aplica_temporal": True},
            },
            "updated_at": str(datetime.now()),
        }
        
        firebase.write_data(f"clients/{client_id}/config/company", default_company)
        firebase.write_data(f"clients/{client_id}/config/hours", default_hours)
        
        return {
            "message": "Configuraciones reiniciadas a valores por defecto",
            "company": default_company,
            "hours": default_hours
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
