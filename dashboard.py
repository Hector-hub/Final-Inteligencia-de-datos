import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# ===== CONFIGURATION =====
st.set_page_config(
    page_title="Dashboard KPI - Parque Vehicular DGII",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== LOAD DATA =====
@st.cache_data
def load_data():
    data_path = os.path.join("data", "Parque vehicular, DGII, 2007-2025.xlsx")
    df = pd.read_excel(data_path)
    df.columns = df.columns.str.rstrip()
    return df

df = load_data()

# ===== SIDEBAR - FILTERS =====
st.sidebar.title("🔍 FILTROS")
st.sidebar.markdown("---")

# Filter by Year of Registration
año_min = int(df["Año Inscripción"].min())
año_max = int(df["Año Inscripción"].max())
año_range = st.sidebar.slider(
    "Años de Inscripción",
    min_value=año_min,
    max_value=año_max,
    value=(año_min, año_max),
    step=1
)

# Filter by Origin
origen_opciones = ["TODAS"] + sorted(df["Origen"].dropna().unique().tolist())
origen_seleccionado = st.sidebar.multiselect(
    "Origen del Vehículo",
    options=origen_opciones,
    default="TODAS"
)

# Filter by Vehicle Class
clase_opciones = ["TODAS"] + sorted(df["Descripción Clase"].dropna().unique().tolist())
clase_seleccionada = st.sidebar.multiselect(
    "Clase de Vehículo",
    options=clase_opciones,
    default="TODAS"
)

# Filter by Vehicle Type
tipo_opciones = ["TODOS"] + sorted(df["Tipo"].dropna().unique().tolist())
tipo_seleccionado = st.sidebar.multiselect(
    "Tipo de Vehículo",
    options=tipo_opciones,
    default="TODOS"
)

# Apply filters
df_filtered = df[
    (df["Año Inscripción"] >= año_range[0]) &
    (df["Año Inscripción"] <= año_range[1])
].copy()

if "TODAS" not in origen_seleccionado and origen_seleccionado:
    df_filtered = df_filtered[df_filtered["Origen"].isin(origen_seleccionado)]

if "TODAS" not in clase_seleccionada and clase_seleccionada:
    df_filtered = df_filtered[df_filtered["Descripción Clase"].isin(clase_seleccionada)]

if "TODOS" not in tipo_seleccionado and tipo_seleccionado:
    df_filtered = df_filtered[df_filtered["Tipo"].isin(tipo_seleccionado)]

# ===== MAIN DASHBOARD =====
st.title("🚗 Dashboard de KPIs - Parque Vehicular DGII (2007-2025)")
st.markdown("**Análisis interactivo del parque vehicular registrado en la República Dominicana**")
st.markdown("---")

# KEY METRICS
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_vehicles = df_filtered["Cantidad"].sum()
    st.metric(
        label="📊 Total de Vehículos",
        value=f"{total_vehicles:,.0f}",
        delta="Registrados"
    )

with col2:
    total_records = len(df_filtered)
    st.metric(
        label="📋 Registros",
        value=f"{total_records:,}",
        delta="En dataset"
    )

with col3:
    avg_age = (datetime.now().year - df_filtered[df_filtered["Año Fabricación"].notna()]["Año Fabricación"]).mean()
    st.metric(
        label="🗓️ Edad Promedio",
        value=f"{avg_age:.2f} años",
        delta="Del parque"
    )

with col4:
    top_brand = df_filtered.groupby("Marca")["Cantidad"].sum().idxmax() if len(df_filtered) > 0 else "N/A"
    st.metric(
        label="🏆 Marca Líder",
        value=top_brand,
        delta="Más frecuente"
    )

st.markdown("---")

# ===== TABS =====
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 KPI 1: Total por Año",
    "📊 KPI 2: Distribución por Origen",
    "🗓️ KPI 3: Edad Promedio",
    "🏷️ Análisis Adicional",
    "📥 Descargar Datos"
])

# ===== TAB 1: TOTAL BY YEAR =====
with tab1:
    st.subheader("Total de Vehículos por Año de Inscripción")
    
    totals_by_year = df_filtered.groupby("Año Inscripción")["Cantidad"].sum().reset_index()
    
    fig = px.line(
        totals_by_year,
        x="Año Inscripción",
        y="Cantidad",
        markers=True,
        title="Evolución del Total de Vehículos Inscritos",
        labels={"Cantidad": "Número de Vehículos", "Año Inscripción": "Año"},
        template="plotly_white",
        height=500
    )
    fig.update_traces(line=dict(color='#1f77b4', width=3), marker=dict(size=8))
    fig.update_yaxes(tickformat=",")
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Año Máximo", f"{int(totals_by_year.loc[totals_by_year['Cantidad'].idxmax(), 'Año Inscripción'])}")
    with col2:
        st.metric("Total Máximo", f"{totals_by_year['Cantidad'].max():,.0f}")
    with col3:
        st.metric("Promedio Anual", f"{totals_by_year['Cantidad'].mean():,.0f}")

