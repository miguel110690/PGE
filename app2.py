import streamlit as st
import pandas as pd

# --------------------------------------------------
# CARGA
# --------------------------------------------------

archivo = "RELACION DE PROCURADORES PÚBLICOS EN FUNCIONES (59).xlsx"

df = pd.read_excel(
    archivo,
    sheet_name="ENCARGATURA"
)

# Limpiar espacios en nombres de columnas
df.columns = df.columns.str.strip()

# --------------------------------------------------
# FECHAS
# --------------------------------------------------

# Convertir FIN a fecha
df["FIN"] = pd.to_datetime(
    df["FIN"],
    errors="coerce"
)

# Fecha actual (sin hora)
hoy = pd.Timestamp.today().normalize()

# --------------------------------------------------
# FILTRO
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
# COLUMNAS A MOSTRAR
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

# Solo por seguridad
columnas_existentes = [
    c for c in columnas
    if c in df_filtrado.columns
]

# --------------------------------------------------
# KPI
# --------------------------------------------------

st.title("⚖️ Encargaturas Vigentes")

st.metric(
    "Total encargaturas vigentes",
    len(df_filtrado)
)

# --------------------------------------------------
# TABLA
# --------------------------------------------------

# --------------------------------------------------
# FILTROS DE BÚSQUEDA
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    filtro_procurador = st.text_input(
        "🔍 Buscar Procurador"
    )

with col2:
    filtro_entidad = st.text_input(
        "🔍 Buscar Entidad"
    )

# Aplicar filtros

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
        .str.contains(
            filtro_entidad,
            case=False,
            na=False
        )
    ]

st.dataframe(
    df_filtrado[columnas_existentes],
    use_container_width=True,
    height=700
)
