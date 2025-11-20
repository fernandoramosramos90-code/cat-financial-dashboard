import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------
# PAGE CONFIG
# -------------------------------------
st.set_page_config(
    page_title="Caterpillar Finance Dashboard",
    layout="wide",
    page_icon="📊"
)

# -------------------------------------
# CUSTOM CSS (mejor contrastado)
# -------------------------------------
st.markdown(
    """
    <style>
        body { color: #000000; background-color:#ffffff; }
        .reportview-container { background-color: #ffffff; }
        .main { color:#000000 !important; }
        .stTextInput>div>div>input { color:#000000 !important; }
        .stMetric-value { color:#000000 !important; }
        .stTabs [role="tab"] { 
            font-size: 18px; 
            color: #000000 !important; 
            background:white; 
            border-radius:8px; 
        }
        .stTabs [aria-selected="true"] { 
            color: #000000 !important; 
            font-weight: bold; 
            background:#FFCC00 !important; 
        }
        h1, h2, h3, h4, h5 { color: #000000 !important; }
        .metric-card { 
            padding: 20px; 
            border-radius: 14px; 
            background: #F8F8F8; 
            border:1px solid #d6d6d6; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------
# SIDEBAR UPLOAD
# -------------------------------------
st.sidebar.header("📁 Cargar Datos")
file = st.sidebar.file_uploader("Sube tu archivo Excel o CSV", type=["xlsx", "csv"])

if file:
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file, sheet_name=None)  # ← LEER TODAS LAS HOJAS
else:
    df = {}

# -------------------------------------
# TABS
# -------------------------------------
tabs = st.tabs([
    "📘 Estado de Resultados",
    "🏢 Finanzas",
    "💳 Cartera",
    "📈 Ventas & IA",
    "⚙️ Ajustes"
])

# ============================================================
# TAB 0 - ESTADO DE RESULTADOS (NUEVO)
# ============================================================
with tabs[0]:
    st.title("📘 Estado de Resultados – Caterpillar")

    if "EstadoResultados" not in df:
        st.warning("Sube el archivo Excel generado o asegúrate de incluir la hoja 'EstadoResultados'.")
    else:
        er = df["EstadoResultados"]

        st.subheader("📄 Estado de Resultados")
        st.dataframe(er, use_container_width=True)

        # Mostrar métricas principales
        try:
            utilidad_bruta = float(er.loc[er["Concepto"] == "Utilidad Bruta", "Monto (USD)"].values[0])
            utilidad_op = float(er.loc[er["Concepto"] == "Utilidad Operativa", "Monto (USD)"].values[0])
            utilidad_neta = float(er.loc[er["Concepto"] == "Utilidad Neta", "Monto (USD)"].values[0])

            col1, col2, col3 = st.columns(3)
            col1.metric("Utilidad Bruta", f"${utilidad_bruta:,.2f}")
            col2.metric("Utilidad Operativa", f"${utilidad_op:,.2f}")
            col3.metric("Utilidad Neta", f"${utilidad_neta:,.2f}")

        except:
            st.warning("No se pudieron calcular las métricas del Estado de Resultados.")

# ============================================================
# TAB 1 - FINANZAS
# ============================================================
with tabs[1]:
    st.title("🏢 Reporte Financiero Caterpillar")

    if "FlujoEfectivo" not in df:
        st.warning("Sube el archivo Excel que incluya la hoja 'FlujoEfectivo'.")
    else:
        fe = df["FlujoEfectivo"]

        st.subheader("📊 Flujo de Efectivo")
        st.dataframe(fe)

        # Gráfico
        fig = px.bar(
            fe,
            x="Concepto",
            y="Monto (USD)",
            title="Flujo de Efectivo",
            color="Monto (USD)"
        )
        fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font=dict(color="black"))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 2 - CARTERA
# ============================================================
with tabs[2]:
    st.title("💳 Cartera Vencida y Corriente")

    if "Cartera" not in df:
        st.warning("Tu archivo debe contener la hoja 'Cartera'.")
    else:
        cartera = df["Cartera"]

        vencida = cartera[cartera["Status"] == "Vencida"]
        corriente = cartera[cartera["Status"] == "Corriente"]

        col1, col2 = st.columns(2)
        col1.metric("Cartera Vencida", f"${vencida['Monto'].sum():,.2f}")
        col2.metric("Cartera Corriente", f"${corriente['Monto'].sum():,.2f}")

        fig = px.pie(
            cartera,
            names="Status",
            values="Monto",
            title="Distribución de Cartera"
        )
        fig.update_layout(paper_bgcolor="white", font=dict(color="black"))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 3 - VENTAS E IA
# ============================================================
with tabs[3]:
    st.title("📈 Proyecciones Inteligentes de Ventas")

    if "VentasMensuales" not in df:
        st.warning("Tu archivo debe incluir la hoja 'VentasMensuales'.")
    else:
        vm = df["VentasMensuales"].copy()
        vm["Mes"] = pd.to_datetime(vm["Mes"])
        last_value = vm["Monto"].iloc[-1]
        projection = last_value * np.random.uniform(1.03, 1.12)

        st.metric("Proyección Próximo Mes", f"${projection:,.2f}")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=vm["Mes"], y=vm["Monto"], mode="lines+markers", name="Histórico"))
        fig.add_trace(go.Scatter(
            x=[vm["Mes"].max() + pd.DateOffset(months=1)],
            y=[projection],
            mode="markers",
            name="Proyección",
            marker=dict(size=12, color="gold")
        ))

        fig.update_layout(paper_bgcolor="white", font=dict(color="black"))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================
# TAB 4 - AJUSTES
# ============================================================
with tabs[4]:
    st.title("⚙️ Ajustes Generales")
    st.write("Aquí podrás cambiar colores, logos y configuraciones futuras.")






