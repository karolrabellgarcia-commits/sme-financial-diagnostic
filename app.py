# app.py
import sys
import os

# Asegurar que el path incluye la raíz para importar los módulos correctamente
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from financial_normalization.models import BalanceSheet, IncomeStatement
from accounting_validation.validator import AccountingValidator
from financial_metrics.calculator import FinancialCalculator
from audit_trail.provenance import ProvenanceTracker
from sector_benchmarking.benchmarker import SectorBenchmarker

st.set_page_config(
    page_title="Plataforma de Diagnóstico Financiero Empresarial",
    page_layout="wide"
)

st.title("Plataforma de Inteligencia Financiera y Diagnóstico Empresarial")
st.markdown("---")

# Barra lateral para entrada de datos de la empresa y referencias sectoriales
st.sidebar.header("1. Datos de Identificación y Sectoriales")
cif_input = st.text_input("CIF de la Sociedad", value="B82000004")
dso_sector = st.sidebar.number_input("DSO Mediana Sector (días)", value=60.0)
limite_deuda_cp_sector = st.sidebar.number_input("Límite Deuda CP Sector (%)", value=40.0)

st.sidebar.header("2. Datos Contables Normalizados (EUR)")
with st.sidebar.expander("Balance de Situación", expanded=True):
    activo_no_corriente = st.number_input("Activo No Corriente", value=2300000.0)
    existencias = st.number_input("Existencias", value=400000.0)
    deudores_comerciales = st.number_input("Deudores Comerciales (Clientes)", value=820000.0)
    efectivo = st.number_input("Efectivo y Equivalentes", value=180000.0)
    
    patrimonio_neto = st.number_input("Patrimonio Neto Total", value=1700000.0)
    deudas_lp = st.number_input("Deudas Financieras Largo Plazo", value=1000000.0)
    deudas_cp = st.number_input("Deudas Financieras Corto Plazo", value=450000.0)
    acreedores_comerciales = st.number_input("Acreedores Comerciales (Proveedores)", value=550000.0)

with st.sidebar.expander("Cuenta de Pérdidas y Ganancias", expanded=False):
    ventas = st.number_input("Cifra Neta de Negocios (Ventas)", value=4000000.0)
    aprovisionamientos = st.number_input("Aprovisionamientos (Valor Negativo)", value=-2200000.0)
    gastos_personal = st.number_input("Gastos de Personal (Valor Negativo)", value=-950000.0)
    otros_gastos = st.number_input("Otros Gastos de Explotación (Valor Negativo)", value=-300000.0)
    amortizacion = st.number_input("Amortización de Inmovilizado (Valor Negativo)", value=-150000.0)

# Construcción de objetos del modelo normalizado
balance = BalanceSheet(
    inmovilizado_material=activo_no_corriente,
    existencias=existencias,
    deudores_comerciales=deudores_comerciales,
    efectivo_equivalentes=efectivo,
    capital=patrimonio_neto * 0.6,
    reservas=patrimonio_neto * 0.4,
    resultado_ejercicio_pn=100000.0,
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

# Validación Contable Estricta
es_valido, descuadre, incidencias_balance = AccountingValidator.validate_balance_identity(balance)

st.subheader(f"Diagnóstico para: `{cif_input}`")

if not es_valido:
    st.error("ALERTA CRÍTica: El balance presentado no cuadra matemáticamente.")
    for inc in incidencias_balance:
        st.warning(inc)
    st.stop()
else:
    st.success("Validación contable superada: Ecuación fundamental de balance cuadrada correctamente.")

# Cálculos Financieros Deterministas
ebitda = FinancialCalculator.calculate_ebitda(pyg)
margen_ebitda = FinancialCalculator.calculate_ebitda_margin(pyg)
liquidity = FinancialCalculator.calculate_liquidity_ratios(balance)
cycles = FinancialCalculator.calculate_operational_cycles(balance, pyg)

# Métricas de Deuda
deuda_financiera_total = balance.deudas_financieras_lp + balance.deudas_financieras_cp
pct_deuda_cp = (balance.deudas_financieras_cp / deuda_financiera_total * 100.0) if deuda_financiera_total > 0 else 0.0

# Benchmarking e Impacto Económico
impacto_dso = SectorBenchmarker.calculate_dso_economic_impact(cycles["dso"], dso_sector, ventas)
riesgo_deuda_cp = SectorBenchmarker.evaluate_short_term_debt_risk(pct_deuda_cp, limite_deuda_cp_sector)

# Visualización en Pestañas Profesionales
tab1, tab2, tab3 = st.tabs(["1. Diagnóstico Ejecutivo y Ratios", "2. Impacto Económico y Benchmarking", "3. Trazabilidad y Certidumbre"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cifra de Negocios", f"{ventas:,.0f} €")
    col2.metric("EBITDA", f"{ebitda:,.0f} €", f"{margen_ebitda:.2f}% Margen")
    col3.metric("Fondo de Maniobra", f"{liquidity['fondo_maniobra']:,.0f} €")
    col4.metric("Ciclo Caja (CCC)", f"{cycles['ccc']} días")

    st.markdown("### Indicadores Operativos y de Liquidez")
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Ratio Corriente", liquidity["ratio_corriente"])
    col_b.metric("Prueba Ácida", liquidity["prueba_acida"])
    col_c.metric("Período Medio de Cobro (DSO)", f"{cycles['dso']} días")

with tab2:
    st.markdown("### Bloque Diferencial: Impacto Económico en Euros")
    st.info(impacto_dso["interpretacion"])
    
    st.markdown("### Evaluación de Riesgo de Deuda a Corto Plazo")
    if riesgo_deuda_cp["nivel_riesgo"] == "CRÍTICO / ALTO":
        st.error(riesgo_deuda_cp["detalle"])
    else:
        st.success(riesgo_deuda_cp["detalle"])

with tab3:
    st.markdown("### Trazabilidad y Reproducibilidad del Paquete")
    payload = {
        "cif": cif_input,
        "ventas": ventas,
        "ebitda": ebitda,
        "dso": cycles["dso"],
        "dso_sector": dso_sector
    }
    repro_hash = ProvenanceTracker.generate_reproducibility_hash(payload)
    st.text(f"Hash SHA-256 de Reproducibilidad:\n{repro_hash}")
    st.caption("Certidumbre de cálculo: DERIVADO — ALTA (Fórmulas deterministas verificadas).")
