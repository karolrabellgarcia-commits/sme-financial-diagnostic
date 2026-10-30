"""
narrative_generator.py
----------------------
Módulo de traducción ejecutiva. Recoge los outputs deterministas del motor
financiero y construye el contexto estructurado para que el LLM traduzca 
los datos en un informe comercial y directivo de alto impacto.
"""

from typing import Dict, Any


class ExecutiveTranslator:
    def __init__(self, ratios: Dict[str, Any], diagnosis: Dict[str, Any]):
        self.ratios = ratios
        self.diagnosis = diagnosis

    def build_llm_system_prompt(self) -> str:
        """Define la personalidad y el tono del analista senior de riesgos."""
        return (
            "Actúa como un director de riesgos financieros y consultor estratégico de empresas. "
            "Tu objetivo es redactar un diagnóstico implacable, claro y orientado a la acción "
            "para el dueño de una PYME. No utilices jerga académica aburrida. "
            "Traduce los datos y los euros inmovilizados en consecuencias de negocio reales "
            "y formula preguntas directas y difíciles que el empresario debe resolver con su equipo."
        )

    def build_llm_user_payload(self) -> str:
        """Construye el bloque de datos estructurados para inyectar al LLM."""
        alerts_text = ""
        for alert in self.diagnosis.get("alertas_activadas", []):
            impacto = f" (Impacto estimado de caja: {alert['impacto_caja_eur']} €)" if alert.get("impacto_caja_eur") else ""
            alerts_text += f"- [{alert['gravedad']}] {alert['titulo']}: {alert['detalle']}{impacto}\n"

        return f"""
        DATOS FINANCIEROS CLAVE CALCULADOS:
        - Margen EBITDA: {self.ratios['margen_ebitda_pct']}%
        - Período Medio de Cobro (DSO): {self.ratios['dso_dias']} días
        - Período Medio de Pago (DPO): {self.ratios['dpo_dias']} días
        - Ciclo de Conversión de Caja (CCC): {self.ratios['ccc_dias']} días
        - Deuda Bancaria Total: {self.ratios['deuda_total_eur']} €
        - Concentración de Deuda a Corto Plazo: {self.ratios['concentracion_deuda_cp_pct']}%
        - Caja total atrapada por desviaciones sectoriales: {self.diagnosis['caja_atrapada_total_eur']} €

        ALERTAS DE RIESGO DETECTADAS:
        {alerts_text if alerts_text else "Sin alertas críticas en este bloque."}

        Por favor, genera un informe ejecutivo estructurado en tres secciones obligatorias:
        1. **Diagnóstico de Salud Financiera:** Resumen sin rodeos de la situación de la empresa.
        2. **El Coste de la Ineficiencia:** Explicación en euros del impacto de los desfases de caja o endeudamiento.
        3. **Preguntas Incisivas para la Dirección:** 2 o 3 preguntas punzantes que el empresario debe hacerle a su director financiero esta misma semana.
        """
