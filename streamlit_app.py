
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Reid & Compañía - Dashboard Transformación Digital", layout="wide")

def load_sample_data():
    valor_financiero = pd.DataFrame({
        "Indicador": ["ROI Total", "ROI Ajustado", "CAPEX", "OPEX", "Ahorro proyectado", "Payback"],
        "Valor": [145, 4.5, 5200000, 4800000, 3200000, 14],
        "Unidad": ["%", "x", "RD$", "RD$", "RD$/año", "meses"]
    })
    cultura_digital = pd.DataFrame({
        "Indicador": ["eNPS", "Adopción Digital", "Proyectos Ágiles"],
        "Actual": [45, 62, 25],
        "Meta": [70, 90, 75],
        "Periodo": ["18 meses", "18 meses", "18 meses"]
    })
    cx_kpi = pd.DataFrame({
        "Etapa": ["Descubrimiento", "Evaluación", "Compra", "Servicio", "Fidelización"],
        "Conversion Rate": [0.40, 0.55, 0.65, 0.70, 0.75],
        "Satisfacción": [72, 75, 80, 78, 82],
        "NPS": [68, 72, 75, 77, 80]
    })
    riesgos = pd.DataFrame({
        "Riesgo": ["Ciberataque", "Pérdida CRM", "Fraude interno", "Falla IA", "Fuga datos"],
        "Probabilidad": ["Alta", "Media", "Media", "Media", "Media"],
        "Impacto": ["Alta", "Alta", "Media", "Alta", "Alta"],
        "Nivel": ["Crítico", "Alto", "Medio", "Alto", "Alto"],
        "Mitigación": ["Firewalls + MFA", "Backup diario", "Auditoría", "Auditoría ética", "Contrato NDA"]
    })
    return valor_financiero, cultura_digital, cx_kpi, riesgos

def read_upload(xls):
    valor_financiero = pd.read_excel(xls, sheet_name="Valor_Financiero")
    cultura_digital = pd.read_excel(xls, sheet_name="Cultura_Digital")
    cx_kpi = pd.read_excel(xls, sheet_name="CX_KPI")
    riesgos = pd.read_excel(xls, sheet_name="Riesgos")
    return valor_financiero, cultura_digital, cx_kpi, riesgos

st.sidebar.title("Reid & Compañía")
st.sidebar.subheader("Datos del Dashboard")
uploaded = st.sidebar.file_uploader("Sube el Excel base (.xlsx) con las 4 hojas", type=["xlsx"])
use_sample = st.sidebar.checkbox("Usar datos de ejemplo", value=True if uploaded is None else False)

if uploaded is not None and not use_sample:
    try:
        valor_financiero, cultura_digital, cx_kpi, riesgos = read_upload(uploaded)
        st.sidebar.success("Excel cargado correctamente.")
    except Exception as e:
        st.sidebar.error(f"Error leyendo el Excel: {e}")
        st.stop()
else:
    valor_financiero, cultura_digital, cx_kpi, riesgos = load_sample_data()

st.title("Dashboard de Transformación Digital - Reid & Compañía S.A.")
st.caption("Valor, Experiencia del Cliente, Cultura Digital y Riesgo & Ética")

# KPI Header
col1, col2, col3, col4 = st.columns(4)

def get_val(df, name):
    try:
        return float(df.loc[df["Indicador"] == name, "Valor"].values[0])
    except:
        return None

roi_total = get_val(valor_financiero, "ROI Total")
roi_ajustado = get_val(valor_financiero, "ROI Ajustado")
capex = get_val(valor_financiero, "CAPEX")
opex = get_val(valor_financiero, "OPEX")

col1.metric("ROI Total", f"{roi_total:.0f}%" if roi_total is not None else "—")
col2.metric("ROI Ajustado", f"{roi_ajustado:.1f}x" if roi_ajustado is not None else "—")
col3.metric("CAPEX", f"RD${capex:,.0f}" if capex is not None else "—")
col4.metric("OPEX", f"RD${opex:,.0f}" if opex is not None else "—")

st.markdown('---')

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Valor & ROI", "Customer Experience (CX)", "Cultura & Liderazgo", "Riesgo & Ética"])

