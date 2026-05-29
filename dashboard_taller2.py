"""
Taller 2 — Dashboard Analítico Interactivo
Universidad EAFIT · Maestría en Ciencia de Datos
Dataset: Superstore Sales (Kaggle)
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar

st.set_page_config(
    page_title="Superstore Analytics · EAFIT",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta UI (página clara)
C_PRIMARY = "#1E3A5F"
C_ACCENT  = "#E07A3A"
C_TEXT    = "#334155"
C_DARK    = "#1E293B"
C_GREEN   = "#6BAA7D"
C_RED     = "#E57373"

# Paleta gráficas (fondo oscuro)
CHART_BG    = "#0F172A"
CHART_PLOT  = "#1E293B"
CHART_TITLE = "#F1F5F9"
CHART_TEXT  = "#CBD5E1"
CHART_GRID  = "rgba(148,163,184,0.12)"
C_BAR       = "#64748B"
C_BAR_DIM   = "#475569"
C_LINE_MID  = "#94A3B8"
C_LINE_HI   = "#60A5FA"

FONT = "Segoe UI, Arial, sans-serif"
TITLE_SIZE = 13
TICK_SIZE = 10

PLOTLY_TEMPLATE = "plotly_dark"


def chart_layout(fig, title, height=380, right_margin=40, top_margin=48):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        title=dict(text=title, font=dict(size=TITLE_SIZE, family=FONT, color=CHART_TITLE)),
        font=dict(family=FONT, size=TICK_SIZE, color=CHART_TEXT),
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_PLOT,
        height=height,
        margin=dict(l=16, r=right_margin, t=top_margin, b=48),
        legend=dict(font=dict(color=CHART_TEXT)),
    )
    fig.update_xaxes(
        gridcolor=CHART_GRID, zerolinecolor=CHART_GRID,
        linecolor=CHART_GRID, tickfont=dict(color=CHART_TEXT),
        title_font=dict(color=CHART_TEXT),
    )
    fig.update_yaxes(
        gridcolor=CHART_GRID, zerolinecolor=CHART_GRID,
        linecolor=CHART_GRID, tickfont=dict(color=CHART_TEXT),
        title_font=dict(color=CHART_TEXT),
    )
    fig.update_traces(textfont=dict(color=CHART_TEXT, size=10))
    return fig


def insight_box(text, tone="neutral"):
    styles = {
        "neutral": ("#F8FAFC", C_PRIMARY),
        "accent":  ("#FEF7F3", C_ACCENT),
        "green":   ("#F4F8F5", C_GREEN),
    }
    bg, border = styles.get(tone, styles["neutral"])
    st.markdown(
        f"<div style='background:{bg};border-left:3px solid {border};"
        f"border-radius:0 6px 6px 0;padding:14px 18px;font-size:14px;"
        f"color:{C_TEXT};line-height:1.65;margin:8px 0 16px 0;'>{text}</div>",
        unsafe_allow_html=True,
    )


st.markdown("""
<style>
  html, body, [class*="css"] { font-family: "Segoe UI", Arial, sans-serif; color: #334155; }
  [data-testid="metric-container"] {
    background: white; border: 1px solid #E2E8F0; border-radius: 8px;
    padding: 14px 18px; box-shadow: none;
  }
  [data-testid="metric-container"] [data-testid="stMetricLabel"] {
    font-size: 11px; font-weight: 600; letter-spacing: 0.5px; color: #64748B;
  }
  [data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size: 22px; font-weight: 700; color: #1E293B;
  }
  .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #E2E8F0; }
  .stTabs [data-baseweb="tab"] {
    height: 38px; padding: 0 16px; background: #F8FAFC;
    border-radius: 6px 6px 0 0; font-weight: 600; font-size: 13px;
    border: 1px solid #E2E8F0; border-bottom: none; color: #64748B;
  }
  .stTabs [aria-selected="true"] {
    background: #1E3A5F !important; color: white !important; border-color: #1E3A5F;
  }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv("sales-forecasting/train.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True)
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], dayfirst=True)
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.quarter
    return df


