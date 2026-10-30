import pytest
from financial_engine import FinancialData, FinancialDiagnosticEngine

def test_financial_engine_calculation():
    # Datos de prueba reales (extraídos de un balance tipo Registro Mercantil)
    data = FinancialData(
        cifra_negocios=748089.0,
        consumos_explotacion=648144.0,
        gastos_personal=17444.0,
        ebitda=82952.0,
        gastos_financieros=3779.0,
        resultado_neto=171290.0,
        existencias=117290.0,
        clientes=226865.0,
        efectivo=92661.0,
        patrimonio_neto=840342.0,
        deuda_bancaria_cp=4558.0,
        deuda_bancaria_lp=209500.0,
        proveedores=316607.0
    )

    engine = FinancialDiagnosticEngine(data=data, vat_rate=0.21)
    ratios = engine.calculate_ratios()

    # Verificaciones de precisión matemática
    assert ratios["margen_ebitda_pct"] == 11.09
    assert ratios["deuda_total_eur"] == 214058.0
    assert ratios["concentracion_deuda_cp_pct"] == 2.1  # Estructura sana a largo plazo

    # Prueba de evaluación de cohorte y alertas
    cohort_medians = {
        "dso_dias": 64.0,
        "concentracion_deuda_cp_p75": 65.0
    }
    diagnosis = engine.evaluate_risk_triggers(ratios, cohort_medians)
    
    assert "num_alertas" in diagnosis
    print("\n✅ Todos los tests del motor matemático han pasado con éxito.")

if __name__ == "__main__":
    test_financial_engine_calculation()
