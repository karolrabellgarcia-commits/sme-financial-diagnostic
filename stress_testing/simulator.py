# stress_testing/simulator.py
from typing import Dict, Any


class StressTester:
    """Motor matemático determinista para simulación de escenarios de estrés financiero."""

    @staticmethod
    def simulate_cost_increase(
        ventas: float, ebitda_original: float, aprovisionamientos_original: float, porcentaje_aumento: float
    ) -> Dict[str, Any]:
        incremento_costes = abs(aprovisionamientos_original) * (porcentaje_aumento / 100.0)
        nuevo_ebitda = ebitda_original - incremento_costes
        nuevo_margen_ebitda = (nuevo_ebitda / ventas * 100.0) if ventas > 0 else 0.0

        return {
            "escenario": f"Incremento de costes en +{porcentaje_aumento}%",
            "impacto_euros": round(incremento_costes, 2),
            "nuevo_ebitda": round(nuevo_ebitda, 2),
            "nuevo_margen_ebitda": round(nuevo_margen_ebitda, 2),
            "diferencia_ebitda": round(nuevo_ebitda - ebitda_original, 2)
        }

    @staticmethod
    def simulate_sales_drop(
        ventas_original: float, ebitda_original: float, porcentaje_caida: float
    ) -> Dict[str, Any]:
        factor_caida = porcentaje_caida / 100.0
        nuevas_ventas = ventas_original * (1.0 - factor_caida)
        nuevo_ebitda = ebitda_original * (1.0 - factor_caida)
        nuevo_margen = (nuevo_ebitda / nuevas_ventas * 100.0) if nuevas_ventas > 0 else 0.0

        return {
            "escenario": f"Caída de ventas de -{porcentaje_caida}%",
            "nuevas_ventas": round(nuevas_ventas, 2),
            "nuevo_ebitda": round(nuevo_ebitda, 2),
            "nuevo_margen_ebitda": round(nuevo_margen, 2)
        }

    @staticmethod
    def simulate_collection_delay(
        ventas_anuales: float, dias_retraso_adicional: float
    ) -> Dict[str, Any]:
        if ventas_anuales <= 0:
            return {"necesidad_adicional_financiacion": 0.0}

        necesidad_adicional = (ventas_anuales / 365.0) * dias_retraso_adicional
        return {
            "escenario": f"Retraso adicional de cobro de {dias_retraso_adicional} días",
            "necesidad_adicional_financiacion": round(necesidad_adicional, 2),
            "interpretacion": (
                f"Un retraso de {dias_retraso_adicional} días en el cobro a clientes "
                f"exigirá inyectar o financiar {necesidad_adicional:,.2f} € adicionales en circulante."
            )
        }
