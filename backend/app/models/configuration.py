"""
Modelos de configuración del sistema
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime


class CompanyConfig(BaseModel):
    """Configuración de la empresa"""
    empresa_nombre: str = Field(..., min_length=1)
    empresa_nit: str = Field(..., min_length=1)
    empresa_direccion: str = Field(..., min_length=1)
    salario_minimo_legal: float = Field(..., gt=0)
    auxilio_transporte: float = Field(default=0, ge=0)
    descuento_salud_porcentaje: float = Field(default=4.0, ge=0, le=100)
    descuento_pension_porcentaje: float = Field(default=4.0, ge=0, le=100)

    class Config:
        from_attributes = True


class HourTypeConfig(BaseModel):
    """Configuración de tipo de hora"""
    nombre: str = Field(..., min_length=1)
    recargo_porcentaje: float = Field(default=0, ge=0)
    aplica_fijo: bool = Field(default=True)
    aplica_temporal: bool = Field(default=True)

    class Config:
        from_attributes = True


class HourConfiguration(BaseModel):
    """Configuración completa de horas y recargas"""
    valor_hora_ordinaria: float = Field(..., gt=0)
    horas_por_config: Dict[str, HourTypeConfig] = Field(default_factory=dict)
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ConfigurationUpdate(BaseModel):
    """Modelo para actualizar configuración"""
    empresa_nombre: Optional[str] = None
    empresa_nit: Optional[str] = None
    empresa_direccion: Optional[str] = None
    salario_minimo_legal: Optional[float] = None
    auxilio_transporte: Optional[float] = None
    descuento_salud_porcentaje: Optional[float] = None
    descuento_pension_porcentaje: Optional[float] = None
    valor_hora_ordinaria: Optional[float] = None
    horas_por_config: Optional[Dict[str, HourTypeConfig]] = None


class SystemSettings(BaseModel):
    """Todas las configuraciones del sistema"""
    company: CompanyConfig
    hours: HourConfiguration
