# sector_benchmarking/benchmarker.py
from typing import Dict, Optional


class SectorBenchmarker:
    """Motor de comparación sectorial y cálculo de impacto económico en euros

    basado en diferencias contra referencias (ej. Banco de España / CNAE).
    """

    @staticmethod
    def calculate_dso_economic_impact(
        dso_empresa: float, dso_sector: float, ventas_anuales: float
    ) -> Dict[str, Optional[float]]:
        """Calcula el capital circulante adicional inmovilizado por exceso de DSO.

        Fórmula: (Ventas anuales / 365) * (DSO empresa - DSO sector)
        """
        if dso_empresa is None or dso_sector is None or ventas_anuales <= 0:
            return {
                "diferencia_dias": None,
                "capital_inmovilizado_euros": None,
                "interpretacion": "Datos insuficientes para calcular impacto económico de cobros.",
            }

        diferencia_dias = dso_empresa - dso_sector
        # Si la empresa cobra más rápido que el sector, la ineficiencia de capital atrapado por desviación negativa es 0 o favorable.
        dias_efecto = max(0.0, diferencia_dias)
        capital_inmovilizado = (ventas_anuales / 365.0) * dias_efecto

        return {
            "diferencia_dias": round(diferencia_dias, 2),
            "capital_inmovilizado_euros": round(capital_inmovilizado, 2),
            "interpretacion": (
                f"La empresa tarda {dso_empresa:.1f} días en cobrar frente a los "
                f"{dso_sector:.1f} días de la mediana del sector. "
                f"Esto genera un capital circulante potencialmente inmovilizado de "
                f"{capital_inmovilizado:,.2f} €."
                if diferencia_dias > 0
                else f"La empresa cobra más rápido que la media del sector (diferencia de {diferencia_dias:.1f} días)."
            ),
        }

    @staticmethod
    def evaluate_short_term_debt_risk(
        deuda_cp_pct: float, limite_sector_cp_pct: float
    ) -> Dict[str, str]:
        """Evalúa el riesgo de concentración de deuda a corto plazo frente al umbral sectorial."""
        if deuda_cp_pct is None or limite_sector_cp_pct is None:
            return {
                "nivel_riesgo": "NO DISPONIBLE",
                "detalle": "Faltan datos de estructura de deuda o referencia sectorial.",
            }

        if deuda_cp_pct > limite_sector_cp_pct:
            return {
                "nivel_riesgo": "CRÍTICO / ALTO",
                "detalle": (
                    f"El {deuda_cp_pct:.1f}% de la deuda vence a corto plazo, "
                    f"superando el límite prudente del sector ({limite_sector_cp_pct:.1f}%)."
                ),
            }
        else:
            return {
                "nivel_riesgo": "CONTROLADO / ESTABLE",
                "detalle": (
                    f"El porcentaje de deuda a corto plazo ({deuda_cp_pct:.1f}%) "
                    f"se encuentra dentro de los márgenes seguros del sector (<= {limite_sector_cp_pct:.1f}%)."
                ),
            }
