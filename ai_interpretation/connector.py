# ai_interpretation/connector.py
from typing import Dict, Any, List


class AIInterpretationConnector:
    """Prepara el objeto de datos estructurado y validado para la IA analítica

    (Punto 13 de la Especificación Maestra). Garantiza que la IA nunca calcula ratios,
    sino que recibe datos deterministas para interpretarlos.
    """
    
    @staticmethod
    def build_structured_payload(
        cif: str, 
        balance_summary: Dict[str, float], 
        metrics_summary: Dict[str, Any], 
        anomalies: List[str]
    ) -> Dict[str, Any]:
        return {
            "metadatos_sistema": "Plataforma de Diagnóstico Financiero - Estándar Banco de España",
            "empresa_cif": cif,
            "resumen_balance": balance_summary,
            "ratios_deterministas_calculados": metrics_summary,
            "contradicciones_detectadas": anomalies,
            "instruccion_para_ia": (
                "Actúa como analista financiero senior experto en la Central de Balances. "
                "Interpreta los datos anteriores, explica las implicaciones económicas, "
                "identifica los riesgos principales y formula preguntas incisivas para la dirección."
            )
        }
