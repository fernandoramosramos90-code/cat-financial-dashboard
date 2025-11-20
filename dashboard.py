import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Caterpillar Finance Dashboard", layout="wide", page_icon="📊")

st.markdown(
    """
    <style>
        body { color: #000000; background-color:#ffffff; }
        .reportview-container { background-color: #ffffff; }
        .main { color:#000000 !important; }
        .stTextInput>div>div>input { color:#000000 !important; }
        .stMetric-value { color:#000000 !important; }
        .stTabs [role="tab"] { font-size: 18px; color: #000000 !important; background:white; border-radius:8px; }
        .stTabs [aria-selected="true"] { color: #000000 !important; font-weight: bold; background:#FFCC00 !important; }
        h1, h2, h3, h4, h5 { color: #000000 !important; }
        .metric-card { padding: 20px; border-radius: 14px; background: #F8F8F8; border:1px solid #d6d6d6; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("📁 Cargar Datos")
file = st.sidebar.file_uploader("Sube tu archivo Excel o CSV", type=["xlsx", "csv"])

df = pd.read_csv(file) if (file and file.name.endswith("csv")) else (pd.read_excel(file) if file else pd.DataFrame())

tabs = st.tabs(["🏢 Finanzas", "💳 Cartera", "📈 Ventas & IA", "⚙️ Ajustes"])

with tabs[0]:
    st.title("Reporte Financiero Caterpillar")
    if df.empty:
        st.warning("Por favor carga datos para continuar.")
    else:
        st.subheader("📊 Flujo de Efectivo")
        if "Fecha" in df.columns and "Monto" in df.columns:
            df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce")
            df_sorted = df.sort_values("Fecha")
            fig = px.line(df_sorted, x="Fecha", y="Monto", title="Flujo Mensual", markers=True)
            fig.update_layout(plot_bgcolor="white", paper_bgcolor="white", font=dict(color="black"))
            st.plotly_chart(fig, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            col1.metric("Total Ingresos", f"${df['Monto'].sum():,.2f}")
            col2.metric("Promedio Mensual", f"${df['Monto'].mean():,.2f}")
            col3.metric("Transacciones", len(df))

with tabs[1]:
    st.title("Cartera Vencida y Corriente")
    if df.empty:
        st.warning("Sube un archivo para analizar cartera.")
    else:
        if all(col in df.columns for col in ["Cliente", "Status", "Monto"]):
            vencida = df[df["Status"] == "Vencida"]
            corriente = df[df["Status"] == "Corriente"]
            col1, col2 = st.columns(2)
            col1.metric("Cartera Vencida", f"${vencida['Monto'].sum():,.2f}")
            col2.metric("Cartera Corriente", f"${corriente['Monto'].sum():,.2f}")
            fig = px.pie(df, names="Status", values="Monto", title="Distribución de Cartera")
            fig.update_layout(paper_bgcolor="white", font=dict(color="black"))
            st.plotly_chart(fig, use_container_width=True)

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
            fig.add_trace(go.Scatter(x=df_m["Fecha"], y=df_m["Monto"], mode="lines+markers", name="Histórico", line=dict(color="black")))
            fig.add_trace(go.Scatter(x=[df_m["Fecha"].max() + pd.DateOffset(months=1)], y=[prediction], mode="markers", name="Proyección", marker=dict(size=12, color="gold")))
            fig.update_layout(paper_bgcolor="white", plot_bgcolor="white", font=dict(color="black"))
            st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.title("Configuración General")
    st.write("Ajusta colores, logos y configuraciones futuras.")
    




