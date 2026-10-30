"""
financial_engine.py
-------------------
Motor determinista de análisis financiero y diagnóstico de caja/riesgo.
Diseñado para procesar estados financieros oficiales (Modelo PGC / Registro Mercantil)
y calcular indicadores de gestión, liquidez, ciclo de caja y estructura de pasivo.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FinancialData:
    # Cuenta de Resultados (P&G)
    cifra_negocios: float              # Importe neto de la cifra de negocios
    consumos_explotacion: float        # Compras + Variación de existencias
    gastos_personal: float             # Gastos de personal
    ebitda: float                      # Resultado económico bruto de explotación
    gastos_financieros: float          # Gastos financieros
    resultado_neto: float              # Resultado del ejercicio

    # Balance de Situación (Activo)
    existencias: float                 # Existencias
    clientes: float                    # Deudores comerciales y cuentas a cobrar
    efectivo: float                    # Efectivo y activos líquidos

    # Balance de Situación (Pasivo)
    patrimonio_neto: float             # Fondos propios + subvenciones
    deuda_bancaria_cp: float          # Pasivo corriente con coste (entidades crédito CP)
    deuda_bancaria_lp: float          # Pasivo no corriente con coste (entidades crédito LP)
    proveedores: float                 # Acreedores comerciales y cuentas a pagar


class FinancialDiagnosticEngine:
    def __init__(self, data: FinancialData, vat_rate: float = 0.21):
        """
        Inicializa el motor financiero.
        :param data: Objeto FinancialData con los estados contables.
        :param vat_rate: Tipo de IVA general aplicado para homogeneizar saldos de balance con P&G.
        """
        self.d = data
        self.vat_factor = 1.0 + vat_rate

    def calculate_ratios(self) -> Dict[str, Any]:
        """Calcula los ratios clave de margen, ciclo de caja y liquidez."""
        # Margen EBITDA (%)
        margen_ebitda = (self.d.ebitda / self.d.cifra_negocios * 100) if self.d.cifra_negocios > 0 else 0.0

        # Período Medio de Cobro (DSO - Days Sales Outstanding)
        ventas_con_iva = self.d.cifra_negocios * self.vat_factor
        dso = (self.d.clientes / ventas_con_iva * 365) if ventas_con_iva > 0 else 0.0

        # Período Medio de Pago (DPO - Days Payable Outstanding)
        compras_con_iva = self.d.consumos_explotacion * self.vat_factor
        dpo = (self.d.proveedores / compras_con_iva * 365) if compras_con_iva > 0 else 0.0

        # Dias de Inventario / Rotación de Stock (DIO - Days Inventory Outstanding)
        dio = (self.d.existencias / self.d.consumos_explotacion * 365) if self.d.consumos_explotacion > 0 else 0.0

        # Ciclo de Conversión de Caja (CCC = DSO + DIO - DPO)
        ccc = dso + dio - dpo

        # Cobertura de Intereses (EBITDA / Gastos Financieros)
        cobertura_intereses = (self.d.ebitda / self.d.gastos_financieros) if self.d.gastos_financieros > 0 else 999.0

        # Deuda Bancaria Total
        deuda_total = self.d.deuda_bancaria_cp + self.d.deuda_bancaria_lp

        # Concentración de Deuda a Corto Plazo (%)
        concentracion_cp = (self.d.deuda_bancaria_cp / deuda_total * 100) if deuda_total > 0 else 0.0

        return {
            "margen_ebitda_pct": round(margen_ebitda, 2),
            "dso_dias": round(dso, 1),
            "dpo_dias": round(dpo, 1),
            "dio_dias": round(dio, 1),
            "ccc_dias": round(ccc, 1),
            "cobertura_intereses_x": round(cobertura_intereses, 2),
            "deuda_total_eur": round(deuda_total, 2),
            "concentracion_deuda_cp_pct": round(concentracion_cp, 1)
        }

    def evaluate_risk_triggers(self, ratios: Dict[str, Any], cohort_medians: Dict[str, float]) -> Dict[str, Any]:
        """
        Evalúa los disparadores de riesgo financiero comparando los ratios
        de la empresa contra la mediana de su cohorte sectorial.
        """
        alerts = []
        diferencial_caja_eur = 0.0

        # 1. Alerta de Cobro / Clientes (DSO superior a la competencia)
        dso_empresa = ratios["dso_dias"]
        dso_sector = cohort_medians.get("dso_dias", 60.0)
        
        if dso_empresa > dso_sector:
            dias_exceso = dso_empresa - dso_sector
            ventas_diarias_con_iva = (self.d.cifra_negocios * self.vat_factor) / 365
            diferencial_caja_eur = dias_exceso * ventas_diarias_con_iva
            alerts.append({
                "codigo": "RISK_DSO_EXCESS",
                "gravedad": "ALTA",
                "titulo": "Exceso en Período Medio de Cobro",
                "detalle": f"La empresa tarda {dso_empresa} días en cobrar vs. {dso_sector} días de la mediana del sector.",
                "impacto_caja_eur": round(diferencial_caja_eur, 2)
            })

        # 2. Alerta de Concentración de Deuda a Corto Plazo
        cp_pct = ratios["concentracion_deuda_cp_pct"]
        cp_sector_p75 = cohort_medians.get("concentracion_deuda_cp_p75", 65.0)
        
        if cp_pct > cp_sector_p75:
            alerts.append({
                "codigo": "RISK_SHORT_TERM_DEBT_CONCENTRATION",
                "gravedad": "CRÍTICA",
                "titulo": "Alta Concentración de Deuda a Corto Plazo",
                "detalle": f"El {cp_pct}% de la deuda bancaria vence a CP (pólizas/líneas), superando el umbral de seguridad del sector ({cp_sector_p75}%).",
                "impacto_caja_eur": None
            })

        return {
            "num_alertas": len(alerts),
            "caja_atrapada_total_eur": round(diferencial_caja_eur, 2),
            "alertas_activadas": alerts
        }
