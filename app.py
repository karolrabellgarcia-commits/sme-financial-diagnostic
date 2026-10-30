"""
app.py
------
Interfaz web interactiva construida con Streamlit para el SaaS
de Diagnóstico Financiero de PYMEs. Versión corporativa sin elementos informales.
"""

import streamlit as st
from financial_engine import FinancialData, FinancialDiagnosticEngine
from narrative_generator import ExecutiveTranslator

# Configuración de la página
st.set_page_config(
    page_title="Diagnóstico Financiero PYME",
    layout="wide"
)

# Título y Encabezado
st.title("Diagnóstico Financiero Automático para PYMEs")
st.markdown("---")

# Barra lateral (Sidebar) para entrada de datos
st.sidebar.header("Datos de la Empresa")
cif_input = st.sidebar.text_input("Introduce el CIF de la empresa:", value="B12345678")

st.sidebar.subheader("Configuración de Cohorte")
dso_sector = st.sidebar.number_input("DSO Mediana Sector (Días)", value=55)
p75_deuda_cp = st.sidebar.number_input("Límite Deuda CP Sector (%)", value=50)

# Botón de ejecución
if st.sidebar.button("Generar Diagnóstico", type="primary"):
    
    # 1. Simulación de carga de datos contables (Mock para la Demo)
    data = FinancialData(
        cifra_negocios=1250000.0,
        consumos_explotacion=820000.0,
        gastos_personal=210000.0,
        ebitda=115000.0,
        gastos_financieros=12500.0,
        resultado_neto=48000.0,
        existencias=140000.0,
        clientes=310000.0,
        efectivo=25000.0,
        patrimonio_neto=420000.0,
        deuda_bancaria_cp=180000.0,
        deuda_bancaria_lp=95000.0,
        proveedores=195000.0
    )

    # 2. Motor Determinista
    engine = FinancialDiagnosticEngine(data=data, vat_rate=0.21)
    ratios = engine.calculate_ratios()
    
    cohort_medians = {
        "dso_dias": float(dso_sector),
        "concentracion_deuda_cp_p75": float(p75_deuda_cp)
    }
    diagnosis = engine.evaluate_risk_triggers(ratios, cohort_medians)

    # 3. Vista de Métricas en Pantalla (Cuadro de Mandos)
    st.subheader(f"Indicadores Clave de Gestión (CIF: {cif_input})")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Margen EBITDA", f"{ratios['margen_ebitda_pct']}%", delta="Normal" if ratios['margen_ebitda_pct'] > 8 else "Bajo")
    col2.metric("Cobro a Clientes (DSO)", f"{ratios['dso_dias']} días", delta=f"{ratios['dso_dias'] - dso_sector:.1f} días vs sector", delta_color="inverse")
    col3.metric("Pago Proveedores (DPO)", f"{ratios['dpo_dias']} días")
    col4.metric("Deuda a CP", f"{ratios['concentracion_deuda_cp_pct']}%", delta="Riesgo CP" if ratios['concentracion_deuda_cp_pct'] > p75_deuda_cp else "Sano", delta_color="inverse")

    st.markdown("---")

    # 4. Bloque de Alertas y Caja Inmovilizada
    st.subheader("Alertas de Riesgo y Financiación")
    
    if diagnosis["caja_atrapada_total_eur"] > 0:
        st.error(f"Caja Inmovilizada por Desfases Contables: {diagnosis['caja_atrapada_total_eur']:,.2f} EUR")
    else:
        st.success("No se detectan desfases graves de caja frente a la cohorte.")

    for alert in diagnosis["alertas_activadas"]:
        st.warning(f"[{alert['gravedad']}] {alert['titulo']}: {alert['detalle']}")

    st.markdown("---")

    # 5. Borrador de Informe Ejecutivo
    st.subheader("Propuesta de Informe Ejecutivo (Generado para la Dirección)")
    
    translator = ExecutiveTranslator(ratios=ratios, diagnosis=diagnosis)
    payload = translator.build_llm_user_payload()
    
    st.info(payload)

else:
    st.info("Haga clic en 'Generar Diagnóstico' en el panel lateral para procesar el análisis.")