# ===== TAB 2: DISTRIBUTION BY ORIGIN =====
with tab2:
    st.subheader("Distribución por Origen (Top 10)")
    
    df_valid_origin = df_filtered.dropna(subset=['Origen'])
    origin_totals = df_valid_origin.groupby("Origen")["Cantidad"].sum().sort_values(ascending=False).head(10).reset_index()
    
    fig = px.bar(
        origin_totals,
        x="Cantidad",
        y="Origen",
        orientation="h",
        title="Top 10 Orígenes del Parque Vehicular",
        labels={"Cantidad": "Número de Vehículos", "Origen": "Origen"},
        template="plotly_white",
        height=500,
        color="Cantidad",
        color_continuous_scale="Viridis"
    )
    fig.update_xaxes(tickformat=",")
    st.plotly_chart(fig, use_container_width=True)
    
    # Table with percentages
    st.subheader("Detalle de Orígenes")
    origin_totals["Porcentaje"] = (origin_totals["Cantidad"] / df_filtered["Cantidad"].sum() * 100).round(2)
    origin_totals = origin_totals.rename(columns={"Cantidad": "Total Vehículos"})
    st.dataframe(
        origin_totals,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total Vehículos": st.column_config.NumberColumn(format="%,d"),
            "Porcentaje": st.column_config.ProgressColumn(min_value=0, max_value=100)
        }
    )

# ===== TAB 3: AVERAGE AGE =====
with tab3:
    st.subheader("Edad Promedio del Parque Vehicular")
    
    año_actual = datetime.now().year
    df_valid_age = df_filtered[
        df_filtered["Año Fabricación"].notna() & 
        (df_filtered["Año Fabricación"] <= año_actual) &
        (df_filtered["Año Fabricación"] >= 1900)
    ].copy()
    
    if len(df_valid_age) > 0:
        df_valid_age["Edad"] = año_actual - df_valid_age["Año Fabricación"]
        
        age_by_year = df_valid_age.groupby("Año Inscripción").apply(
            lambda g: (g["Edad"] * g["Cantidad"]).sum() / g["Cantidad"].sum(),
            include_groups=False
        ).reset_index(name="Edad Promedio")
        
        fig = px.line(
            age_by_year,
            x="Año Inscripción",
            y="Edad Promedio",
            markers=True,
            title="Evolución de la Edad Promedio del Parque Vehicular",
            labels={"Edad Promedio": "Edad (Años)", "Año Inscripción": "Año"},
            template="plotly_white",
            height=500
        )
        fig.update_traces(line=dict(color='#ff7f0e', width=3), marker=dict(size=8))
        fig.add_hline(y=age_by_year["Edad Promedio"].mean(), line_dash="dash", line_color="red", annotation_text=f"Promedio: {age_by_year['Edad Promedio'].mean():.2f} años")
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Edad Promedio", f"{age_by_year['Edad Promedio'].mean():.2f} años")
        with col2:
            st.metric("Edad Máxima", f"{age_by_year['Edad Promedio'].max():.2f} años")
        with col3:
            st.metric("Edad Mínima", f"{age_by_year['Edad Promedio'].min():.2f} años")
        with col4:
            reduccion = age_by_year['Edad Promedio'].iloc[0] - age_by_year['Edad Promedio'].iloc[-1]
            st.metric("Reducción Total", f"{reduccion:.2f} años", delta="Desde inicio")
    else:
        st.warning("No hay datos válidos de edad para el filtro seleccionado.")

# ===== TAB 4: ADDITIONAL ANALYSIS =====
with tab4:
    st.subheader("Análisis Adicional")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Top 10 Marcas**")
        top_brands = df_filtered.groupby("Marca")["Cantidad"].sum().sort_values(ascending=False).head(10)
        fig_brands = px.bar(
            x=top_brands.values,
            y=top_brands.index,
            orientation="h",
            labels={"x": "Cantidad", "y": "Marca"},
            title="Top 10 Marcas",
            template="plotly_white",
            height=400
        )
        fig_brands.update_xaxes(tickformat=",")
        st.plotly_chart(fig_brands, use_container_width=True)
    
    with col2:
        st.write("**Distribución por Clase de Vehículo**")
        class_dist = df_filtered.groupby("Descripción Clase")["Cantidad"].sum().sort_values(ascending=False).head(10)
        fig_class = px.pie(
            values=class_dist.values,
            names=class_dist.index,
            title="Distribución por Clase (Top 10)",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_class, use_container_width=True)
    
    # Type distribution
    st.write("**Distribución por Tipo de Vehículo**")
    type_dist = df_filtered.groupby("Tipo")["Cantidad"].sum().sort_values(ascending=False)
    fig_type = px.bar(
        x=type_dist.index,
        y=type_dist.values,
        labels={"x": "Tipo", "y": "Cantidad"},
        title="Vehículos por Tipo",
        template="plotly_white",
        height=400
    )
    fig_type.update_yaxes(tickformat=",")
    st.plotly_chart(fig_type, use_container_width=True)

# ===== TAB 5: DOWNLOAD DATA =====
with tab5:
    st.subheader("📥 Descargar Datos Filtrados")
    
    # Create CSV
    csv = df_filtered.to_csv(index=False)
    
    st.download_button(
        label="📥 Descargar como CSV",
        data=csv,
        file_name=f"parque_vehicular_filtrado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )
    
    # Show summary
    st.write("**Resumen de datos filtrados:**")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Registros", f"{len(df_filtered):,}")
    with col2:
        st.metric("Total Vehículos", f"{df_filtered['Cantidad'].sum():,.0f}")
    with col3:
        st.metric("Orígenes Únicos", df_filtered["Origen"].nunique())

# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>Dashboard Interactivo - Análisis de Parque Vehicular DGII (2007-2025)</p>
    <p>Datos actualizados a: 2025 | Registros: 179,779 | Total de vehículos: 8,549,162</p>
</div>
""", unsafe_allow_html=True)
