"""
main.py
-------
Orquestador principal del MVP de diagnóstico financiero para PYMEs.
Simula la entrada de un CIF, extrae los datos contables, ejecuta el motor
matemático determinista y genera la estructura del informe ejecutivo.
"""

from financial_engine import FinancialData, FinancialDiagnosticEngine
from narrative_generator import ExecutiveTranslator


def get_mock_company_data(cif: str) -> FinancialData:
    """
    Simula la extracción de datos contables desde el Registro Mercantil o base de datos.
    En producción, aquí se conectaría la API de scraping/ingesta de datos.
    """
    print(f"🔍 Obteniendo datos oficiales del Registro Mercantil para el CIF: {cif}...")
    
    # Datos de ejemplo de una PYME tipo con tensión en cobros (DSO)
    return FinancialData(
        cifra_negocios=1250000.0,      # 1,25M € de ventas
        consumos_explotacion=820000.0,   # 820k € de compras/consumos
        gastos_personal=210000.0,        # 210k € de personal
        ebitda=115000.0,                 # 115k € de EBITDA (Margen ~9.2%)
        gastos_financieros=12500.0,      # 12.5k € de intereses
        resultado_neto=48000.0,          # 48k € de beneficio neto
        existencias=140000.0,            # Stock en almacén
        clientes=310000.0,               # Deudores comerciales (DSO elevado)
        efectivo=25000.0,                # Poca liquidez en caja
        patrimonio_neto=420000.0,        # Fondos propios
        deuda_bancaria_cp=180000.0,      # 180k € de deuda a corto plazo (pólizas/líneas)
        deuda_bancaria_lp=95000.0,       # 95k € de deuda a largo plazo
        proveedores=195000.0             # Cuentas a pagar
    )


def run_diagnostic(cif: str) -> None:
    """Ejecuta el flujo completo del diagnóstico financiero."""
    print("=" * 60)
    print(f"🚀 INICIANDO DIAGNÓSTICO FINANCIERO AUTOMATIZADO - CIF: {cif}")
    print("=" * 60)

    # 1. Obtención de datos
    company_data = get_mock_company_data(cif)

    # 2. Ejecución del motor determinista
    engine = FinancialDiagnosticEngine(data=company_data, vat_rate=0.21)
    ratios = engine.calculate_ratios()

    # Medianas sectoriales de referencia (Cohorte)
    cohort_medians = {
        "dso_dias": 55.0,                         # La competencia cobra a 55 días
        "concentracion_deuda_cp_p75": 50.0        # Máximo de seguridad de deuda a CP: 50%
    }
    diagnosis = engine.evaluate_risk_triggers(ratios, cohort_medians)

    # 3. Traducción a narrativa ejecutiva
    translator = ExecutiveTranslator(ratios=ratios, diagnosis=diagnosis)
    system_prompt = translator.build_llm_system_prompt()
    user_payload = translator.build_llm_user_payload()

    # 4. Impresión de resultados estructurados
    print("\n📊 RESULTADOS DETERMINISTAS (PUNTOS DE VERDAD):")
    print("-" * 60)
    for k, v in ratios.items():
        print(f"  • {k}: {v}")

    print("\n⚠️ ALERTAS Y CAJA INMOVILIZADA DETECTADA:")
    print("-" * 60)
    print(f"  • Número de alertas activadas: {diagnosis['num_alertas']}")
    print(f"  • Caja total atrapada por desfases: {diagnosis['caja_atrapada_total_eur']} €")
    for alert in diagnosis["alertas_activadas"]:
        print(f"    [{alert['gravedad']}] {alert['titulo']}: {alert['detalle']}")

    print("\n📝 PROMPT STRUCTURAL PREPARADO PARA EL LLM:")
    print("=" * 60)
    print(user_payload)
    print("=" * 60)
    print("\n✅ Diagnóstico procesado con éxito.")


if __name__ == "__main__":
    # Prueba con un CIF de demostración
    run_diagnostic(cif="B12345678")
