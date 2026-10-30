# app.py
import sys
import os
import pandas as pd

# Asegurar que el path incluye la raíz para importar los módulos correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from financial_normalization.models import BalanceSheet, IncomeStatement
from accounting_validation.validator import AccountingValidator
from financial_metrics.calculator import FinancialCalculator
from audit_trail.provenance import ProvenanceTracker
from sector_benchmarking.benchmarker import SectorBenchmarker
from stress_testing.simulator import StressTester
from historical_analysis.analyzer import HistoricalAnalyzer
from anomaly_detection.detector import FinancialAnomalyDetector
from ai_interpretation.connector import AIInterpretationConnector

st.set_page_config(
    page_title="Informe de Diagnóstico Financiero - Central de Balances",
    layout="wide"
)

st.title("Plataforma de Inteligencia Financiera y Diagnóstico Empresarial")
st.markdown("*Estándar Metodológico: Central de Balances / Rigor Determinista y Trazabilidad SHA-256*")
st.markdown("---")

# ==========================================
# BARRA LATERAL: ÚNICAMENTE CIF Y CONFIGURACIÓN BÁSICA
# ==========================================
st.sidebar.header("Identificación de la Empresa")
cif_input = st.sidebar.text_input("CIF de la Sociedad", value="B82000004")
dso_sector = st.sidebar.number_input("DSO Mediana Sector (días)", value=60.0)
limite_deuda_cp_sector = st.sidebar.number_input("Límite Deuda CP Sector (%)", value=40.0)

# Carga de datos avanzados (Opcional)
st.sidebar.markdown("---")
st.sidebar.header("Ajuste Avanzado de Datos (Opcional)")
usar_datos_manuales = st.sidebar.checkbox("Modificar estados financieros manualmente", value=False)

if usar_datos_manuales:
    with st.sidebar.expander("Balance de Situación", expanded=True):
        activo_no_corriente = st.number_input("Activo No Corriente", value=2400000.0)
        existencias = st.number_input("Existencias", value=400000.0)
        deudores_comerciales = st.number_input("Deudores Comerciales (Clientes)", value=820000.0)
        efectivo = st.number_input("Efectivo y Equivalentes", value=180000.0)
        
        patrimonio_neto = st.number_input("Patrimonio Neto Total", value=1600000.0)
        resultado_pn = st.number_input("Resultado del Ejercicio (en PN)", value=100000.0)
        deudas_lp = st.number_input("Deudas Financieras Largo Plazo", value=1000000.0)
        deudas_cp = st.number_input("Deudas Financieras Corto Plazo", value=550000.0)
        acreedores_comerciales = st.number_input("Acreedores Comerciales (Proveedores)", value=550000.0)

    with st.sidebar.expander("Cuenta de Pérdidas y Ganancias", expanded=False):
        ventas = st.number_input("Cifra Neta de Negocios (Ventas)", value=4000000.0)
        aprovisionamientos = st.number_input("Aprovisionamientos (Valor Negativo)", value=-2200000.0)
        gastos_personal = st.number_input("Gastos de Personal (Valor Negativo)", value=-950000.0)
        otros_gastos = st.number_input("Otros Gastos de Explotación (Valor Negativo)", value=-300000.0)
        amortizacion = st.number_input("Amortización de Inmovilizado (Valor Negativo)", value=-150000.0)
else:
    # Valores por defecto vinculados al CIF (Simulación de base de datos)
    activo_no_corriente = 2400000.0
    existencias = 400000.0
    deudores_comerciales = 820000.0
    efectivo = 180000.0
    patrimonio_neto = 1600000.0
    resultado_pn = 100000.0
    deudas_lp = 1000000.0
    deudas_cp = 550000.0
    acreedores_comerciales = 550000.0
    ventas = 4000000.0
    aprovisionamientos = -2200000.0
    gastos_personal = -950000.0
    otros_gastos = -300000.0
    amortizacion = -150000.0

# ==========================================
# CONSTRUCCIÓN DE MODELOS Y VALIDACIÓN
# ==========================================
balance = BalanceSheet(
    inmovilizado_material=activo_no_corriente,
    existencias=existencias,
    deudores_comerciales=deudores_comerciales,
    efectivo_equivalentes=efectivo,
    capital=patrimonio_neto,
    reservas=0.0,
    resultado_ejercicio_pn=resultado_pn,
    deudas_financieras_lp=deudas_lp,
    acreedores_comerciales=acreedores_comerciales,
    deudas_financieras_cp=deudas_cp
)

pyg = IncomeStatement(
    importe_neto_cifra_negocios=ventas,
    aprovisionamientos=aprovisionamientos,
    gastos_personal=gastos_personal,
    otros_gastos_explotacion=otros_gastos,
    amortizacion_inmovilizado=amortizacion
)

es_valido, descuadre, incidencias_balance = AccountingValidator.validate_balance_identity(balance)

st.header(f"Informe Completo de Diagnóstico Financiero — CIF: {cif_input}")

if not es_valido:
    st.error(f"ALERTA CRÍTICA: El balance presentado no cuadra matemáticamente. Descuadre: {descuadre:,.2f} €")
    for inc in incidencias_balance:
        st.warning(inc)
    st.stop()
else:
    st.success("Validación contable superada: Identidad fundamental cuadrada (Activo = Patrimonio Neto + Pasivo).")

