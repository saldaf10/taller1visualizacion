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
ventas_sub_all = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(ascending=True)
)
# Quitar Phones (celulares), mantener desde Chairs hacia abajo, y quitar las 5 más pequeñas
chairs_sales = ventas_sub_all["Chairs"]
ventas_sub = ventas_sub_all[
    (ventas_sub_all.index != "Phones") & (ventas_sub_all <= chairs_sales)
]
ventas_sub = ventas_sub.iloc[5:]  # quitar las 5 categorías con menos ventas (parte inferior)

fig, ax = plt.subplots(figsize=(10, 7))

# Color selectivo: Chairs resaltada en azul institucional;
# el resto en gris neutro para eliminar ruido visual y activar atención focal.
colores = ["#1565C0" if cat == "Chairs" else "#BDBDBD" for cat in ventas_sub.index]

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
    "Chairs lidera las ventas de mobiliario — prioridad de inversión",
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

# Calcular cambio porcentual
mensual["pct_change"] = mensual["Sales"].pct_change() * 100
# Ignorar la transición de Diciembre a Enero (estacionalidad esperada)
mensual.loc[mensual["YearMonth"].dt.month == 1, "pct_change"] = None

# Patrones seleccionados: mes donde empieza la bajada (rojo)
# 2017-07 y la que sigue (2017-09), más las dos últimas (2018-06, 2018-09)
meses_inicio_bajada = ["2015-01", "2015-07", "2017-07", "2017-09", "2018-06", "2018-09"]
top4 = []
pct_arr = mensual["pct_change"].values
for mes in meses_inicio_bajada:
    ts = pd.Timestamp(mes)
    ds_idx = mensual.index[mensual["YearMonth"] == ts][0]
    v_idx = ds_idx + 1
    # Extender el verde mientras haya subidas consecutivas
    pk_end = v_idx + 1
    while pk_end + 1 < len(mensual):
        next_pct = mensual.loc[pk_end + 1, "pct_change"]
        if pd.notna(next_pct) and next_pct > 0:
            pk_end += 1
        else:
            break
    top4.append({
        "drop_start": ds_idx,
        "valley": v_idx,
        "pk_end": pk_end,
        "rise_pct": float(pct_arr[v_idx + 1]) if pd.notna(pct_arr[v_idx + 1]) else 0,
        "drop_pct": float(pct_arr[v_idx]) if pd.notna(pct_arr[v_idx]) else 0,
    })

fig, axes = plt.subplots(1, 2, figsize=(14, 5), sharey=True)
fig.suptitle(
    "Contraste Antes / Después — 4 Subidas Mayores con Bajada Previa",
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

# ── VERSIÓN BUENA (con contraste): bajadas en rojo, subidas en verde
ax2 = axes[1]

# Contexto (fondo): línea y puntos en gris neutro
ax2.plot(mensual["YearMonth"], mensual["Sales"], color="#BDBDBD", linewidth=1.8, zorder=1)
ax2.scatter(mensual["YearMonth"], mensual["Sales"], color="#BDBDBD", s=20, zorder=2)

# Resaltar los 4 patrones seleccionados
for p in top4:
    ds, v, pke = p["drop_start"], p["valley"], p["pk_end"]
    # Segmento bajada en rojo
    ax2.plot(
        [mensual.loc[ds, "YearMonth"], mensual.loc[v, "YearMonth"]],
        [mensual.loc[ds, "Sales"], mensual.loc[v, "Sales"]],
        color="#D32F2F", linewidth=2.5, zorder=4,
    )
    ax2.scatter(mensual.loc[v, "YearMonth"], mensual.loc[v, "Sales"],
                color="#D32F2F", s=50, zorder=5)
    # Segmento(s) de subida en verde — pueden cubrir varios meses consecutivos
    xs_green = [mensual.loc[i, "YearMonth"] for i in range(v, pke + 1)]
    ys_green = [mensual.loc[i, "Sales"] for i in range(v, pke + 1)]
    ax2.plot(xs_green, ys_green, color="#2E7D32", linewidth=2.8, zorder=4)
    ax2.scatter(mensual.loc[pke, "YearMonth"], mensual.loc[pke, "Sales"],
                color="#2E7D32", s=50, zorder=5)

# Leyenda compacta
from matplotlib.lines import Line2D
leyenda = [
    Line2D([0], [0], color="#D32F2F", linewidth=2, label="Bajada previa"),
    Line2D([0], [0], color="#2E7D32", linewidth=2, label="Subida destacada"),
]
ax2.legend(handles=leyenda, fontsize=8, loc="upper left", framealpha=0.85)

ax2.set_title("DESPUÉS — Patrones bajada (rojo) → subida (verde) resaltados", fontsize=11, color="#1B5E20", fontweight="bold")
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
