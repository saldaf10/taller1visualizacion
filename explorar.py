import pandas as pd
import numpy as np
import json

df = pd.read_csv('sales-forecasting/train.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
df['year']  = df['Order Date'].dt.year
df['month'] = df['Order Date'].dt.month

mensual = df.groupby(['year','month'])['Sales'].sum().reset_index().sort_values(['year','month']).reset_index(drop=True)
mensual['pct_change'] = mensual['Sales'].pct_change() * 100
mensual.loc[mensual['month'] == 1, 'pct_change'] = None  # quitar transicion dic->ene

labels = [f"{int(r['year'])}-{int(r['month']):02d}" for _, r in mensual.iterrows()]
pcts   = [round(r['pct_change'], 1) if pd.notna(r['pct_change']) else None for _, r in mensual.iterrows()]
sales  = [round(r['Sales'], 0) for _, r in mensual.iterrows()]

print("LABELS =", json.dumps(labels))
print("PCTS =",   json.dumps(pcts))
print("SALES =",  json.dumps(sales))

valid = [(labels[i], v) for i,v in enumerate(pcts) if v is not None]
valid_sorted = sorted(valid, key=lambda x: x[1])
print()
print("Bottom 5:", valid_sorted[:5])
print("Top 5:   ", valid_sorted[-5:])

# Caso 2: cada mes, los 4 años
print()
print("=== Febrero ===")
feb = df[df['month']==2].groupby('year')['Sales'].sum().round(0)
print(feb)

print()
print("=== Marzo ===")
mar = df[df['month']==3].groupby('year')['Sales'].sum().round(0)
print(mar)

print()
print("=== Todas las categorias, tendencia por anio ===")
cat_year = df.groupby(['year','Category'])['Sales'].sum().unstack()
print(cat_year.round(0))
