"""
Modelos de registro de horas
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, date


class HoursBase(BaseModel):
    """Modelo base de horas"""
    employee_id: str
    fecha: date = Field(..., description="Fecha del registro")
    quincena: str  # Formato: "2025-01"
    
    horas_ordinarias: float = Field(default=0, ge=0)
    recargo_nocturno: float = Field(default=0, ge=0)
    recargo_diurno_dominical: float = Field(default=0, ge=0)
    recargo_nocturno_dominical: float = Field(default=0, ge=0)
    hora_extra_diurna: float = Field(default=0, ge=0)
    hora_extra_nocturna: float = Field(default=0, ge=0)
    hora_diurna_dominical_o_festivo: float = Field(default=0, ge=0)
    hora_extra_diurna_dominical_o_festivo: float = Field(default=0, ge=0)
    hora_nocturna_dominical_o_festivo: float = Field(default=0, ge=0)
    hora_extra_nocturna_dominical_o_festivo: float = Field(default=0, ge=0)
    
    motivo_deuda: Optional[str] = None
    valor_deuda: float = Field(default=0, ge=0)
    
    notas: Optional[str] = None


class HoursCreate(HoursBase):
    """Modelo para crear registro de horas"""
    pass


class HoursUpdate(BaseModel):
    """Modelo para actualizar horas"""
    fecha: Optional[date] = None
    
    horas_ordinarias: Optional[float] = None
    recargo_nocturno: Optional[float] = None
    recargo_diurno_dominical: Optional[float] = None
    recargo_nocturno_dominical: Optional[float] = None
    hora_extra_diurna: Optional[float] = None
    hora_extra_nocturna: Optional[float] = None
    hora_diurna_dominical_o_festivo: Optional[float] = None
    hora_extra_diurna_dominical_o_festivo: Optional[float] = None
    hora_nocturna_dominical_o_festivo: Optional[float] = None
    hora_extra_nocturna_dominical_o_festivo: Optional[float] = None
    
    motivo_deuda: Optional[str] = None
    valor_deuda: Optional[float] = None
    
    notas: Optional[str] = None


class Hours(HoursBase):
    """Modelo de horas con metadatos"""
    id: str
    client_id: str
    employee_name: str
    cedula: str
    total_horas: float = Field(default=0, ge=0)
    total_valor: float = Field(default=0, ge=0)
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
