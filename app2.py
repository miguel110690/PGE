import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.set_page_config(
    page_title="Encargaturas Vigentes",
    layout="wide"
)

# --------------------------------------------------
# CARGA
# --------------------------------------------------

archivo = "RELACION DE PROCURADORES PÚBLICOS EN FUNCIONES (59).xlsx"

df = pd.read_excel(
    archivo,
    sheet_name="ENCARGATURA"
)

# Limpiar nombres de columnas
df.columns = df.columns.str.strip()

# --------------------------------------------------
# FECHAS
# --------------------------------------------------

df["FIN"] = pd.to_datetime(
    df["FIN"],
    errors="coerce"
)

hoy = pd.Timestamp.today().normalize()

# --------------------------------------------------
# FILTRAR ENCARGATURAS VIGENTES
# --------------------------------------------------

df_filtrado = df[
    (
        df["FIN"].isna()
    )
    |
    (
        df["FIN"] >= hoy
    )
].copy()

# --------------------------------------------------
# COLUMNAS
# --------------------------------------------------

columnas = [
    "AMBITO",
    "TIPO",
    "ENTIDAD",
    "NOMBRE DEL PROCURADOR PÚBLICO",
    "UBIGEO/CODIGO_2",
    "AMBITO_2",
    "TIPO_2",
    "ENTIDAD ENCARGADA",
    "RESOLUCIÓN_ENCARGATURA",
    "INICIO"
]

columnas_existentes = [
    c for c in columnas
    if c in df_filtrado.columns
]

# --------------------------------------------------
# TITULO
# --------------------------------------------------

st.title("⚖️ Encargaturas Vigentes")

st.metric(
    "Total encargaturas vigentes",
    len(df_filtrado)
)

# --------------------------------------------------
# FILTROS
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    filtro_procurador = st.text_input(
        "🔍 Buscar Procurador"
    )

with col2:

    filtro_entidad = st.text_input(
        "🔍 Buscar Entidad (exacta)"
    )

# --------------------------------------------------
# APLICAR FILTROS
# --------------------------------------------------

if filtro_procurador:

    df_filtrado = df_filtrado[
        df_filtrado["NOMBRE DEL PROCURADOR PÚBLICO"]
        .astype(str)
        .str.contains(
            filtro_procurador,
            case=False,
            na=False
        )
    ]

if filtro_entidad:

    df_filtrado = df_filtrado[
        df_filtrado["ENTIDAD"]
        .astype(str)
        .str.upper()
        ==
        filtro_entidad.upper()
    ]

# --------------------------------------------------
# RENUMERAR FILAS
# --------------------------------------------------

df_filtrado = df_filtrado.reset_index(drop=True)

df_filtrado.insert(
    0,
    "N°",
    range(1, len(df_filtrado) + 1)
)

# --------------------------------------------------
# CONTADOR
# --------------------------------------------------

st.info(
    "Registros encontrados: "
    + str(len(df_filtrado))
)

# --------------------------------------------------
# TABLA
# --------------------------------------------------

# ----------------------------------------
# TABLA CON AJUSTE DE TEXTO
# ----------------------------------------

columnas_mostrar = ["N°"] + columnas_existentes

tabla_html = (
    df_filtrado[columnas_mostrar]
    .to_html(
        index=False,
        escape=False
    )
)

st.markdown("""
<style>

table {
    width: 100% !important;
    font-size: 12px;
    table-layout: fixed;
}

th {
    background-color: #f5f7fa;
    text-align: left;
    padding: 8px;
    white-space: normal !important;
}

td {
    padding: 6px;
    white-space: normal !important;
    word-wrap: break-word;
    overflow-wrap: break-word;
    vertical-align: top;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    tabla_html,
    unsafe_allow_html=True
)
    hide_index=True,
    disabled=True,
    column_config={
        "N°": st.column_config.NumberColumn(
            width="small"
        ),

        "ENTIDAD": st.column_config.TextColumn(
            width="large"
        ),

        "NOMBRE DEL PROCURADOR PÚBLICO": st.column_config.TextColumn(
            width="large"
        ),

        "ENTIDAD ENCARGADA": st.column_config.TextColumn(
            width="large"
        ),

        "RESOLUCIÓN_ENCARGATURA": st.column_config.TextColumn(
            width="large"
        )
    }
)
