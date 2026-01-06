"""
Cálculos de nómina - Lógica de negocio reutilizable
Siguiendo la ley colombiana 2025
"""

from typing import Dict, List
from datetime import datetime


class PayrollCalculator:
    """Calculador completo de nómina colombiana"""

    def __init__(self, config: Dict):
        """
        Inicializa el calculador con configuración

        Args:
            config: Dict con salario_minimo_legal, descuentos, horas config, etc
        """
        self.salario_minimo = config.get("salario_minimo_legal", 1423500)
        self.auxilio_transporte = config.get("auxilio_transporte", 100000)
        self.desc_salud = config.get("descuento_salud_porcentaje", 4.0)
        self.desc_pension = config.get("descuento_pension_porcentaje", 4.0)
        self.horas_config = config.get("horas_por_config", {})
        self.valor_hora_base = config.get("valor_hora_ordinaria", self.salario_minimo / 240)

    def calcular_nomina(self, employee: Dict, horas: Dict, periodo: str) -> Dict:
        """
        Calcula la nómina completa de un empleado

        Args:
            employee: Datos del empleado
            horas: Registro de horas trabajadas
            periodo: Quincena en formato YYYY-MM

        Returns:
            Dict con cálculo completo de nómina
        """

        resultado = {
            "employee_id": employee.get("id"),
            "employee_name": employee.get("nombre"),
            "cedula": employee.get("cedula"),
            "tipo": employee.get("tipo"),
            "salario_base": employee.get("salario"),
            "periodo": periodo,
            "fecha_calculo": datetime.now().isoformat(),
            "detalle": [],
            "total_bruto": 0,
            "auxilio_transporte": 0,
            "descuento_salud": 0,
            "descuento_pension": 0,
            "deuda_consumos": 0,
            "total_descuentos": 0,
            "neto_a_pagar": 0,
        }

        # Calculo de valores por tipo de hora
        horas_detalle = self._calcular_horas(employee, horas)
        resultado["detalle"] = horas_detalle["detalle"]
        resultado["total_bruto"] = horas_detalle["total_valor"]
        resultado["total_horas"] = horas_detalle["total_horas"]

        # Auxilio de transporte
        if employee.get("deducir_auxilioTransporte", True):
            resultado["auxilio_transporte"] = self.auxilio_transporte
            resultado["total_bruto"] += self.auxilio_transporte

        # Descuentos
        base_descuento = employee.get("salario", self.salario_minimo)

        if employee.get("deducir_salud", True):
            resultado["descuento_salud"] = round(
                base_descuento * (self.desc_salud / 100), 2
            )

        if employee.get("deducir_pension", True):
            resultado["descuento_pension"] = round(
                base_descuento * (self.desc_pension / 100), 2
            )

        # Deuda por consumos
        resultado["deuda_consumos"] = employee.get("deuda_consumos", 0)

        # Total descuentos
        resultado["total_descuentos"] = (
            resultado["descuento_salud"]
            + resultado["descuento_pension"]
            + resultado["deuda_consumos"]
        )

        # Neto a pagar
        resultado["neto_a_pagar"] = max(0, resultado["total_bruto"] - resultado["total_descuentos"])

        return resultado

    def _calcular_horas(self, employee: Dict, horas: Dict) -> Dict:
        """Calcula el valor de todas las horas trabajadas"""

        detalle = []
        total_valor = 0
        total_horas = 0

        # Mapeo de campos a tipos de hora
        mapping_horas = {
            "horas_ordinarias": "Ordinarias",
            "recargo_nocturno": "Recargo Nocturno",
            "recargo_diurno_dominical": "Recargo Diurno Dominical",
            "recargo_nocturno_dominical": "Recargo Nocturno Dominical",
            "hora_extra_diurna": "Hora Extra Diurna",
            "hora_extra_nocturna": "Hora Extra Nocturna",
            "hora_diurna_dominical_o_festivo": "Hora Diurna Dominical o Festivo",
            "hora_extra_diurna_dominical_o_festivo": "Hora Extra Diurna Dominical o Festivo",
            "hora_nocturna_dominical_o_festivo": "Hora Nocturna Dominical o Festivo",
            "hora_extra_nocturna_dominical_o_festivo": "Hora Extra Nocturna Dominical o Festivo",
        }

        for campo, tipo_hora in mapping_horas.items():
            cantidad = horas.get(campo, 0)

            if cantidad > 0:
                # Obtener configuración del tipo de hora
                config_hora = self.horas_config.get(tipo_hora, {})
                recargo_pct = config_hora.get("recargo_porcentaje", 0)

                # Valor base por hora
                valor_unitario = self.valor_hora_base
                valor_recargo = valor_unitario * (recargo_pct / 100)
                valor_total_unitario = valor_unitario + valor_recargo
                subtotal = round(cantidad * valor_total_unitario, 2)

                detalle.append({
                    "tipo_hora": tipo_hora,
                    "cantidad": cantidad,
                    "valor_unitario": round(valor_unitario, 2),
                    "recargo_porcentaje": recargo_pct,
                    "valor_recargo": round(valor_recargo, 2),
                    "valor_total_unitario": round(valor_total_unitario, 2),
                    "subtotal": subtotal,
                })

                total_valor += subtotal
                total_horas += cantidad

        return {
            "detalle": detalle,
            "total_valor": round(total_valor, 2),
            "total_horas": round(total_horas, 2),
        }
