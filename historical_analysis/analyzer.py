# historical_analysis/analyzer.py
from typing import Dict, List, Any


class HistoricalAnalyzer:
    """Motor de análisis plurianual y detección de patrones históricos

    basado en series temporales de 3 a 5 ejercicios.
    """

    @staticmethod
    def calculate_growth_rates(historical_data: List[Dict[str, float]]) -> List[Dict[str, Any]]:
        """Calcula tasas de crecimiento interanual para Ventas, EBITDA y Deuda.

        historical_data: Lista ordenada cronológicamente de diccionarios con:
        {'ejercicio': 2023, 'ventas': 3500000, 'ebitda': 320000, 'deuda': 1400000, 'caja': 150000}
        """
        evolucion = []
        for i in range(len(historical_data)):
            actual = historical_data[i]
            if i == 0:
                # Año base sin crecimiento interanual calculable
                evolucion.append({
                    "ejercicio": actual["ejercicio"],
                    "ventas": actual["ventas"],
                    "crecimiento_ventas_pct": None,
                    "crecimiento_ebitda_pct": None,
                    "crecimiento_deuda_pct": None
                })
            else:
                anterior = historical_data[i - 1]
                
                # Variaciones porcentuales
                c_ventas = ((actual["ventas"] - anterior["ventas"]) / anterior["ventas"] * 100.0) if anterior["ventas"] > 0 else 0.0
                c_ebitda = ((actual["ebitda"] - anterior["ebitda"]) / anterior["ebitda"] * 100.0) if anterior["ebitda"] != 0 else 0.0
                c_deuda = ((actual["deuda"] - anterior["deuda"]) / anterior["deuda"] * 100.0) if anterior["deuda"] != 0 else 0.0

                evolucion.append({
                    "ejercicio": actual["ejercicio"],
                    "ventas": actual["ventas"],
                    "crecimiento_ventas_pct": round(c_ventas, 2),
                    "crecimiento_ebitda_pct": round(c_ebitda, 2),
                    "crecimiento_deuda_pct": round(c_deuda, 2)
                })

        return evolucion

    @staticmethod
    def detect_historical_patterns(historical_data: List[Dict[str, float]]) -> List[str]:
        """Detecta patrones de alerta anómalos en la serie temporal.

        Ej: Ventas creciendo con EBITDA decreciente, o Deuda creciendo más rápido que las ventas.
        """
        alertas_patron = []
        if len(historical_data) < 2:
            return ["Se requieren al menos 2 ejercicios históricos para detectar patrones."]

        for i in range(1, len(historical_data)):
            ant = historical_data[i - 1]
            act = historical_data[i]
            ej_actual = act.get("ejercicio", i)

            # Patrón 1: Ventas creciendo pero EBITDA disminuyendo
            if act["ventas"] > ant["ventas"] and act["ebitda"] < ant["ebitda"]:
                alertas_patron.append(
                    f"[PATRÓN ANÓMALO - {ej_actual}] Crecimiento sin rentabilidad operativa: "
                    f"Las ventas aumentaron un {((act['ventas']-ant['ventas'])/ant['ventas']*100):.1f}%, "
                    f"pero el EBITDA disminuyó."
                )

            # Patrón 2: Deuda creciendo más rápido que las ventas
            c_ventas = ((act["ventas"] - ant["ventas"]) / ant["ventas"]) if ant["ventas"] > 0 else 0
            c_deuda = ((act["deuda"] - ant["deuda"]) / ant["deuda"]) if ant["deuda"] > 0 else 0
            if c_deuda > c_ventas and c_deuda > 0.05:
                alertas_patron.append(
                    f"[PATRÓN ANÓMALO - {ej_actual}] Apalancamiento desproporcionado: "
                    f"La deuda crece a un ritmo superior a la facturación comercial."
                )

        if not alertas_patron:
            alertas_patron.append("No se han detectado patrones de riesgo grave en la serie histórica evaluada.")

        return alertas_patron
