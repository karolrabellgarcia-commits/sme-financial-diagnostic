# financial_metrics/calculator.py
from typing import Dict, Any


class FinancialCalculator:
    """Motor de cálculo determinista con trazabilidad y conciliación partida por partida."""

    @staticmethod
    def calculate_ebitda_reconciled(pyg: Any) -> Dict[str, Any]:
        """Calcula el EBITDA y genera la tabla de conciliación detallada."""
        ventas = pyg.importe_neto_cifra_negocios
        aprovisionamientos = pyg.aprovisionamientos
        personal = pyg.gastos_personal
        otros_gastos = pyg.otros_gastos_explotacion
        amortizacion = pyg.amortizacion_inmovilizado

        # Cálculo determinista puro
        ebitda = ventas + aprovisionamientos + personal + otros_gastos
        ebit = ebitda + amortizacion

        reconciliation = {
            "partidas": [
                {"partida": "Importe Neto de Cifra de Negocios (Ventas)", "valor": ventas, "origen": "P&G Oficial"},
                {"partida": "Aprovisionamientos", "valor": aprovisionamientos, "origen": "P&G Oficial"},
                {"partida": "Gastos de Personal", "valor": personal, "origen": "P&G Oficial"},
                {"partida": "Otros Gastos de Explotación", "valor": otros_gastos, "origen": "P&G Oficial"},
                {"partida": "Resultado Bruto de Explotación (EBITDA)", "valor": ebitda, "origen": "Derivado (Suma algebraica)"},
                {"partida": "Amortización de Inmovilizado", "valor": amortizacion, "origen": "P&G Oficial"},
                {"partida": "Resultado de Explotación (EBIT)", "valor": ebit, "origen": "Derivado (EBITDA + Amortización)"}
            ],
            "formula": "EBITDA = Ventas + Aprovisionamientos + Gastos de Personal + Otros Gastos de Explotación",
            "resultado": ebitda,
            "fiabilidad": "Alta (Basado en P&G contable normalizada)"
        }
        return reconciliation

    @staticmethod
    def calculate_working_capital(balance: Any) -> Dict[str, Any]:
        """Calcula el Fondo de Maniobra y detalla sus componentes."""
        ac_existencias = balance.existencias
        ac_deudores = balance.deudores_comerciales
        ac_efectivo = balance.efectivo_equivalentes
        activo_corriente_total = ac_existencias + ac_deudores + ac_efectivo

        pc_acreedores = balance.acreedores_comerciales
        pc_deudas_cp = balance.deudas_financieras_cp
        pasivo_corriente_total = pc_acreedores + pc_deudas_cp

        fondo_maniobra = activo_corriente_total - pasivo_corriente_total

        detalle = {
            "activo_corriente": {
                "existencias": ac_existencias,
                "deudores_comerciales": ac_deudores,
                "efectivo_y_equivalentes": ac_efectivo,
                "total": activo_corriente_total
            },
            "pasivo_corriente": {
                "acreedores_comerciales": pc_acreedores,
                "deudas_financieras_cp": pc_deudas_cp,
                "total": pasivo_corriente_total
            },
            "formula": "Fondo de Maniobra = Activo Corriente Total - Pasivo Corriente Total",
            "resultado": fondo_maniobra,
            "fiabilidad": "Alta (Saldos de Balance de Situación)"
        }
        return detalle

    @staticmethod
    def calculate_operational_cycles_advanced(balance_inicial: Any, balance_final: Any, ventas: float, compras: float) -> Dict[str, Any]:
        """Calcula DSO, DPO y DIO utilizando saldos medios interanuales cuando es posible."""
        # Deudores medios
        deudores_medios = (balance_inicial.deudores_comerciales + balance_final.deudores_comerciales) / 2.0
        dso = (deudores_medios / ventas * 365.0) if ventas > 0 else 0.0

        # Proveedores medios
        proveedores_medios = (balance_inicial.acreedores_comerciales + balance_final.acreedores_comerciales) / 2.0
        dpo = (proveedores_medios / abs(compras) * 365.0) if compras != 0 else 0.0

        # Existencias medias
        existencias_medias = (balance_inicial.existencias + balance_final.existencias) / 2.0
        dio = (existencias_medias / abs(compras) * 365.0) if compras != 0 else 0.0

        ccc = dso + dio - dpo

        return {
            "dso": {
                "valor": round(dso, 2),
                "formula": "((Saldo Inicial Deudores + Saldo Final Deudores) / 2 / Ventas Anuales) * 365",
                "saldos_utilizados": {"inicial": balance_inicial.deudores_comerciales, "final": balance_final.deudores_comerciales},
                "limitacion": "Requiere desglose extracontable de efectos descontados para precisión absoluta."
            },
            "dpo": {
                "valor": round(dpo, 2),
                "formula": "((Saldo Inicial Proveedores + Saldo Final Proveedores) / 2 / Compras Anuales) * 365"
            },
            "dio": {
                "valor": round(dio, 2),
                "formula": "((Saldo Inicial Existencias + Saldo Final Existencias) / 2 / Aprovisionamientos) * 365"
            },
            "ccc": {
                "valor": round(ccc, 2),
                "formula": "CCC = DSO + DIO - DPO"
            }
        }
