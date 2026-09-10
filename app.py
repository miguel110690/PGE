import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------
st.set_page_config(
    page_title="Brecha de Procuradores Públicos",
    layout="wide"
)

# --------------------------------------------------
# CARGA DE DATOS
# --------------------------------------------------
archivo = "Relación de entidades públicas - nacional regional.xlsx"

df = pd.read_excel(archivo)

df.columns = [c.strip() for c in df.columns]

# --------------------------------------------------
# CÁLCULOS
# --------------------------------------------------

total_entidades = len(df)

designados = (
    df["CUENTA CON PROCURADOR PÚBLICO O PP ADJUNTO"]
    .astype(str)
    .str.upper()
    .eq("SI")
    .sum()
)

encargados = (
    df["CUENTA CON PROCURADOR PÚBLICO ENCARGADO*"]
    .astype(str)
    .str.upper()
    .eq("SI")
    .sum()
)

sin_pp = (
    df["NO CUENTA CON PP DESIGNADO NI ENCARGADO"]
    .astype(str)
    .str.upper()
    .eq("SI")
    .sum()
)

brecha = encargados + sin_pp

# --------------------------------------------------
# NIVEL
# --------------------------------------------------

def clasificar_nivel(x):

    texto = str(x).upper()

    if "MUNICIPAL" in texto:
        return "Municipal"

    if "REGIONAL" in texto:
        return "Regional"

    return "Nacional"

df["NIVEL"] = df["TIPO"].apply(clasificar_nivel)

brecha_nivel = (
    df[
        (df["CUENTA CON PROCURADOR PÚBLICO ENCARGADO*"] == "SI")
        | (df["NO CUENTA CON PP DESIGNADO NI ENCARGADO"] == "SI")
    ]
    .groupby("NIVEL")
    .size()
    .reset_index(name="BRECHA")
)

# --------------------------------------------------
# ESTADO
# --------------------------------------------------

def obtener_estado(row):

    if str(row["CUENTA CON PROCURADOR PÚBLICO O PP ADJUNTO"]).upper() == "SI":
        return "Designado"

    if str(row["CUENTA CON PROCURADOR PÚBLICO ENCARGADO*"]).upper() == "SI":
        return "Encargado"

    return "Sin PP"

df["ESTADO"] = df.apply(obtener_estado, axis=1)

estado_df = (
    df.groupby("ESTADO")
    .size()
    .reset_index(name="TOTAL")
)

# --------------------------------------------------
# CABECERA
# --------------------------------------------------

st.markdown(
    """
    # PROBLEMÁTICA
    ## 🔴 Brecha de Designación de Procuradores Públicos
    """
)

st.divider()

# --------------------------------------------------
# KPI
# --------------------------------------------------

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Total Entidades",
    f"{total_entidades:,}"
)

c2.metric(
    "Designados",
    f"{designados:,}"
)

c3.metric(
    "Encargados",
    f"{encargados:,}"
)

c4.metric(
    "Sin Procurador",
    f"{sin_pp:,}"
)

c5.metric(
    "Brecha",
    f"{brecha:,}"
)

st.divider()

# --------------------------------------------------
# GRÁFICOS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.bar(
        brecha_nivel,
        x="NIVEL",
        y="BRECHA",
        text="BRECHA",
        color="NIVEL",
        title="Brecha por Nivel"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig2 = px.pie(
        estado_df,
        values="TOTAL",
        names="ESTADO",
        title="Situación de Procuradores"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# --------------------------------------------------
# FILTROS
# --------------------------------------------------

st.subheader("Detalle de entidades")

nivel = st.multiselect(
    "Nivel",
    options=sorted(df["NIVEL"].unique()),
    default=sorted(df["NIVEL"].unique())
)

estado = st.multiselect(
    "Estado",
    options=sorted(df["ESTADO"].unique()),
    default=sorted(df["ESTADO"].unique())
)

df_filtrado = df[
    (df["NIVEL"].isin(nivel))
    &
    (df["ESTADO"].isin(estado))
]

st.dataframe(
    df_filtrado,
    use_container_width=True,
    height=600
)

# --------------------------------------------------
# PIE
# --------------------------------------------------

st.caption(
    "Fuente: Dirección de Información y Registro (DIR)"
)