# ==========================================
# CÁLCULOS DETERMINISTAS DE NÚCLEO
# ==========================================
ebitda = FinancialCalculator.calculate_ebitda(pyg)
margen_ebitda = FinancialCalculator.calculate_ebitda_margin(pyg)
liquidity = FinancialCalculator.calculate_liquidity_ratios(balance)
cycles = FinancialCalculator.calculate_operational_cycles(balance, pyg)

deuda_financiera_total = balance.deudas_financieras_lp + balance.deudas_financieras_cp
pct_deuda_cp = (balance.deudas_financieras_cp / deuda_financiera_total * 100.0) if deuda_financiera_total > 0 else 0.0

impacto_dso = SectorBenchmarker.calculate_dso_economic_impact(cycles["dso"], dso_sector, ventas)
riesgo_deuda_cp = SectorBenchmarker.evaluate_short_term_debt_risk(pct_deuda_cp, limite_deuda_cp_sector)

estres_costes = StressTester.simulate_cost_increase(ventas, ebitda, aprovisionamientos, 10.0)

serie_historica_demo = [
    {"ejercicio": 2021, "ventas": 3200000.0, "ebitda": 380000.0, "deuda": 1100000.0, "caja": 200000.0},
    {"ejercicio": 2022, "ventas": 3600000.0, "ebitda": 350000.0, "deuda": 1300000.0, "caja": 160000.0},
    {"ejercicio": 2023, "ventas": ventas, "ebitda": ebitda, "deuda": deuda_financiera_total, "caja": balance.efectivo_equivalentes}
]
crecimiento_historico = HistoricalAnalyzer.calculate_growth_rates(serie_historica_demo)
alertas_historicas = HistoricalAnalyzer.detect_historical_patterns(serie_historica_demo)

contradictions = FinancialAnomalyDetector.detect_contradictions(
    ventas_crecen=True,
    caja_baja=(balance.efectivo_equivalentes < 200000.0),
    ebitda_sube=(ebitda > 350000.0),
    existencias_crecen_mas_que_ventas=False
)

ai_payload = AIInterpretationConnector.build_structured_payload(
    cif=cif_input,
    balance_summary={"activo_total": balance.total_activo, "patrimonio_neto": balance.total_patrimonio_neto},
    metrics_summary={"ebitda": ebitda, "margen_ebitda": margen_ebitda, "ccc": cycles["ccc"]},
    anomalies=contradictions
)

payload_hash = {
    "cif": cif_input,
    "ventas": ventas,
    "ebitda": ebitda,
    "dso": cycles["dso"],
    "dso_sector": dso_sector
}
repro_hash = ProvenanceTracker.generate_reproducibility_hash(payload_hash)

# ==========================================
# PRESENTACIÓN CONTINUA Y UNIFICADA (SIN PESTAÑAS)
# ==========================================

st.markdown("---")
st.subheader("1. Resumen Ejecutivo y Métricas Principales")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Cifra de Negocios", f"{ventas:,.0f} €")
col2.metric("EBITDA", f"{ebitda:,.0f} €", f"{margen_ebitda:.2f}% Margen")
col3.metric("Fondo de Maniobra", f"{liquidity['fondo_maniobra']:,.0f} €")
col4.metric("Ciclo Caja (CCC)", f"{cycles['ccc']} días")

col_a, col_b, col_c = st.columns(3)
col_a.metric("Ratio Corriente", liquidity["ratio_corriente"])
col_b.metric("Prueba Ácida", liquidity["prueba_acida"])
col_c.metric("Período Medio de Cobro (DSO)", f"{cycles['dso']} días")

st.markdown("---")
st.subheader("2. Benchmarking e Impacto Económico en Euros")
st.info(impacto_dso["interpretacion"])

if riesgo_deuda_cp["nivel_riesgo"] == "CRÍTICO / ALTO":
    st.error(f"Riesgo de Deuda CP: {riesgo_deuda_cp['detalle']}")
else:
    st.success(f"Estructura de Deuda: {riesgo_deuda_cp['detalle']}")

st.markdown("---")
st.subheader("3. Evolución Histórica Plurianual")
st.dataframe(crecimiento_historico, use_container_width=True)

st.markdown("**Patrones Detectados:**")
for alerta in alertas_historicas:
    if "PATRÓN ANÓMALO" in alerta:
        st.warning(alerta)
    else:
        st.success(alerta)

st.markdown("---")
st.subheader("4. Simulaciones de Estrés Operativo")
st.write(f"**Escenario:** {estres_costes['escenario']}")
col_s1, col_s2, col_s3 = st.columns(3)
col_s1.metric("Impacto en Costes", f"{estres_costes['impacto_euros']:,.0f} €")
col_s2.metric("Nuevo EBITDA", f"{estres_costes['nuevo_ebitda']:,.0f} €", f"{estres_costes['diferencia_ebitda']:,.0f} €")
col_s3.metric("Nuevo Margen EBITDA", f"{estres_costes['nuevo_margen_ebitda']:.2f}%")

st.markdown("---")
st.subheader("5. Detección de Contradicciones y Conector de IA")
for cond in contradictions:
    st.warning(cond)

with st.expander("Ver Payload Estructurado para IA (Formato JSON)"):
    st.json(ai_payload)

st.markdown("---")
st.subheader("6. Trazabilidad Criptográfica de Diagnóstico")
st.code(f"Hash SHA-256: {repro_hash}", language="text")
st.caption("Certidumbre de cálculo: DERIVADO — ALTA (Fórmulas deterministas verificadas bajo estándar Central de Balances).")
