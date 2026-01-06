"""
Validadores de negocio
"""

import re
from typing import Tuple
from datetime import datetime


def validar_cedula_colombiana(cedula: str) -> Tuple[bool, str]:
    """
    Valida una cédula colombiana
    
    Args:
        cedula: Número de cédula
    
    Returns:
        tuple: (es_válida, mensaje_error)
    """
    # Remover espacios y caracteres especiales
    cedula = re.sub(r'\D', '', cedula)
    
    if len(cedula) < 5 or len(cedula) > 20:
        return False, "La cédula debe tener entre 5 y 20 dígitos"
    
    if not cedula.isdigit():
        return False, "La cédula solo puede contener dígitos"
    
    return True, "Válido"


def validar_email(email: str) -> Tuple[bool, str]:
    """Valida un email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Email inválido"
    
    return True, "Válido"


def validar_salario(salario: float, salario_minimo: float = 1000000) -> Tuple[bool, str]:
    """Valida un salario"""
    if salario <= 0:
        return False, "El salario debe ser mayor a 0"
    
    if salario < salario_minimo:
        return False, f"El salario no puede ser menor al mínimo (${salario_minimo:,.0f})"
    
    return True, "Válido"


def validar_nombre(nombre: str) -> Tuple[bool, str]:
    """Valida un nombre de empleado"""
    if not nombre or len(nombre.strip()) < 2:
        return False, "El nombre debe tener al menos 2 caracteres"
    
    if len(nombre) > 100:
        return False, "El nombre no puede exceder 100 caracteres"
    
    return True, "Válido"


def validar_porcentaje(porcentaje: float, minimo: float = 0, maximo: float = 100) -> Tuple[bool, str]:
    """Valida un porcentaje"""
    if not isinstance(porcentaje, (int, float)):
        return False, "El porcentaje debe ser un número"
    
    if porcentaje < minimo or porcentaje > maximo:
        return False, f"El porcentaje debe estar entre {minimo} y {maximo}"
    
    return True, "Válido"


def validar_horas_diarias(horas: float, max_horas: float = 24) -> Tuple[bool, str]:
    """Valida horas diarias"""
    if horas < 0:
        return False, "Las horas no pueden ser negativas"
    
    if horas > max_horas:
        return False, f"Las horas no pueden exceder {max_horas} en un día"
    
    return True, "Válido"


def validar_periodo(periodo: str) -> Tuple[bool, str]:
    """Valida un período en formato YYYY-MM"""
    if not re.match(r'^\d{4}-\d{2}$', periodo):
        return False, "El período debe estar en formato YYYY-MM"
    
    try:
        year, month = periodo.split('-')
        year, month = int(year), int(month)
        
        if month < 1 or month > 12:
            return False, "El mes debe estar entre 01 y 12"
        
        if year < 2000 or year > 2100:
            return False, "El año debe estar entre 2000 y 2100"
        
        return True, "Válido"
    except:
        return False, "Período inválido"


def validar_tipo_empleado(tipo: str) -> Tuple[bool, str]:
    """Valida el tipo de empleado"""
    tipos_validos = ['FIJO', 'TEMPORAL', 'CONTRATISTA']
    
    if tipo.upper() not in tipos_validos:
        return False, f"Tipo de empleado debe ser uno de: {', '.join(tipos_validos)}"
    
    return True, "Válido"


def validar_cantidad_dinero(cantidad: float) -> Tuple[bool, str]:
    """Valida que una cantidad de dinero sea válida"""
    if cantidad < 0:
        return False, "La cantidad no puede ser negativa"
    
    # Verificar que no tenga más de 2 decimales
    if len(str(cantidad).split('.')[-1]) > 2:
        return False, "La cantidad solo puede tener máximo 2 decimales"
    
    return True, "Válido"


def validar_fecha(fecha_str: str, formato: str = "%Y-%m-%d") -> Tuple[bool, str]:
    """Valida que una fecha sea válida"""
    try:
        datetime.strptime(fecha_str, formato)
        return True, "Válido"
    except ValueError:
        return False, f"Fecha inválida. Use el formato {formato}"


def validar_rango_numerico(valor: float, minimo: float, maximo: float, nombre: str = "Valor") -> Tuple[bool, str]:
    """Valida que un número esté dentro de un rango"""
    if valor < minimo or valor > maximo:
        return False, f"{nombre} debe estar entre {minimo} y {maximo}"
    
    return True, "Válido"


def validar_no_vacio(valor: str, nombre: str = "Campo") -> Tuple[bool, str]:
    """Valida que un campo no esté vacío"""
    if not valor or len(str(valor).strip()) == 0:
        return False, f"{nombre} no puede estar vacío"
    
    return True, "Válido"


# Alias para compatibilidad hacia atrás
def validar_horas(horas: float, max_horas: float = 24) -> Tuple[bool, str]:
    """Alias para validar_horas_diarias"""
    return validar_horas_diarias(horas, max_horas)


def validar_horas_trabajo(horas_data: dict) -> Tuple[bool, str]:
    """
    Valida un registro de horas de trabajo según legislación colombiana
    
    Límites diarios:
    - Horas ordinarias: máximo 12
    - Recargo nocturno: máximo 8
    - Recargo dominical: máximo 8
    - Horas extras: máximo 4 cada una
    - Total de horas: máximo 24
    
    Args:
        horas_data: Dict con los tipos de horas
    
    Returns:
        tuple: (es_válido, mensaje_error)
    """
    
    # Extraer datos
    horas_ordinarias = horas_data.get('horas_ordinarias', 0)
    recargo_nocturno = horas_data.get('recargo_nocturno', 0)
    recargo_diurno_dominical = horas_data.get('recargo_diurno_dominical', 0)
    recargo_nocturno_dominical = horas_data.get('recargo_nocturno_dominical', 0)
    hora_extra_diurna = horas_data.get('hora_extra_diurna', 0)
    hora_extra_nocturna = horas_data.get('hora_extra_nocturna', 0)
    hora_diurna_dominical = horas_data.get('hora_diurna_dominical_o_festivo', 0)
    hora_extra_diurna_dominical = horas_data.get('hora_extra_diurna_dominical_o_festivo', 0)
    hora_extra_nocturna_dominical = horas_data.get('hora_extra_nocturna_dominical_o_festivo', 0)
    
    # 1. Validar horas ordinarias
    if horas_ordinarias < 0:
        return False, "Horas ordinarias no pueden ser negativas"
    if horas_ordinarias > 12:
        return False, f"Horas ordinarias máximo 12 (recibidas: {horas_ordinarias})"
    
    # 2. Validar recargos nocturnos
    if recargo_nocturno < 0:
        return False, "Recargo nocturno no puede ser negativo"
    if recargo_nocturno > 8:
        return False, f"Recargo nocturno máximo 8 horas (recibidas: {recargo_nocturno})"
    
    # 3. Validar recargos dominicales
    if recargo_diurno_dominical < 0:
        return False, "Recargo diurno dominical no puede ser negativo"
    if recargo_diurno_dominical > 8:
        return False, f"Recargo diurno dominical máximo 8 horas (recibidas: {recargo_diurno_dominical})"
    
    if recargo_nocturno_dominical < 0:
        return False, "Recargo nocturno dominical no puede ser negativo"
    if recargo_nocturno_dominical > 8:
        return False, f"Recargo nocturno dominical máximo 8 horas (recibidas: {recargo_nocturno_dominical})"
    
    # 4. Validar horas extra
    if hora_extra_diurna < 0:
        return False, "Hora extra diurna no puede ser negativa"
    if hora_extra_diurna > 4:
        return False, f"Hora extra diurna máximo 4 horas (recibidas: {hora_extra_diurna})"
    
    if hora_extra_nocturna < 0:
        return False, "Hora extra nocturna no puede ser negativa"
    if hora_extra_nocturna > 4:
        return False, f"Hora extra nocturna máximo 4 horas (recibidas: {hora_extra_nocturna})"
    
    # 5. Validar dominicales extra
    if hora_diurna_dominical < 0:
        return False, "Hora dominical diurna no puede ser negativa"
    if hora_diurna_dominical > 8:
        return False, f"Hora dominical diurna máximo 8 horas (recibidas: {hora_diurna_dominical})"
    
    if hora_extra_diurna_dominical < 0:
        return False, "Hora extra dominical diurna no puede ser negativa"
    if hora_extra_diurna_dominical > 4:
        return False, f"Hora extra dominical diurna máximo 4 horas (recibida: {hora_extra_diurna_dominical})"
    
    if hora_extra_nocturna_dominical < 0:
        return False, "Hora extra dominical nocturna no puede ser negativa"
    if hora_extra_nocturna_dominical > 4:
        return False, f"Hora extra dominical nocturna máximo 4 horas (recibida: {hora_extra_nocturna_dominical})"
    
    # 6. Validar total de horas
    total_horas = (
        horas_ordinarias +
        recargo_nocturno +
        recargo_diurno_dominical +
        recargo_nocturno_dominical +
        hora_extra_diurna +
        hora_extra_nocturna +
        hora_diurna_dominical +
        hora_extra_diurna_dominical +
        hora_extra_nocturna_dominical
    )
    
    if total_horas > 24:
        return False, f"Total de horas ({total_horas}) excede máximo permitido de 24 horas por día"
    
    return True, "Validación de horas exitosa"

