"""
Taller — Evaluación 1 (15%)
Universidad EAFIT — Maestría en Ciencia de Datos
Dataset: Superstore Sales (Kaggle - rohitsahoo/sales-forecasting)
"""

import matplotlib
matplotlib.use("Agg")   # backend sin ventana — genera archivos PNG directamente
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ─────────────────────────────────────────────
# CARGA Y PREPARACIÓN GENERAL DEL DATASET
# ─────────────────────────────────────────────
df = pd.read_csv("sales-forecasting/train.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)

os.makedirs("outputs", exist_ok=True)


# ══════════════════════════════════════════════════════════════════════
# RETO 1 — JERARQUÍA: "Ingeniería de la Atención"
# ══════════════════════════════════════════════════════════════════════
# Pregunta de negocio: ¿qué subcategoría genera más ventas?
# Tipo de gráfico elegido: barras horizontales ordenadas de mayor a menor.
# Justificación: la pregunta es de comparación de categorías (no de tendencia
# temporal), por lo que el gráfico de barras es el más eficiente. El orden
# descendente permite leer la jerarquía de un solo vistazo. Las barras
# horizontales facilitan leer etiquetas largas sin rotación.

# Agregación: ventas totales por subcategoría
ventas_sub = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=True)   # ascending=True para que la mayor quede arriba en barh
)

fig, ax = plt.subplots(figsize=(10, 7))

# Color selectivo: solo la barra mayor (Phones) resaltada en azul institucional;
# el resto en gris neutro para eliminar ruido visual y activar atención focal.
colores = ["#BDBDBD" if cat != "Phones" else "#1565C0" for cat in ventas_sub.index]

bars = ax.barh(ventas_sub.index, ventas_sub.values, color=colores, height=0.65)

# Etiquetas de valor al final de cada barra para evitar que el lector tenga
# que mirar el eje X; reduce carga cognitiva.
for bar, valor in zip(bars, ventas_sub.values):
    ax.text(
        bar.get_width() + 4000,
        bar.get_y() + bar.get_height() / 2,
        f"${valor:,.0f}",
        va="center",
        ha="left",
        fontsize=8,
        color="#444444",
    )

# Título accionable: comunica el hallazgo, no solo describe el gráfico
ax.set_title(
    "Phones lidera las ventas — foco de inversión prioritario",
    fontsize=13,
    fontweight="bold",
    pad=14,
    loc="left",
)
ax.set_xlabel("Ventas totales (USD)", fontsize=10)
ax.set_ylabel("Subcategoría de producto", fontsize=10)

# Eliminación de ruido visual: sin grilla pesada, sin bordes innecesarios
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.xaxis.set_visible(False)          # el eje X es redundante con las etiquetas de valor
ax.tick_params(axis="y", length=0)   # sin ticks en Y

# Fuente del dato (obligatorio para credibilidad)
fig.text(
    0.01, -0.01,
    "Fuente: Superstore Sales Dataset — Kaggle (rohitsahoo/sales-forecasting)",
    fontsize=7, color="#888888",
)

plt.tight_layout()
plt.savefig("outputs/reto1_jerarquia.png", dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Reto 1 guardado en outputs/reto1_jerarquia.png")


# ══════════════════════════════════════════════════════════════════════
# RETO 2 — CONTRASTE: "Detección de Anomalías"
# ══════════════════════════════════════════════════════════════════════
# Pregunta de negocio: ¿cuándo ocurre el pico de ventas y qué tan atípico es?
# Tipo de gráfico elegido: línea temporal mensual.
# Justificación: los datos tienen una dimensión temporal continua (2015–2018),
# lo que hace que el gráfico de líneas sea la representación natural para
# mostrar tendencia y detectar anomalías en el tiempo.

# Serie mensual de ventas
df["YearMonth"] = df["Order Date"].dt.to_period("M")
mensual = df.groupby("YearMonth")["Sales"].sum().reset_index()
mensual["YearMonth"] = mensual["YearMonth"].dt.to_timestamp()
mensual = mensual.sort_values("YearMonth").reset_index(drop=True)

# Identificar el pico máximo (anomalía positiva)
idx_pico = mensual["Sales"].idxmax()
pico_fecha = mensual.loc[idx_pico, "YearMonth"]
pico_valor = mensual.loc[idx_pico, "Sales"]

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle(
    "Contraste Antes / Después — Detección del Pico de Ventas",
    fontsize=13, fontweight="bold", y=1.02,
)

# ── VERSIÓN MALA (sin contraste): todos los puntos iguales, sin anotación
ax1 = axes[0]
ax1.plot(mensual["YearMonth"], mensual["Sales"], color="#4472C4", linewidth=1.8)
ax1.set_title("ANTES — Sin contraste", fontsize=11, color="#B00020", fontweight="bold")
ax1.set_ylabel("Ventas mensuales (USD)", fontsize=9)
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.tick_params(axis="x", rotation=30, labelsize=8)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x/1000:.0f}k"))

# ── VERSIÓN BUENA (con contraste): fondo gris, figura roja en el pico
ax2 = axes[1]

# Contexto (fondo): línea y puntos en gris neutro
ax2.plot(mensual["YearMonth"], mensual["Sales"], color="#BDBDBD", linewidth=1.8, zorder=1)
ax2.scatter(mensual["YearMonth"], mensual["Sales"], color="#BDBDBD", s=30, zorder=2)

