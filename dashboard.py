import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------
# PAGE CONFIG
# ------------------------------
st.set_page_config(
    page_title="Caterpillar Finance Dashboard",
    layout="wide",
    page_icon="📊"
)

# ------------------------------
# CUSTOM CSS
# ------------------------------
st.markdown(
    """
    <style>
        body { color: black; }
        .reportview-container { background-color: #ffffff; }
        .sidebar .sidebar-content { background-color: #F2F2F2; }
        .stTabs [role="tab"] { font-size: 18px; color: #000000; }
        .stTabs [aria-selected="true"] { color: #FFCC00 !important; font-weight: bold; }
        h1, h2, h3, h4, h5 { color: #000000 !important; }
        .metric-card { padding: 20px; border-radius: 14px; background: #F8F8F8; }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# SIDEBAR UPLOAD
# ------------------------------
st.sidebar.header("📁 Cargar Datos")
file = st.sidebar.file_uploader("Sube tu archivo Excel o CSV", type=["xlsx", "csv"])

if file:
    if file.name.endswith("csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
else:
    df = pd.DataFrame()

# ------------------------------
# TABS
# ------------------------------
tabs = st.tabs(["🏢 Finanzas", "💳 Cartera", "📈 Ventas & IA", "⚙️ Ajustes"])

# ------------------------------
# TAB 1: FINANZAS
# ------------------------------
with tabs[0]:
    st.title("Reporte Financiero Caterpillar")
    
    if df.empty:
        st.warning("Por favor carga datos para continuar.")
    else:
        st.subheader("📊 Flujo de Efectivo")

        if "Fecha" in df.columns and "Monto" in df.columns:
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            df_sorted = df.sort_values("Fecha")

            fig = px.line(df_sorted, x="Fecha", y="Monto", title="Flujo Mensual")
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Resumen Financiero")

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Ingresos", f"${df['Monto'].sum():,.2f}")
            col2.metric("Promedio Mensual", f"${df['Monto'].mean():,.2f}")
            col3.metric("Transacciones", len(df))
        else:
            st.warning("Tu archivo debe incluir columnas 'Fecha' y 'Monto'.")

# ------------------------------
# TAB 2: CARTERA
# ------------------------------
with tabs[1]:
    st.title("Cartera Vencida y Corriente")

    if df.empty:
        st.warning("Sube un archivo para analizar cartera.")
    else:
        if "Cliente" in df.columns and "Status" in df.columns and "Monto" in df.columns:
            vencida = df[df["Status"] == "Vencida"]
            corriente = df[df["Status"] == "Corriente"]

            col1, col2 = st.columns(2)
            col1.metric("Cartera Vencida", f"${vencida['Monto'].sum():,.2f}")
            col2.metric("Cartera Corriente", f"${corriente['Monto'].sum():,.2f}")

            fig = px.pie(df, names="Status", values="Monto", title="Distribución de Cartera")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Tu archivo debe incluir columnas: Cliente, Status, Monto")

# ------------------------------
# TAB 3: VENTAS E IA
# ------------------------------
with tabs[2]:
    st.title("Proyecciones Inteligentes de Ventas")

    if df.empty:
        st.warning("Sube datos para generar predicciones.")
    else:
        if "Fecha" in df.columns and "Monto" in df.columns:
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            df_m = df.groupby(df["Fecha"].dt.to_period("M")).sum().reset_index()
            df_m["Fecha"] = df_m["Fecha"].dt.to_timestamp()

            last_value = df_m["Monto"].iloc[-1]
            prediction = last_value * np.random.uniform(1.03, 1.10)

            st.metric("Proyección Próximo Mes", f"${prediction:,.2f}")

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_m["Fecha"], y=df_m["Monto"], mode="lines+markers", name="Histórico"))
            fig.add_trace(go.Scatter(x=[df_m["Fecha"].max() + pd.DateOffset(months=1)], y=[prediction], mode="markers", name="Proyección", marker=dict(size=12)))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Se requieren columnas Fecha y Monto.")

# ------------------------------
# TAB 4: AJUSTES
# ------------------------------
with tabs[3]:
    st.title("Configuración General")
    st.write("Aquí podrás ajustar parámetros futuros, colores, logos y configuraciones adicionales.")




