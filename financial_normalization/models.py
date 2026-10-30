# financial_normalization/models.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional


class QualityRating(Enum):
    OBSERVADO_ALTA = "OBSERVADO — ALTA"
    DERIVADO_ALTA = "DERIVADO — ALTA"
    DERIVADO_MEDIA = "DERIVADO — MEDIA"
    ESTIMADO_CONDICIONAL = "ESTIMADO — CONDICIONAL"
    NO_DISPONIBLE = "NO DISPONIBLE"


@dataclass
class AccountingTrace:
    original_code: str
    original_description: str
    original_value: float
    normalized_concept: str
    mapping_rule: str


@dataclass
class BalanceSheet:
    # ACTIVO NO CORRIENTE
    inmovilizado_intangible: float = 0.0
    inmovilizado_material: float = 0.0
    inversiones_inmobiliarias: float = 0.0
    inversiones_financieras_lp: float = 0.0

    # ACTIVO CORRIENTE
    existencias: float = 0.0
    deudores_comerciales: float = 0.0
    otros_deudores: float = 0.0
    inversiones_financieras_cp: float = 0.0
    efectivo_equivalentes: float = 0.0

    # PATRIMONIO NETO
    capital: float = 0.0
    reservas: float = 0.0
    resultado_ejercicio_pn: float = 0.0
    otros_componentes_pn: float = 0.0

    # PASIVO NO CORRIENTE
    deudas_financieras_lp: float = 0.0
    provisiones_lp: float = 0.0

    # PASIVO CORRIENTE
    acreedores_comerciales: float = 0.0
    deudas_financieras_cp: float = 0.0
    otras_obligaciones_cp: float = 0.0

    @property
    def total_activo_no_corriente(self) -> float:
        return (
            self.inmovilizado_intangible
            + self.inmovilizado_material
            + self.inversiones_inmobiliarias
            + self.inversiones_financieras_lp
        )

    @property
    def total_activo_corriente(self) -> float:
        return (
            self.existencias
            + self.deudores_comerciales
            + self.otros_deudores
            + self.inversiones_financieras_cp
            + self.efectivo_equivalentes
        )

    @property
    def total_activo(self) -> float:
        return self.total_activo_no_corriente + self.total_activo_corriente

    @property
    def total_patrimonio_neto(self) -> float:
        return (
            self.capital
            + self.reservas
            + self.resultado_ejercicio_pn
            + self.otros_componentes_pn
        )

    @property
    def total_pasivo_no_corriente(self) -> float:
        return self.deudas_financieras_lp + self.provisiones_lp

    @property
    def total_pasivo_corriente(self) -> float:
        return (
            self.acreedores_comerciales
            + self.deudas_financieras_cp
            + self.otras_obligaciones_cp
        )

    @property
    def total_pasivo(self) -> float:
        return self.total_pasivo_no_corriente + self.total_pasivo_corriente

    @property
    def total_pasivo_y_patrimonio_neto(self) -> float:
        return self.total_patrimonio_neto + self.total_pasivo


@dataclass
class IncomeStatement:
    importe_neto_cifra_negocios: float = 0.0
    aprovisionamientos: float = 0.0  # Signo habitual: negativo
    variacion_existencias: float = 0.0
    gastos_personal: float = 0.0  # Signo habitual: negativo
    otros_gastos_explotacion: float = 0.0  # Signo habitual: negativo
    amortizacion_inmovilizado: float = 0.0  # Signo habitual: negativo
    deterioros_y_enajenaciones: float = 0.0

    ingresos_financieros: float = 0.0
    gastos_financieros: float = 0.0  # Signo habitual: negativo
    impuesto_beneficios: float = 0.0

    @property
    def resultado_explotacion_ebit(self) -> float:
        return (
            self.importe_neto_cifra_negocios
            + self.aprovisionamientos
            + self.variacion_existencias
            + self.gastos_personal
            + self.otros_gastos_explotacion
            + self.amortizacion_inmovilizado
            + self.deterioros_y_enajenaciones
        )

    @property
    def ebitda(self) -> float:
        # EBITDA = EBIT - Amortizaciones (dado que la amortización restó, la sumamos de vuelta en valor absoluto)
        return self.resultado_explotacion_ebit - self.amortizacion_inmovilizado

    @property
    def resultado_financiero(self) -> float:
        return self.ingresos_financieros + self.gastos_financieros

    @property
    def resultado_antes_impuestos_ebt(self) -> float:
        return self.resultado_explotacion_ebit + self.resultado_financiero

    @property
    def resultado_ejercicio(self) -> float:
        return self.resultado_antes_impuestos_ebt + self.impuesto_beneficios
