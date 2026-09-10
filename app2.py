import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Directorio de Procuradores",
    layout="wide"
)

archivo = "RELACION DE PROCURADORES PÚBLICOS EN FUNCIONES.xlsx"

df = pd.read_excel(archivo)

st.title("⚖️ Directorio Nacional de Procuradores Públicos")

# KPIS
total = len(df)

titulares = (
    df["CARGO"]
    .astype(str)
    .str.upper()
    .str.contains("PROCURADOR PÚBLICO$")
    .sum()
)

adjuntos = (
    df["CARGO"]
    .astype(str)
    .str.upper()
    .str.contains("ADJUNTO")
    .sum()
)

encargados = (
    df["CARGO"]
    .astype(str)
    .str.upper()
    .str.contains("ENCARGADO")
    .sum()
)

entidades = df["ENTIDAD"].nunique()
departamentos = df["DEPARTAMENTO"].nunique()

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric("Procuradores", total)
c2.metric("Titulares", titulares)
c3.metric("Adjuntos", adjuntos)
c4.metric("Encargados", encargados)
c5.metric("Entidades", entidades)
c6.metric("Departamentos", departamentos)

st.divider()

tab1, tab2, tab3 = st.tabs([
    "📊 Resumen",
    "🗺️ Mapa",
    "📋 Directorio"
])

with tab1:

    ambito = (
        df.groupby("AMBITO")
        .size()
        .reset_index(name="TOTAL")
    )

    fig = px.bar(
        ambito,
        x="AMBITO",
        y="TOTAL",
        color="AMBITO",
        title="Procuradores por ámbito"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    dep = (
        df.groupby("DEPARTAMENTO")
        .size()
        .reset_index(name="TOTAL")
        .sort_values("TOTAL", ascending=False)
        .head(15)
    )

    fig2 = px.bar(
        dep,
        x="TOTAL",
        y="DEPARTAMENTO",
        orientation="h",
        title="Top departamentos"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

with tab2:

    mapa = df.dropna(
        subset=["LATITUD (Y)", "LONGITUD (X)"]
    )

    st.map(
        mapa.rename(
            columns={
                "LATITUD (Y)": "lat",
                "LONGITUD (X)": "lon"
            }
        )
    )

with tab3:

    dep = st.selectbox(
        "Departamento",
        ["Todos"] + sorted(
            df["DEPARTAMENTO"]
            .dropna()
            .unique()
        .tolist())
    )

    cargo = st.selectbox(
        "Cargo",
        ["Todos"] + sorted(
            df["CARGO"]
            .dropna()
            .unique()
        .tolist())
    )

    resultado = df.copy()

    if dep != "Todos":
        resultado = resultado[
            resultado["DEPARTAMENTO"] == dep
        ]

    if cargo != "Todos":
        resultado = resultado[
            resultado["CARGO"] == cargo
        ]

    st.dataframe(
        resultado[
            [
                "DEPARTAMENTO",
                "PROVINCIA",
                "ENTIDAD",
                "NOMBRE DEL PROCURADOR PÚBLICO",
                "CARGO",
                "CELULAR (1)"
            ]
        ],
        use_container_width=True
    )
