# financial_metrics/calculator.py
from typing import Dict, Optional
from financial_normalization.models import BalanceSheet, IncomeStatement


class FinancialCalculator:

    @staticmethod
    def calculate_ebitda(pyg: IncomeStatement) -> float:
        """EBITDA = Resultado de Explotación (EBIT) + Amortización del inmovilizado."""
        return pyg.ebitda

    @staticmethod
    def calculate_ebitda_margin(pyg: IncomeStatement) -> Optional[float]:
        """Margen EBITDA (%) = EBITDA / Cifra de Negocios * 100."""
        if pyg.importe_neto_cifra_negocios == 0:
            return None
        return (pyg.ebitda / pyg.importe_neto_cifra_negocios) * 100.0

    @staticmethod
    def calculate_liquidity_ratios(balance: BalanceSheet) -> Dict[str, float]:
        """Calcula ratios de liquidez basados estrictamente en el balance normalizado."""
        ac = balance.total_activo_corriente
        pc = balance.total_pasivo_corriente
        efectivo = balance.efectivo_equivalentes
        existencias = balance.existencias

        # Ratio Corriente
        ratio_corriente = (ac / pc) if pc > 0 else 0.0

        # Prueba Ácida (Acid Test): (Activo Corriente - Existencias) / Pasivo Corriente
        prueba_acida = ((ac - existencias) / pc) if pc > 0 else 0.0

        # Ratio de Tesorería estricta: Efectivo / Pasivo Corriente
        ratio_tesoreria = (efectivo / pc) if pc > 0 else 0.0

        # Fondo de Maniobra (Working Capital): Activo Corriente - Pasivo Corriente
        fondo_maniobra = ac - pc

        return {
            "ratio_corriente": round(ratio_corriente, 4),
            "prueba_acida": round(prueba_acida, 4),
            "ratio_tesoreria": round(ratio_tesoreria, 4),
            "fondo_maniobra": round(fondo_maniobra, 2),
        }

    @staticmethod
    def calculate_operational_cycles(
        balance: BalanceSheet, pyg: IncomeStatement, use_averages: bool = False
    ) -> Dict[str, Optional[float]]:
        """Calcula DSO, DIO, DPO y Ciclo de Conversión de Caja (CCC).

        Metodología documentada según disponibilidad de saldos.
        """
        ventas = pyg.importe_neto_cifra_negocios
        if ventas <= 0:
            return {
                "dso": None,
                "dio": None,
                "dpo": None,
                "ccc": None,
                "metodologia": "No calculable por cifra de negocios nula",
            }

        # DSO (Days Sales Outstanding): Clientes / Ventas * 365
        clientes = balance.deudores_comerciales
        dso = (clientes / ventas) * 365.0

        # DIO (Days Inventory Outstanding): Existencias / Coste de Ventas * 365
        # Aproximación del coste de ventas mediante aprovisionamientos y variaciones
        coste_ventas = abs(pyg.aprovisionamientos) + abs(pyg.variacion_existencias)
        if coste_ventas > 0:
            dio = (balance.existencias / coste_ventas) * 365.0
        else:
            dio = 0.0

        # DPO (Days Payable Outstanding): Proveedores / Compras * 365
        # Aproximación de compras
        compras = abs(pyg.aprovisionamientos)
        proveedores = balance.acreedores_comerciales
        if compras > 0:
            dpo = (proveedores / compras) * 365.0
        else:
            dpo = 0.0

        ccc = dso + dio - dpo

        return {
            "dso": round(dso, 2),
            "dio": round(dio, 2),
            "dpo": round(dpo, 2),
            "ccc": round(ccc, 2),
            "metodologia": (
                "Saldos de cierre (Aproximación estándar)"
                if not use_averages
                else "Saldos medios"
            ),
        }
