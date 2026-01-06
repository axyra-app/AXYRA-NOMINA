"""
Constantes del sistema de nómina
Ley Colombiana 2025
"""

# Tipos de horas con sus recargos
TIPOS_HORAS = {
    "ordinarias": 0.00,
    "recargo_nocturno": 0.35,
    "recargo_diurno_dominical": 0.75,
    "recargo_nocturno_dominical": 1.10,
    "hora_extra_diurna": 0.25,
    "hora_extra_nocturna": 0.75,
    "hora_diurna_dominical_o_festivo": 0.80,
    "hora_extra_diurna_dominical_o_festivo": 1.05,
    "hora_nocturna_dominical_o_festivo": 1.10,
    "hora_extra_nocturna_dominical_o_festivo": 1.85,
}

# Configuración por defecto
DEFAULT_CONFIG = {
    "salario_minimo": 1423500,
    "auxilio_transporte": 140606,
    "descuentos": {
        "salud": 4.0,      # 4%
        "pension": 4.0,    # 4%
    }
}

# Tipos de empleados
TIPOS_EMPLEADOS = ["FIJO", "TEMPORAL"]

# Estados de nómina
ESTADOS_NOMINA = ["BORRADOR", "PAGADA", "ANULADA"]

# Horas máximas por período
HORAS_ORDINARIAS_MAXIMAS_QUINCENA = 80  # 4 semanas = 160 horas, quincena = 80
HORAS_EXTRAS_MAXIMAS_SEMANA = 4
HORAS_MAXIMAS_DIA = 8
