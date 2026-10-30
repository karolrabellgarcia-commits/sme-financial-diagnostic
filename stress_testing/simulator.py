# stress_testing/simulator.py
from typing import Dict, Any


class StressTester:
    """Simulador de estrés con separación explícita de hipótesis y costes."""

    @staticmethod
    def simulate_cost_increase_advanced(
        ventas: float, 
        ebitda_original: float, 
        aprovisionamientos_original: float, 
        porcentaje_aumento: float,
        pct_costes_variables: float = 80.0
    ) -> Dict[str, Any]:
        """Simula incremento de materias primas diferenciando parte fija y variable."""
        coste_variable = abs(aprovisionamientos_original) * (pct_costes_variables / 100.0)
        incremento_costes = coste_variable * (porcentaje_aumento / 100.0)
        nuevo_ebitda = ebitda_original - incremento_costes
        nuevo_margen_ebitda = (nuevo_ebitda / ventas * 100.0) if ventas > 0 else 0.0

        return {
            "escenario": f"Incremento de materias primas en +{porcentaje_aumento}% (Asumiendo {pct_costes_variables}% variable)",
            "impacto_euros": round(incremento_costes, 2),
            "nuevo_ebitda": round(nuevo_ebitda, 2),
            "nuevo_margen_ebitda": round(nuevo_margen_ebitda, 2),
            "diferencia_ebitda": round(nuevo_ebitda - ebitda_original, 2),
            "supuestos": f"Aprovisionamientos base: {aprovisionamientos_original:,.2f}€. Base variable afectada: {coste_variable:,.2f}€."
        }

    @staticmethod
    def simulate_sales_drop_advanced(
        ventas_original: float, 
        ebitda_original: float, 
        porcentaje_caida: float,
        apalancamiento_operativo_fijo: float = 30.0
    ) -> Dict[str, Any]:
        """Simula caída de ventas considerando rigidez de costes fijos."""
        factor_caida = porcentaje_caida / 100.0
        nuevas_ventas = ventas_original * (1.0 - factor_caida)
        
        # El EBITDA cae de forma más drástica si hay costes fijos rígidos
        impacto_ebitda_pct = porcentaje_caida * (1.0 + (apalancamiento_operativo_fijo / 100.0))
        nuevo_ebitda = ebitda_original * (1.0 - (impacto_ebitda_pct / 100.0))
        nuevo_margen = (nuevo_ebitda / nuevas_ventas * 100.0) if nuevas_ventas > 0 else 0.0

        return {
            "escenario": f"Caída de ventas de -{porcentaje_caida}%",
            "nuevas_ventas": round(nuevas_ventas, 2),
            "nuevo_ebitda": round(nuevo_ebitda, 2),
            "nuevo_margen_ebitda": round(nuevo_margen, 2),
            "impacto_porcentual_ebitda": round(impacto_ebitda_pct, 2)
        }