def calc_cagr(df_src):
    pivot = df_src.pivot_table("Sales", "Sub-Category", "Year", aggfunc="sum").fillna(0)
    result = {}
    for sub in pivot.index:
        v15 = pivot.loc[sub, 2015] if 2015 in pivot.columns else 0
        v18 = pivot.loc[sub, 2018] if 2018 in pivot.columns else 0
        result[sub] = ((v18 / v15) ** (1 / 3) - 1) * 100 if v15 > 0 else np.nan
    return pd.Series(result, name="CAGR")


df_full = load_data()
cagr_series = calc_cagr(df_full)

with st.sidebar:
    st.markdown(f"""
    <div style='background:{C_PRIMARY};color:white;padding:14px;border-radius:8px;margin-bottom:12px;'>
      <div style='font-size:10px;letter-spacing:1.5px;opacity:0.75;'>EAFIT · MDS</div>
      <div style='font-size:16px;font-weight:700;margin-top:4px;'>Superstore Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Filtros")
    years = st.multiselect("Año", [2015, 2016, 2017, 2018], default=[2015, 2016, 2017, 2018])
    segments = st.multiselect("Segmento", sorted(df_full["Segment"].unique()), default=sorted(df_full["Segment"].unique()))
    categories = st.multiselect("Categoría", sorted(df_full["Category"].unique()), default=sorted(df_full["Category"].unique()))
    st.markdown("---")
    st.caption("Dataset: Superstore Sales · 9.800 registros · 2015–2018")

df = df_full[
    df_full["Year"].isin(years) &
    df_full["Segment"].isin(segments) &
    df_full["Category"].isin(categories)
].copy()

if df.empty:
    st.warning("No hay datos para los filtros seleccionados.")
    st.stop()

st.markdown(f"""
<div style='background:{C_PRIMARY};color:white;padding:28px 32px;border-radius:12px;margin-bottom:24px;'>
  <div style='font-size:11px;letter-spacing:1.5px;opacity:0.7;margin-bottom:6px;'>
    Universidad EAFIT · Taller 2
  </div>
  <div style='font-size:26px;font-weight:700;line-height:1.25;'>
    Análisis de portafolio y demanda — Superstore Sales
  </div>
  <div style='font-size:14px;opacity:0.85;margin-top:8px;'>
    Producto, estacionalidad y canasta de compra · 2015–2018
  </div>
</div>
""", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Ventas totales", f"${df['Sales'].sum()/1e6:.2f}M")
k2.metric("Pedidos", f"{df['Order ID'].nunique():,}")
k3.metric("Ticket promedio", f"${df['Sales'].sum()/df['Order ID'].nunique():,.0f}")
k4.metric("Clientes", f"{df['Customer ID'].nunique():,}")

tab_exploracion, tab_portafolio, tab_estacionalidad, tab_canasta = st.tabs([
    "Exploración",
    "Portafolio y Copiers",
    "Estacionalidad",
    "Canasta de compra",
])

# ── TAB EXPLORACIÓN (solo contexto, sin gráficas) ─────────────────────────────
with tab_exploracion:
    insight_box(
        "<strong>Pregunta de negocio:</strong> ¿Qué producto concentra el mayor potencial de crecimiento "
        "y en qué momentos del año se concentra la demanda?",
        "neutral",
    )
    st.markdown("#### Proceso de análisis")
    st.markdown("""
    Se trabajó sobre **9.800 líneas de pedido** (2015–2018) agrupando ventas por subcategoría,
    mes y pedido. El análisis partió de dos preguntas:

    1. **Volumen vs. crecimiento:** Phones y Chairs lideran en ventas totales, pero el crecimiento
       sostenido no siempre coincide con el volumen.
    2. **Estacionalidad:** La demanda no se reparte de forma uniforme; ciertos meses concentran
       una fracción desproporcionada del año.

    Para medir crecimiento usamos el **CAGR** (*Compound Annual Growth Rate*, tasa de crecimiento
    anual compuesta): indica cuánto crece una serie en promedio cada año, suponiendo reinversión
    del crecimiento. Se calcula como `(Ventas₂₀₁₈ / Ventas₂₀₁₅)^(1/3) − 1`. Un CAGR de +79,6 %
    significa que Copiers duplicó su escala varias veces en cuatro años, aunque partió de una base pequeña.
    """)

    st.markdown("#### Hallazgos principales")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        **Copiers como apuesta de portafolio**

        - 66 pedidos en cuatro años; ticket promedio **$2.216** (≈10× el promedio general).
        - Ventas: $10.850 (2015) → $62.899 (2018).
        - **CAGR +79,6 %**, el más alto del portafolio.
        - Canon imageCLASS 2200 concentra ~42 % de las ventas de la subcategoría.
        """)
    with c2:
        st.markdown("""
        **Estacionalidad y canasta**

        - Sep + Nov + Dic ≈ **43 %** de las ventas anuales; febrero es el mes más bajo.
        - Copiers concentra **48,5 %** de sus ventas en Q4.
        - En pedidos con Copiers, **Binders** y **Paper** aparecen en ~29 % de los casos.
        - **Machines** cae (−11,1 % CAGR) mientras Copiers crece.
        """)

    st.markdown("""
    Las visualizaciones de este análisis están en las pestañas **Portafolio y Copiers**,
    **Estacionalidad** y **Canasta de compra**, organizadas por tema.
    """)


