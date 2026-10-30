# anomaly_detection/detector.py
from typing import List, Dict, Any


class FinancialAnomalyDetector:
    """Motor de reglas para detectar contradicciones financieras cruzadas

    (Punto 9 de la Especificación Maestra).
    """

    @staticmethod
    def detect_contradictions(
        ventas_crecen: bool, 
        caja_baja: bool, 
        ebitda_sube: bool, 
        existencias_crecen_mas_que_ventas: bool
    ) -> List[str]:
        contradicciones = []
        
        if ventas_crecen and caja_baja:
            contradicciones.append(
                "CASO 1: Crecimiento sin liquidez — Las ventas aumentan pero la tesorería disminuye. "
                "Posible inmovilización en capital circulante (clientes o existencias)."
            )
        
        if ebitda_sube and caja_baja:
            contradicciones.append(
                "CASO 2: Rentabilidad sin generación de caja — El EBITDA mejora pero el efectivo se reduce. "
                "Investigar inversiones, amortizaciones de deuda o tensiones en circulante."
            )
            
        if existencias_crecen_mas_que_ventas:
            contradicciones.append(
                "CASO 3: Acumulación anómala de existencias — Las existencias crecen a un ritmo superior a la facturación, "
                "lo que puede indicar obsolescencia o problemas de rotación."
            )
            
        if not contradicciones:
            contradicciones.append("No se han detectado contradicciones financieras críticas entre los indicadores evaluados.")
            
        return contradicciones
