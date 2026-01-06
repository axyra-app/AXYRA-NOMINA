"""
Modelos de empleados
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class EmployeeBase(BaseModel):
    """Modelo base de empleado"""
    nombre: str = Field(..., min_length=1, max_length=255)
    cedula: str = Field(..., min_length=5, max_length=20)
    tipo: str = Field(..., pattern="^(FIJO|TEMPORAL)$")
    salario: float = Field(..., gt=0)
    comentario: Optional[str] = None
    
    # Deducciones específicas para empleados
    deducir_salud: bool = Field(default=True)
    deducir_pension: bool = Field(default=True)
    deducir_auxilioTransporte: bool = Field(default=True)
    deuda_consumos: float = Field(default=0, ge=0)
    
    class Config:
        from_attributes = True
    
    @property
    def puede_tener_deducciones(self) -> bool:
        """Solo empleados FIJO pueden tener deducciones"""
        return self.tipo == "FIJO"


class EmployeeCreate(EmployeeBase):
    """Modelo para crear empleado"""
    pass


class EmployeeUpdate(BaseModel):
    """Modelo para actualizar empleado"""
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    salario: Optional[float] = None
    comentario: Optional[str] = None
    deducir_salud: Optional[bool] = None
    deducir_pension: Optional[bool] = None
    deducir_auxilioTransporte: Optional[bool] = None
    deuda_consumos: Optional[float] = None


class Employee(EmployeeBase):
    """Modelo de empleado con metadatos"""
    id: str
    client_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
