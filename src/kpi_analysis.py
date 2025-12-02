import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

"""
KPI ANALYSIS: PARQUE VEHICULAR DGII 2007-2025
===============================================

Este script implementa los KPIs para el análisis del parque vehicular
dominicano con todas las correcciones y validaciones necesarias.

El código ha sido validado contra los datos reales del dataset.

Output: genera gráficas PNG y archivo TXT con análisis completo
"""

# ===== CONFIGURATION =====
# Configure the path to the data file
data_path = os.path.join(os.path.dirname(__file__), "..", "data", "Parque vehicular, DGII, 2007-2025.xlsx")
output_path = os.path.join(os.path.dirname(__file__), "..", "reports")
log_file = os.path.join(output_path, f"kpi_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

# ===== LOGGING SETUP =====
class DualLogger:
    """Clase para escribir simultaneamente en consola y archivo"""
    def __init__(self, filename):
        self.file = open(filename, 'w', encoding='utf-8')
        self.console = None
    
    def write(self, message):
        print(message)
        self.file.write(message + '\n')
        self.file.flush()
    
    def close(self):
        self.file.close()

logger = DualLogger(log_file)

# ===== LOAD AND PREPARE DATA =====
logger.write("Cargando datos...")
df = pd.read_excel(data_path)

# Clean column names (important fix)
df.columns = df.columns.str.rstrip()

logger.write(f"✓ Datos cargados: {len(df):,} registros, {df.shape[1]} columnas")
logger.write(f"✓ Total de vehículos: {df['Cantidad'].sum():,}\n")

# ===== KPI 1: TOTAL VEHICLES PER YEAR =====
logger.write("=" * 80)
logger.write("KPI 1: TOTAL DE VEHÍCULOS POR AÑO DE INSCRIPCIÓN")
logger.write("=" * 80)

totals_by_year = df.groupby("Año Inscripción")["Cantidad"].sum()

logger.write(f"\nRango de años: {int(totals_by_year.index.min())} - {int(totals_by_year.index.max())}")
logger.write(f"Total de vehículos: {totals_by_year.sum():,}")
logger.write(f"\nTop 5 años con mayor inscripción:")
for idx, (year, qty) in enumerate(totals_by_year.sort_values(ascending=False).head(5).items(), 1):
    logger.write(f"  {idx}. {int(year)}: {qty:,} vehículos")

# Generate visualization
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(totals_by_year.index, totals_by_year.values, marker='o', linewidth=2, markersize=6, color='#1f77b4')
ax.set_title("Total de Vehículos por Año de Inscripción", fontsize=14, fontweight='bold')
ax.set_xlabel("Año de Inscripción", fontsize=12)
ax.set_ylabel("Cantidad Total de Vehículos", fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000)}K'))
plt.tight_layout()
plt.savefig(os.path.join(output_path, "01_total_by_year_CORRECTED.png"), dpi=300, bbox_inches='tight')
logger.write("\n✓ Gráfica guardada: 01_total_by_year_CORRECTED.png")

# ===== KPI 2: DISTRIBUTION BY ORIGIN (TOP 10) =====
logger.write("\n" + "=" * 80)
logger.write("KPI 2: DISTRIBUCIÓN POR ORIGEN (TOP 10)")
logger.write("=" * 80)

# Remove NaN values from Origin for this analysis
df_valid_origin = df.dropna(subset=['Origen'])
origin_totals = df_valid_origin.groupby("Origen")["Cantidad"].sum().sort_values(ascending=False).head(10)

logger.write(f"\nOrígenes totales en dataset: {df['Origen'].nunique()}")
logger.write(f"Registros con origen especificado: {len(df_valid_origin):,}")
logger.write(f"\nTop 10 orígenes:")
for idx, (origin, qty) in enumerate(origin_totals.items(), 1):
    percentage = (qty / df['Cantidad'].sum()) * 100
    logger.write(f"  {idx:2d}. {origin:15s}: {qty:>10,} vehículos ({percentage:5.2f}%)")

# Generate visualization
fig, ax = plt.subplots(figsize=(12, 7))
colors = plt.cm.Set3(range(len(origin_totals)))
bars = ax.barh(range(len(origin_totals)), origin_totals.values, color=colors)
ax.set_yticks(range(len(origin_totals)))
ax.set_yticklabels(origin_totals.index)
ax.set_xlabel("Cantidad Total de Vehículos", fontsize=12)
ax.set_title("Top 10 Orígenes del Parque Vehicular", fontsize=14, fontweight='bold')
ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x/1000000)}M' if x >= 1000000 else f'{int(x/1000)}K'))
ax.grid(True, alpha=0.3, axis='x', linestyle='--')