# ── TAB PORTAFOLIO + COPIERS (unificado) ─────────────────────────────────────
with tab_portafolio:
    insight_box(
        "<strong>Pregunta de negocio:</strong> ¿Dónde conviene invertir dentro del portafolio y "
        "por qué Copiers destaca frente al resto?",
        "accent",
    )

    cop_df = df_full[
        (df_full["Sub-Category"] == "Copiers") &
        (df_full["Year"].isin(years)) &
        (df_full["Segment"].isin(segments))
    ]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ventas Copiers", f"${cop_df['Sales'].sum():,.0f}")
    c2.metric("CAGR 2015→2018", "+79,6 %")
    c3.metric("Ticket Copiers", f"${cop_df['Sales'].mean():,.0f}" if len(cop_df) else "—")
    c4.metric("Pedidos Copiers", f"{cop_df['Order ID'].nunique()}")

    st.markdown(
        "El **CAGR** mide el crecimiento promedio anual entre 2015 y 2018. "
        "Copiers arranca con poco volumen pero crece mucho más rápido que el resto."
    )

    # Gráfica 1: ventas por subcategoría (sin CAGR)
    st.markdown("#### Ventas totales por subcategoría")
    sub_sales = df.groupby("Sub-Category")["Sales"].sum().sort_values(ascending=True).reset_index()
    colors_vol = [C_ACCENT if s == "Copiers" else C_BAR for s in sub_sales["Sub-Category"]]

    fig_vol = go.Figure(go.Bar(
        x=sub_sales["Sales"],
        y=sub_sales["Sub-Category"],
        orientation="h",
        marker_color=colors_vol,
        text=[f"${v/1000:.0f}K" for v in sub_sales["Sales"]],
        textposition="outside",
        hovertemplate="<b>%{y}</b><br>$%{x:,.0f}<extra></extra>",
    ))
    chart_layout(
        fig_vol,
        "Copiers no lidera en volumen; Phones y Chairs concentran más ventas absolutas",
        height=440,
        right_margin=80,
    )
    fig_vol.update_xaxes(visible=False)
    st.plotly_chart(fig_vol, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("#### CAGR por subcategoría")
        cagr_df = cagr_series.dropna().sort_values(ascending=True).reset_index()
        cagr_df.columns = ["Sub-Category", "CAGR"]
        cagr_colors = [
            C_ACCENT if s == "Copiers" else C_RED if v < 0 else C_BAR
            for s, v in zip(cagr_df["Sub-Category"], cagr_df["CAGR"])
        ]
        fig_cagr = go.Figure(go.Bar(
            x=cagr_df["CAGR"],
            y=cagr_df["Sub-Category"],
            orientation="h",
            marker_color=cagr_colors,
            text=[f"{v:+.1f}%" for v in cagr_df["CAGR"]],
            textposition="outside",
        ))
        fig_cagr.add_vline(x=0, line_color=CHART_TEXT, line_width=1)
        chart_layout(fig_cagr, "Tasa de crecimiento anual compuesta 2015–2018", height=400, right_margin=70)
        fig_cagr.update_xaxes(title="CAGR (%)", ticksuffix="%")
        st.plotly_chart(fig_cagr, use_container_width=True)

    with col_b:
        st.markdown("#### Evolución anual de ventas")
        top_growers = cagr_series.nlargest(5).index.tolist()
        traj = (
            df_full[df_full["Sub-Category"].isin(top_growers)]
            .groupby(["Year", "Sub-Category"])["Sales"].sum().reset_index()
        )
        fig_traj = go.Figure()
        for sub in top_growers:
            d = traj[traj["Sub-Category"] == sub]
            fig_traj.add_trace(go.Scatter(
                x=d["Year"], y=d["Sales"],
                mode="lines+markers",
                name=sub,
                line=dict(
                    color=C_ACCENT if sub == "Copiers" else C_BAR,
                    width=2.5 if sub == "Copiers" else 1.5,
                ),
                marker=dict(size=7 if sub == "Copiers" else 5),
            ))
        chart_layout(fig_traj, "Trayectoria de las cinco subcategorías de mayor CAGR", height=400)
        fig_traj.update_xaxes(tickmode="array", tickvals=sorted(traj["Year"].unique()))
        fig_traj.update_yaxes(title="Ventas ($)", tickformat="$,.0f")
        fig_traj.update_layout(legend=dict(orientation="h", y=-0.22, font=dict(size=10)))
        st.plotly_chart(fig_traj, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("#### Ticket promedio por pedido")
        ticket_df = (
            df.groupby("Sub-Category")
            .apply(lambda x: x["Sales"].sum() / x["Order ID"].nunique())
            .sort_values(ascending=True)
            .reset_index()
        )
        ticket_df.columns = ["Sub-Category", "Ticket"]
        t_colors = [C_ACCENT if s == "Copiers" else C_BAR for s in ticket_df["Sub-Category"]]
        avg_t = df["Sales"].sum() / df["Order ID"].nunique()
        fig_ticket = go.Figure(go.Bar(
            x=ticket_df["Ticket"],
            y=ticket_df["Sub-Category"],
            orientation="h",
            marker_color=t_colors,
            text=[f"${v:,.0f}" for v in ticket_df["Ticket"]],
            textposition="outside",
        ))
        fig_ticket.add_vline(x=avg_t, line_dash="dash", line_color=C_LINE_HI, line_width=1)
        chart_layout(fig_ticket, f"Ticket promedio general: ${avg_t:,.0f}", height=400, right_margin=90)
        fig_ticket.update_xaxes(visible=False)
        st.plotly_chart(fig_ticket, use_container_width=True)

    with col_d:
        st.markdown("#### Ventas de Copiers por mes")
        cop_month = (
            cop_df.groupby("Month")["Sales"].sum()
            .reindex(range(1, 13), fill_value=0)
            .reset_index()
        )
        cop_month["MonthAbbr"] = [calendar.month_abbr[m] for m in cop_month["Month"]]
        m_colors = [C_ACCENT if m in [10, 11, 12] else C_BAR_DIM for m in cop_month["Month"]]
        fig_cop_m = go.Figure(go.Bar(
            x=cop_month["MonthAbbr"],
            y=cop_month["Sales"],
            marker_color=m_colors,
            text=[f"${v/1000:.0f}K" if v > 0 else "" for v in cop_month["Sales"]],
            textposition="outside",
        ))
        chart_layout(fig_cop_m, "Octubre y noviembre concentran buena parte de las ventas de Copiers", height=400)
        fig_cop_m.update_yaxes(title="Ventas ($)", tickformat="$,.0f", range=[0, cop_month["Sales"].max() * 1.18])
        st.plotly_chart(fig_cop_m, use_container_width=True)

    st.markdown("#### Productos principales en Copiers")
    cop_prod = (
        cop_df.groupby("Product Name")
        .agg(Ventas=("Sales", "sum"), Pedidos=("Order ID", "nunique"))
        .sort_values("Ventas", ascending=False)
        .head(8)
        .reset_index()
    )
    p_colors = [C_ACCENT if i == 0 else C_BAR for i in range(len(cop_prod))]
    fig_prod = go.Figure(go.Bar(
        x=cop_prod["Ventas"][::-1],
        y=cop_prod["Product Name"][::-1],
        orientation="h",
        marker_color=p_colors[::-1],
        text=[f"${v:,.0f}" for v in cop_prod["Ventas"][::-1]],
        textposition="outside",
    ))
    chart_layout(fig_prod, "Canon imageCLASS 2200 concentra la mayor parte del volumen", height=320, right_margin=120)
    fig_prod.update_xaxes(visible=False)
    st.plotly_chart(fig_prod, use_container_width=True)


# ── TAB ESTACIONALIDAD ────────────────────────────────────────────────────────
with tab_estacionalidad:
    insight_box(
        "<strong>Pregunta de negocio:</strong> ¿En qué meses y trimestres se concentra la demanda?",
        "neutral",
    )

    mensual_df = df.groupby(["Year", "Month"])["Sales"].sum().reset_index()
    q4_pct = df[df["Quarter"] == 4]["Sales"].sum() / df["Sales"].sum() * 100
    best_month = calendar.month_name[df.groupby("Month")["Sales"].sum().idxmax()]

    s1, s2, s3 = st.columns(3)
    s1.metric("Mes con más ventas", best_month)
    s2.metric("Ventas en Q4", f"{q4_pct:.1f} %")
    s3.metric("Nov / Feb", f"{df[df['Month']==11]['Sales'].sum()/max(df[df['Month']==2]['Sales'].sum(),1):.1f}×")

    st.markdown("#### Mapa de calor mensual")
    heat_data = df.groupby(["Year", "Month"])["Sales"].sum().reset_index()
    heat_pivot = heat_data.pivot(index="Month", columns="Year", values="Sales").fillna(0)
    heat_pivot = heat_pivot.reindex(columns=sorted(heat_pivot.columns))
    month_labels = [calendar.month_abbr[m] for m in heat_pivot.index]
    year_labels = [str(int(y)) for y in heat_pivot.columns]

    fig_heat = go.Figure(go.Heatmap(
        z=heat_pivot.values,
        x=year_labels,
        y=month_labels,
        colorscale=[[0, "#1E293B"], [0.35, "#334155"], [0.65, "#475569"], [1, "#60A5FA"]],
        text=[[f"${v/1000:.0f}K" for v in row] for row in heat_pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=10, family=FONT, color=CHART_TEXT),
        hovertemplate="<b>%{y} %{x}</b><br>$%{z:,.0f}<extra></extra>",
        colorbar=dict(
            tickformat="$,.0f",
            tickfont=dict(color=CHART_TEXT),
            title=dict(text="Ventas", font=dict(color=CHART_TEXT)),
        ),
    ))
    chart_layout(
        fig_heat,
        "Septiembre, noviembre y diciembre repiten el patrón de mayor demanda",
        height=400,
    )
    fig_heat.update_xaxes(type="category", title="Año")
    fig_heat.update_yaxes(type="category", autorange="reversed", title="Mes")
    st.plotly_chart(fig_heat, use_container_width=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### Ventas mensuales por año")
        month_order = [calendar.month_abbr[m] for m in range(1, 13)]
        line_palette = {2015: C_BAR_DIM, 2016: C_BAR, 2017: C_LINE_MID, 2018: C_ACCENT}
        fig_lines = go.Figure()
        for yr in sorted(mensual_df["Year"].unique()):
            yr_data = mensual_df[mensual_df["Year"] == yr].sort_values("Month")
            yr_data["MonthAbbr"] = [calendar.month_abbr[m] for m in yr_data["Month"]]
            fig_lines.add_trace(go.Scatter(
                x=yr_data["MonthAbbr"], y=yr_data["Sales"],
                mode="lines+markers",
                name=str(yr),
                line=dict(color=line_palette.get(yr, C_BAR), width=2.2 if yr == 2018 else 1.5),
                marker=dict(size=6),
            ))
        chart_layout(fig_lines, "Comparación de la curva mensual entre años", height=360)
        fig_lines.update_xaxes(categoryorder="array", categoryarray=month_order)
        fig_lines.update_yaxes(tickformat="$,.0f")
        fig_lines.update_layout(legend=dict(orientation="h", y=-0.22, font=dict(size=10)))
        st.plotly_chart(fig_lines, use_container_width=True)

    with col_r:
        st.markdown("#### Participación de Q4 por subcategoría")
        q4_by_sub = df.groupby(["Sub-Category", "Quarter"])["Sales"].sum().reset_index()
        q4_total = q4_by_sub.groupby("Sub-Category")["Sales"].sum()
        q4_only = q4_by_sub[q4_by_sub["Quarter"] == 4].set_index("Sub-Category")["Sales"]
        q4_pct_sub = (q4_only / q4_total * 100).sort_values(ascending=True).reset_index()
        q4_pct_sub.columns = ["Sub-Category", "Q4_pct"]
        q4_colors = [C_ACCENT if s == "Copiers" else C_BAR for s in q4_pct_sub["Sub-Category"]]
        fig_q4 = go.Figure(go.Bar(
            x=q4_pct_sub["Q4_pct"],
            y=q4_pct_sub["Sub-Category"],
            orientation="h",
            marker_color=q4_colors,
            text=[f"{v:.1f}%" for v in q4_pct_sub["Q4_pct"]],
            textposition="outside",
        ))
        fig_q4.add_vline(x=25, line_dash="dot", line_color=C_BAR)
        chart_layout(fig_q4, "Copiers depende más de Q4 que la mayoría de subcategorías", height=360, right_margin=60)
        fig_q4.update_xaxes(title="% en Q4", ticksuffix="%")
        st.plotly_chart(fig_q4, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown("#### Perfil mensual por categoría")
        cat_month = df.groupby(["Category", "Month"])["Sales"].sum().reset_index()
        cat_month["MonthAbbr"] = [calendar.month_abbr[m] for m in cat_month["Month"]]
        cat_month["Pct"] = cat_month["Sales"] / cat_month.groupby("Category")["Sales"].transform("sum") * 100
        cat_palette = {"Technology": C_ACCENT, "Furniture": C_LINE_HI, "Office Supplies": C_GREEN}
        fig_cat = go.Figure()
        for cat in ["Technology", "Furniture", "Office Supplies"]:
            d = cat_month[cat_month["Category"] == cat].sort_values("Month")
            fig_cat.add_trace(go.Scatter(
                x=d["MonthAbbr"], y=d["Pct"],
                mode="lines+markers",
                name=cat,
                line=dict(color=cat_palette[cat], width=2),
                marker=dict(size=5),
            ))
        chart_layout(fig_cat, "Cada categoría tiene un mes pico distinto", height=340)
        fig_cat.update_xaxes(categoryorder="array", categoryarray=month_order)
        fig_cat.update_yaxes(title="% del año", ticksuffix="%")
        fig_cat.update_layout(legend=dict(orientation="h", y=-0.25, font=dict(size=10)))
        st.plotly_chart(fig_cat, use_container_width=True)

    with col_r2:
        st.markdown("#### Ventas trimestrales")
        q_data = df.groupby(["Year", "Quarter"])["Sales"].sum().reset_index()
        q_data["Label"] = q_data.apply(lambda r: f"{int(r['Year'])} Q{int(r['Quarter'])}", axis=1)
        q_colors = [C_ACCENT if q == 4 else C_BAR for q in q_data["Quarter"]]
        y_max = q_data["Sales"].max() * 1.22
        fig_qtr = go.Figure(go.Bar(
            x=q_data["Label"],
            y=q_data["Sales"],
            marker_color=q_colors,
            text=[f"${v/1000:.0f}K" for v in q_data["Sales"]],
            textposition="outside",
            cliponaxis=False,
        ))
        chart_layout(fig_qtr, "Q4 supera al resto de trimestres en todos los años", height=340, top_margin=52)
        fig_qtr.update_xaxes(tickangle=-40, tickfont=dict(size=9))
        fig_qtr.update_yaxes(tickformat="$,.0f", range=[0, y_max])
        st.plotly_chart(fig_qtr, use_container_width=True)


# ── TAB CANASTA ───────────────────────────────────────────────────────────────
with tab_canasta:
    insight_box(
        "<strong>Pregunta de negocio:</strong> ¿Qué productos se compran junto con Copiers y "
        "cómo se distribuye el valor entre clientes?",
        "green",
    )

    copier_orders = set(
        df_full[(df_full["Sub-Category"] == "Copiers") & (df_full["Year"].isin(years))]["Order ID"]
    )
    basket = df_full[
        df_full["Order ID"].isin(copier_orders) & (df_full["Sub-Category"] != "Copiers")
    ]
    basket_agg = (
        basket.groupby("Sub-Category")
        .agg(Pedidos=("Order ID", "nunique"), Ventas=("Sales", "sum"))
        .reset_index()
        .sort_values("Pedidos", ascending=False)
    )
    basket_agg["Pct"] = basket_agg["Pedidos"] / max(len(copier_orders), 1) * 100

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown("#### Productos que acompañan a Copiers")
        b_sorted = basket_agg.sort_values("Pedidos", ascending=True)
        b_colors = [
            C_GREEN if s in ["Binders", "Paper"] else C_BAR
            for s in b_sorted["Sub-Category"]
        ]
        fig_basket = go.Figure(go.Bar(
            x=b_sorted["Pedidos"],
            y=b_sorted["Sub-Category"],
            orientation="h",
            marker_color=b_colors,
            text=[f"{int(v)} ({p:.0f}%)" for v, p in zip(b_sorted["Pedidos"], b_sorted["Pct"])],
            textposition="outside",
        ))
        chart_layout(fig_basket, "Binders y Paper aparecen en casi 3 de cada 10 pedidos con Copiers", height=380, right_margin=100)
        fig_basket.update_xaxes(title="N.º de pedidos")
        st.plotly_chart(fig_basket, use_container_width=True)

    with col_r:
        st.markdown("#### Valor de la canasta complementaria")
        basket_tree = basket_agg[basket_agg["Ventas"] > 0].copy()
        basket_tree["Categoria"] = basket_tree["Sub-Category"].map(
            df_full.drop_duplicates("Sub-Category").set_index("Sub-Category")["Category"]
        )
        fig_tree = px.treemap(
            basket_tree,
            path=["Categoria", "Sub-Category"],
            values="Ventas",
            color="Pct",
            color_continuous_scale=[[0, "#1E293B"], [0.5, "#475569"], [1, "#60A5FA"]],
        )
        fig_tree.update_traces(texttemplate="<b>%{label}</b><br>$%{value:,.0f}")
        chart_layout(fig_tree, "Storage y Phones aportan el mayor valor en dólares", height=380)
        st.plotly_chart(fig_tree, use_container_width=True)

    col_l2, col_r2 = st.columns(2)

    with col_l2:
        st.markdown("#### Segmento de comprador")
        seg_cop = (
            df_full[(df_full["Sub-Category"] == "Copiers") & (df_full["Year"].isin(years))]
            .groupby("Segment")["Sales"].sum()
        )
        seg_all = df.groupby("Segment")["Sales"].sum()
        segs = sorted(set(seg_cop.index) | set(seg_all.index))
        fig_seg = go.Figure()
        fig_seg.add_trace(go.Bar(
            name="Copiers", x=segs,
            y=(seg_cop / seg_cop.sum() * 100).reindex(segs, fill_value=0),
            marker_color=C_ACCENT,
        ))
        fig_seg.add_trace(go.Bar(
            name="Total", x=segs,
            y=(seg_all / seg_all.sum() * 100).reindex(segs, fill_value=0),
            marker_color=C_BAR,
        ))
        chart_layout(fig_seg, "El perfil de segmento de Copiers es similar al del portafolio", height=340)
        fig_seg.update_layout(barmode="group", legend=dict(orientation="h", y=-0.22))
        fig_seg.update_yaxes(ticksuffix="%")
        st.plotly_chart(fig_seg, use_container_width=True)

    with col_r2:
        st.markdown("#### Concentración de clientes")
        clientes = df.groupby("Customer ID")["Sales"].sum().sort_values(ascending=False).reset_index()
        clientes["Pct_clientes"] = (clientes.index + 1) / len(clientes) * 100
        clientes["Pct_ventas"] = clientes["Sales"].cumsum() / clientes["Sales"].sum() * 100
        fig_pareto = go.Figure()
        fig_pareto.add_trace(go.Scatter(
            x=clientes["Pct_clientes"], y=clientes["Pct_ventas"],
            mode="lines", line=dict(color=C_LINE_HI, width=2),
            name="Acumulado",
        ))
        fig_pareto.add_trace(go.Scatter(
            x=[0, 100], y=[0, 100], mode="lines",
            line=dict(color=C_BAR_DIM, dash="dash"), name="Referencia",
        ))
        chart_layout(fig_pareto, "El 5 % de clientes concentra ~20 % de las ventas", height=340)
        fig_pareto.update_xaxes(title="% clientes (acum.)", ticksuffix="%")
        fig_pareto.update_yaxes(title="% ventas (acum.)", ticksuffix="%")
        fig_pareto.update_layout(legend=dict(orientation="h", y=-0.22))
        st.plotly_chart(fig_pareto, use_container_width=True)

    st.markdown("#### Technology: evolución por subcategoría")
    tech_evol = (
        df_full[df_full["Category"] == "Technology"]
        .groupby(["Year", "Sub-Category"])["Sales"].sum().reset_index()
    )
    tech_palette = {"Copiers": C_ACCENT, "Phones": C_LINE_HI, "Accessories": C_GREEN, "Machines": C_RED}
    fig_tech = go.Figure()
    for sub in ["Copiers", "Phones", "Accessories", "Machines"]:
        d = tech_evol[tech_evol["Sub-Category"] == sub].sort_values("Year")
        fig_tech.add_trace(go.Scatter(
            x=d["Year"], y=d["Sales"],
            mode="lines+markers",
            name=sub,
            line=dict(color=tech_palette[sub], width=2.5 if sub == "Copiers" else 1.8),
            marker=dict(size=6),
        ))
    chart_layout(fig_tech, "Copiers crece; Machines retrocede en el mismo periodo", height=360)
    fig_tech.update_xaxes(tickmode="array", tickvals=[2015, 2016, 2017, 2018])
    fig_tech.update_yaxes(tickformat="$,.0f")
    fig_tech.update_layout(legend=dict(orientation="h", y=-0.22))
    st.plotly_chart(fig_tech, use_container_width=True)

st.markdown(f"""
<div style='background:{C_DARK};color:#CBD5E1;padding:20px;border-radius:8px;
            text-align:center;font-size:12px;margin-top:20px;'>
  Taller 2 · Universidad EAFIT · Superstore Sales (Kaggle) · 2015–2018
</div>
""", unsafe_allow_html=True)
