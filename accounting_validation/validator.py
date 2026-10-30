# accounting_validation/validator.py
from typing import Dict, List, Tuple
from financial_normalization.models import BalanceSheet, IncomeStatement


class AccountingValidationError(Exception):
    """Excepción para errores críticos en la contabilidad presentada."""

    pass


class AccountingValidator:
    TOLERANCE_EUROS = 0.01  # Tolerancia máxima por redondeos

    @classmethod
    def validate_balance_identity(
        cls, balance: BalanceSheet
    ) -> Tuple[bool, float, List[str]]:
        """Comprueba la ecuación fundamental: Activo = Patrimonio Neto + Pasivo.

        Retorna: (es_valido, descuadre_en_euros, lista_de_incidencias)
        """
        incidencias = []
        activo = round(balance.total_activo, 2)
        pasivo_pn = round(balance.total_pasivo_y_patrimonio_neto, 2)
        descuadre = round(activo - pasivo_pn, 2)

        if abs(descuadre) > cls.TOLERANCE_EUROS:
            incidencias.append(
                f"DESCUADRE CRÍTICO DE BALANCE: Total Activo ({activo:,.2f} €) "
                f"!= Patrimonio Neto + Pasivo ({pasivo_pn:,.2f} €). "
                f"Diferencia: {descuadre:,.2f} €."
            )
            return False, descuadre, incidencias

        return True, 0.0, incidencias

    @classmethod
    def validate_income_statement_coherence(
        cls, pyg: IncomeStatement, balance: BalanceSheet
    ) -> List[str]:
        """Verifica la coherencia entre el PyG y el Patrimonio Neto."""
        incidencias = []
        res_pyg = round(pyg.resultado_ejercicio, 2)
        res_pn = round(balance.resultado_ejercicio_pn, 2)

        if abs(res_pyg - res_pn) > cls.TOLERANCE_EUROS:
            incidencias.append(
                f"INCOHERENCIA CONTABLE: El resultado en PyG ({res_pyg:,.2f} €) "
                f"no coincide con el resultado registrado en Patrimonio Neto ({res_pn:,.2f} €)."
            )

        return incidencias