# Figura: el pico en rojo vibrante
ax2.scatter(pico_fecha, pico_valor, color="#D32F2F", s=120, zorder=5, linewidths=1.5)
ax2.plot(
    [mensual.loc[idx_pico - 1, "YearMonth"], pico_fecha, mensual.loc[idx_pico + 1, "YearMonth"]],
    [mensual.loc[idx_pico - 1, "Sales"], pico_valor, mensual.loc[idx_pico + 1, "Sales"]],
    color="#D32F2F", linewidth=2.5, zorder=4,
)

# Anotación directa sobre el gráfico: insight en 5-8 palabras
ax2.annotate(
    f"Pico +{((pico_valor / mensual['Sales'].mean() - 1) * 100):.0f}% sobre la media — Nov 2018",
    xy=(pico_fecha, pico_valor),
    xytext=(pico_fecha - pd.DateOffset(months=14), pico_valor * 0.88),
    fontsize=8.5,
    color="#B00020",
    fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#B00020", lw=1.4),
)

ax2.set_title("DESPUÉS — Con contraste aplicado", fontsize=11, color="#1B5E20", fontweight="bold")
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.tick_params(axis="x", rotation=30, labelsize=8)

fig.text(
    0.01, -0.04,
    "Fuente: Superstore Sales Dataset — Kaggle (rohitsahoo/sales-forecasting)",
    fontsize=7, color="#888888",
)

plt.tight_layout()
plt.savefig("outputs/reto2_contraste.png", dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Reto 2 guardado en outputs/reto2_contraste.png")


# ══════════════════════════════════════════════════════════════════════
# RETO 3 — PERSUASIÓN: "Acto de Habla"
# ══════════════════════════════════════════════════════════════════════
# ACTO DE HABLA ELEGIDO: CONVENCER
# Se elige "Convencer" porque el gráfico no solo describe las ventas por región,
# sino que argumenta una redistribución del presupuesto comercial: la región
# South acumula apenas el 17% de las ventas totales pese a tener la misma
# estructura de segmentos que las demás regiones. Esto constituye una brecha
# de rendimiento que justifica acción inmediata.
#
# ESTRUCTURA NARRATIVA:
# • Contexto  → Cuatro regiones compiten con el mismo portafolio de productos.
# • Hallazgo  → South genera menos de la mitad que West (la líder).
# • Recomendación → Redirigir inversión comercial hacia South para capturar
#                   la oportunidad de crecimiento latente.

ventas_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)
total = ventas_region["Sales"].sum()
ventas_region["pct"] = ventas_region["Sales"] / total * 100

fig, ax = plt.subplots(figsize=(9, 5))

# Color selectivo: South (la región con oportunidad de mejora) en naranja
# fuerte para que demande atención; el resto en gris.
colores = ["#BDBDBD" if r != "South" else "#E65100" for r in ventas_region["Region"]]

bars = ax.bar(ventas_region["Region"], ventas_region["Sales"], color=colores, width=0.55)

# Etiquetas con valor absoluto y porcentaje sobre cada barra
for bar, row in zip(bars, ventas_region.itertuples()):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 8000,
        f"${row.Sales / 1e6:.2f}M\n({row.pct:.0f}%)",
        ha="center", va="bottom", fontsize=9,
        color="#B71C1C" if row.Region == "South" else "#444444",
        fontweight="bold" if row.Region == "South" else "normal",
    )

# Anotación de recomendación directa sobre la barra de South
ax.annotate(
    "Solo 17% del total —\n¿dónde está el equipo comercial?",
    xy=(ventas_region[ventas_region["Region"] == "South"].index[0], ventas_region.loc[ventas_region["Region"] == "South", "Sales"].values[0] / 2),
    xytext=(3.35, ventas_region["Sales"].max() * 0.55),
    fontsize=8.5, color="#BF360C", fontweight="bold",
    arrowprops=dict(arrowstyle="->", color="#BF360C", lw=1.3),
    ha="right",
)

# Título accionable: comunica la acción, no describe el gráfico
ax.set_title(
    "South concentra solo el 17% de ventas — oportunidad de inversión urgente",
    fontsize=12, fontweight="bold", loc="left", pad=12,
)

# Subtítulo con la estructura Contexto → Hallazgo (visible en 5 segundos)
ax.text(
    0, ventas_region["Sales"].max() * 1.17,
    "Contexto: 4 regiones, mismo portafolio  |  Hallazgo: South genera menos de la mitad que West  |  Recomendación: redirigir presupuesto",
    fontsize=7.5, color="#555555", style="italic",
)

ax.set_ylabel("Ventas totales (USD)", fontsize=10)
ax.set_xlabel("Región", fontsize=10)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.yaxis.set_visible(False)
ax.tick_params(axis="x", length=0)

fig.text(
    0.01, -0.03,
    "Fuente: Superstore Sales Dataset — Kaggle (rohitsahoo/sales-forecasting)",
    fontsize=7, color="#888888",
)

plt.tight_layout()
plt.savefig("outputs/reto3_persuasion.png", dpi=150, bbox_inches="tight")
plt.close()
print("[OK] Reto 3 guardado en outputs/reto3_persuasion.png")

print("\n[DONE] Todos los archivos generados en la carpeta outputs/")