# Add value labels on bars
for i, (bar, val) in enumerate(zip(bars, origin_totals.values)):
    ax.text(val, i, f' {val:,}', va='center', fontsize=9)

plt.tight_layout()
plt.savefig(os.path.join(output_path, "02_top_origins_CORRECTED.png"), dpi=300, bbox_inches='tight')
logger.write("\n✓ Gráfica guardada: 02_top_origins_CORRECTED.png")

# ===== KPI 3: AVERAGE AGE PER YEAR =====
logger.write("\n" + "=" * 80)
logger.write("KPI 3: EDAD PROMEDIO DEL PARQUE VEHICULAR POR AÑO")
logger.write("=" * 80)

# Get current year dynamically
from datetime import datetime
año_actual = datetime.now().year

# Filter valid ages
df_valid_age = df[
    df["Año Fabricación"].notna() & 
    (df["Año Fabricación"] <= año_actual) &
    (df["Año Fabricación"] >= 1900)
].copy()

logger.write(f"\nRegistros válidos para análisis de edad: {len(df_valid_age):,} de {len(df):,}")
logger.write(f"Registros excluidos: {len(df) - len(df_valid_age):,}")
logger.write(f"Año actual utilizado para cálculo: {año_actual}")

# Calculate weighted average age per year using CURRENT YEAR
# Formula: Edad = Año Actual - Año Fabricación
df_valid_age["Edad"] = año_actual - df_valid_age["Año Fabricación"]

age_by_year = df_valid_age.groupby("Año Inscripción").apply(
    lambda g: (g["Edad"] * g["Cantidad"]).sum() / g["Cantidad"].sum(),
    include_groups=False
).sort_index()

logger.write(f"\nEdad promedio del parque: {age_by_year.mean():.2f} años")
logger.write(f"Rango de edades: {age_by_year.min():.2f} - {age_by_year.max():.2f} años")
logger.write(f"\nAños con mayor antigüedad (top 3):")
for idx, (year, age) in enumerate(age_by_year.sort_values(ascending=False).head(3).items(), 1):
    logger.write(f"  {idx}. {int(year)}: {age:.2f} años")

logger.write(f"\nAños más modernos (top 3):")
for idx, (year, age) in enumerate(age_by_year.sort_values(ascending=True).head(3).items(), 1):
    logger.write(f"  {idx}. {int(year)}: {age:.2f} años")

# Generate visualization
fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(age_by_year.index, age_by_year.values, marker='o', linewidth=2.5, markersize=7, color='#ff7f0e')
ax.fill_between(age_by_year.index, age_by_year.values, alpha=0.2, color='#ff7f0e')
ax.set_title("Edad Promedio del Parque Vehicular por Año de Inscripción", fontsize=14, fontweight='bold')
ax.set_xlabel("Año de Inscripción", fontsize=12)
ax.set_ylabel("Edad Promedio (Años)", fontsize=12)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_ylim(0, max(age_by_year.values) * 1.1)
plt.tight_layout()
plt.savefig(os.path.join(output_path, "03_average_age_CORRECTED.png"), dpi=300, bbox_inches='tight')
logger.write("\n✓ Gráfica guardada: 03_average_age_CORRECTED.png")

# ===== ADDITIONAL INSIGHTS =====
logger.write("\n" + "=" * 80)
logger.write("INSIGHTS ADICIONALES")
logger.write("=" * 80)

# Top brands
logger.write("\nTop 5 Marcas:")
top_brands = df.groupby('Marca')['Cantidad'].sum().sort_values(ascending=False).head(5)
for idx, (brand, qty) in enumerate(top_brands.items(), 1):
    logger.write(f"  {idx}. {brand}: {qty:,} vehículos")

# Vehicle types distribution
logger.write("\nDistribución por Tipo de Vehículo:")
type_dist = df.groupby('Tipo')['Cantidad'].sum().sort_values(ascending=False)
for typ, qty in type_dist.items():
    if pd.notna(typ):
        percentage = (qty / df['Cantidad'].sum()) * 100
        logger.write(f"  {typ}: {qty:,} vehículos ({percentage:.2f}%)")

logger.write("\n" + "=" * 80)
logger.write("✓ ANÁLISIS DE KPIs COMPLETADO")
logger.write("=" * 80)
logger.write("\nGráficas generadas:")
logger.write("  1. 01_total_by_year_CORRECTED.png")
logger.write("  2. 02_top_origins_CORRECTED.png")
logger.write("  3. 03_average_age_CORRECTED.png")
logger.write(f"\nUbicación: {output_path}")
logger.write(f"\nArchivo de log: {log_file}")
logger.write("\n" + "=" * 80)

# Close logger to flush and save file
logger.close()
print(f"\n✓ Análisis completado. Log guardado en: {log_file}")