with tab1:
    st.subheader("Distribución CAPEX/OPEX y Flujo Financiero")
    # Barras CAPEX / OPEX
    fig1, ax1 = plt.subplots()
    cat = ["CAPEX", "OPEX"]
    vals = [capex if capex is not None else 0, opex if opex is not None else 0]
    ax1.bar(cat, vals)
    ax1.set_ylabel("RD$")
    ax1.set_title("Distribución CAPEX / OPEX")
    st.pyplot(fig1)

    # Línea de flujo (simulada)
    st.caption("Flujo trimestral estimado (simulado para visualización)")
    trimestres = ["Q1","Q2","Q3","Q4","Q5","Q6"]
    flujo = [ - (capex or 2000000)*0.4 - (opex or 1500000)*0.2,
              - (capex or 2000000)*0.3 - (opex or 1500000)*0.2,
              500000, 1200000, 1800000, 2200000 ]
    fig2, ax2 = plt.subplots()
    ax2.plot(trimestres, flujo, marker="o")
    ax2.set_ylabel("RD$")
    ax2.set_title("Flujo de Caja Trimestral y Recuperación")
    st.pyplot(fig2)

with tab2:
    st.subheader("Embudo (CJM) y KPIs de Experiencia")
    stages = cx_kpi["Etapa"]
    conv = (cx_kpi["Conversion Rate"] * 100).round(1)
    fig3, ax3 = plt.subplots()
    ax3.bar(stages, conv)
    ax3.set_ylabel("% Conversión")
    ax3.set_title("Embudo de Conversión por Etapa (CJM)")
    plt.xticks(rotation=15)
    st.pyplot(fig3)

    # Evolución de NPS (simulada)
    st.caption("Evolución NPS (simulada)")
    meses = ["M1","M2","M3","M4","M5","M6"]
    base = float(cx_kpi["NPS"].mean())
    nps_series = [base-4, base-2, base, base+1, base+2, base+3]
    fig4, ax4 = plt.subplots()
    ax4.plot(meses, nps_series, marker="o")
    ax4.set_ylabel("NPS")
    ax4.set_title("NPS Mensual")
    st.pyplot(fig4)

with tab3:
    st.subheader("Cultura y Adopción Digital")
    metas = cultura_digital[["Indicador","Actual","Meta"]]
    st.dataframe(metas, use_container_width=True)

    # Barras horizontales Actual vs Meta
    fig5, ax5 = plt.subplots()
    y = np.arange(len(metas))
    ax5.barh(y - 0.2, metas["Actual"], height=0.4, label="Actual")
    ax5.barh(y + 0.2, metas["Meta"], height=0.4, label="Meta")
    ax5.set_yticks(y, metas["Indicador"])
    ax5.set_xlabel("Porcentaje / Puntuación")
    ax5.set_title("Actual vs Meta (Cultura Digital)")
    ax5.legend()
    st.pyplot(fig5)

    st.markdown("""
**Plan 90/180/365**
- **90 días:** Diagnóstico cultural digital y talleres de sensibilización.
- **180 días:** Embajadores digitales y programas de certificación.
- **365 días:** Integrar competencias digitales en evaluaciones de desempeño.
""")

with tab4:
    st.subheader("Heatmap de Riesgos y Mitigación")
    map_prob = {"Baja":1, "Media":2, "Alta":3}
    map_imp = {"Baja":1, "Media":2, "Alta":3}
    riesgos_num = riesgos.copy()
    riesgos_num["ProbNum"] = riesgos_num["Probabilidad"].map(map_prob)
    riesgos_num["ImpNum"] = riesgos_num["Impacto"].map(map_imp)

    fig6, ax6 = plt.subplots()
    ax6.scatter(riesgos_num["ProbNum"], riesgos_num["ImpNum"])
    ax6.set_xticks([1,2,3])
    ax6.set_yticks([1,2,3])
    ax6.set_xlabel("Probabilidad")
    ax6.set_ylabel("Impacto")
    ax6.set_title("Mapa de Riesgos (Probabilidad vs Impacto)")
    for _, row in riesgos_num.iterrows():
        ax6.annotate(row["Riesgo"], (row["ProbNum"]+0.02, row["ImpNum"]+0.02), fontsize=8)
    st.pyplot(fig6)

    st.markdown("**Controles y Mitigación**")
    st.dataframe(riesgos[["Riesgo","Nivel","Mitigación"]], use_container_width=True)

st.markdown("---")
st.caption("Carga tu propio Excel con las hojas: Valor_Financiero, Cultura_Digital, CX_KPI, Riesgos.")
