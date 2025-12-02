# 🚗 Análisis de Inteligencia de Datos - Parque Vehicular DGII (2007-2025)

Dashboard interactivo y análisis KPI del parque vehicular registrado en la República Dominicana con datos de 18 años (2007-2025).

## 📊 Descripción General

Análisis completo de **8,549,162 vehículos** a través de **179,779 registros**, incluyendo:
- 1,804 marcas distintas
- 16 clases de vehículos
- 12 orígenes/países
- 18 años de datos históricos

## 🎯 Características

✅ **Dashboard Interactivo** - Visualización dinámica con Streamlit
✅ **3 KPIs Principales** - Análisis de tendencias y comportamiento
✅ **Filtros en Tiempo Real** - Explora datos por año, origen, clase y tipo
✅ **Exporta Datos** - Descarga resultados filtrados a CSV
✅ **Código Validado** - Scripts Python con análisis comprobados
✅ **Visualizaciones Profesionales** - Gráficos en Alta Resolución (300 DPI)

## 🏗️ Estructura del Proyecto

```
.
├── dashboard.py                    # Dashboard interactivo (Streamlit)
├── data/
│   └── Parque vehicular, DGII, 2007-2025.xlsx  # Dataset principal
├── src/
│   └── kpi_analysis_corrected.py  # Scripts de análisis KPI
├── reports/
│   ├── 01_total_by_year_CORRECTED.png      # KPI 1: Tendencia anual
│   ├── 02_top_origins_CORRECTED.png        # KPI 2: Origen de vehículos
│   └── 03_average_age_CORRECTED.png        # KPI 3: Edad promedio
├── ANALISIS_DESCRIPTIVO_FINAL.txt  # Análisis descriptivo completo
├── EXECUTIVE_SUMMARY.md            # Resumen ejecutivo
└── requirements.txt                # Dependencias Python
```

## 📈 KPIs Principales

### 1️⃣ Total de Vehículos por Año
- **Hallazgo:** Tendencia creciente, especialmente después de 2017
- **Máximo:** 2024 con 386,354 vehículos inscritos

### 2️⃣ Distribución por Origen
- **Hallazgo:** 41% "OTROS", 34% Japoneses, 5.5% Americanos
- **Implicación:** Alta dependencia de importaciones

### 3️⃣ Edad Promedio del Parque
- **Hallazgo:** 12.60 años promedio (parque envejecido pero renovándose)
- **Tendencia:** Reducción acelerada desde 2017 (-16 años en 18 años)
- **Rango:** 4.40 años (2025) a 20.47 años (2007)

## 🚀 Quick Start

### Opción 1: Dashboard Interactivo (Recomendado)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run dashboard.py
```

El dashboard abrirá en `http://localhost:8501`

**Características del dashboard:**
- 🔍 Filtros por año, origen, clase y tipo
- 📊 5 pestañas con análisis
- 📥 Descarga de datos filtrados
- 📈 Gráficos interactivos con Plotly

### Opción 2: Análisis desde Python

```bash
python src/kpi_analysis_corrected.py
```

Genera gráficos PNG en la carpeta `reports/`

## 📋 Dataset

| Campo | Rango | Notas |
|-------|-------|-------|
| Año Inscripción | 2007-2025 | 18 años de datos |
| Año Fabricación | 2000-2025 | Validado y filtrado |
| Cantidad | 1-4,274,581 | Vehículos por grupo |
| Marcas Únicas | 1,804 | Honda, Toyota, Suzuki lideran |
| Orígenes Únicos | 12 | Principalmente importados |

## 📊 Hallazgos Clave

🔹 **Parque Envejecido**: La edad promedio es de **12.60 años**

🔹 **Pero en Renovación**: Aceleración significativa desde 2017, vehículos 2025 solo tienen **4.40 años** promedio

🔹 **Importaciones Dominan**: 41% sin clasificar específico, 34% japoneses, patrón consistente

🔹 **Crecimiento Continuo**: Inscripciones anuales aumentan, especialmente en últimos 3 años

## 🛠️ Requisitos

- Python 3.8+
- pandas
- plotly
- streamlit
- openpyxl

Ver `requirements.txt` para versiones específicas.

## 📁 Archivos Importantes

- **`ANALISIS_DESCRIPTIVO_FINAL.txt`** - Análisis estadístico detallado
- **`EXECUTIVE_SUMMARY.md`** - Resumen ejecutivo con hallazgos
- **`reports/*_CORRECTED.png`** - Visualizaciones de alta calidad (300 DPI)

## ✅ Validación

Todos los KPIs han sido validados contra el dataset completo:
- ✓ Fórmulas de agregación correctas
- ✓ Valores consistentes con análisis descriptivo
- ✓ Visualizaciones generan sin errores
- ✓ Filtros responden instantáneamente

## 📝 Notas

- **Fórmula de Edad:** Edad = Año Actual (2025) - Año Fabricación
- **Datos Válidos:** 179,728 de 179,780 registros (99.97%)
- **Calidad:** Mínimas inconsistencias, dataset bien estructurado

## 📧 Información del Proyecto

- **Institución:** DGII (Dirección General de Impuestos Internos)
- **Período:** 2007-2025 (18 años)
- **Fecha Actualización:** Diciembre 2025
- **Estado:** ✅ Completo y Validado
