"""
Modelos de nómina y cálculos
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class PayrollDetailItem(BaseModel):
    """Detalle de un concepto de nómina"""
    concepto: str
    valor_base: float
    cantidad: float
    recargo_porcentaje: float
    valor_total_unitario: float
    subtotal: float


class PayrollSummary(BaseModel):
    """Resumen de conceptos de nómina"""
    total_bruto: float
    total_horas: float
    auxilio_transporte: float = 0.0
    descuento_salud: float = 0.0
    descuento_pension: float = 0.0
    deuda: float = 0.0
    neto_a_pagar: float


class PayrollCalculation(BaseModel):
    """Cálculo completo de nómina de un empleado"""
    employee_id: str
    employee_name: str
    cedula: str
    tipo: str
    salario_base: float
    quincena: str
    
    detalle: List[PayrollDetailItem]
    resumen: PayrollSummary
    
    calculated_at: datetime


class PayrollBatch(BaseModel):
    """Lote de nómina para múltiples empleados"""
    client_id: str
    quincena: str
    payrolls: List[PayrollCalculation]
    total_neto: float
    total_bruto: float
    cantidad_empleados: int
    created_at: datetime
