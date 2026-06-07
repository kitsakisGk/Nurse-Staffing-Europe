"""
Builds figures/dashboard.html — a single self-contained HTML file with
4 tabbed interactive dashboards built entirely with Plotly.
Run from the project root:  py notebooks/build_html_dashboard.py
"""
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import json, os

PROCESSED = 'data/processed/'
OUTPUTS   = 'data/outputs/'
OUT_FILE  = 'figures/dashboard.html'

# ── palette — nature tones ──────────────────────────────────────────────────
BG       = '#2c3e2d'   # deep forest green
CARD_BG  = '#1e2d1f'   # darker forest
PAGE_BG  = '#3a4f3b'   # medium forest green
TEXT     = '#f0f4e8'   # warm off-white
MUTED    = '#b8c9a3'   # sage green muted
GRID     = 'rgba(255,255,255,0.07)'
ACC      = ['#7ec8a0', '#e07b54', '#d4a843', '#5b9bd5']
REG_COL  = {'Northern': '#7ec8a0', 'Western': '#5b9bd5',
            'Southern': '#d4a843', 'Eastern': '#e07b54'}
CLUS_COL = ['#e07b54','#7ec8a0','#5b9bd5','#d4a843','#a678c8']
CLUS_LBL = {
    0: 'Low staffing / High AMI mortality',
    1: 'High staffing / Low mortality (Nordic)',
    2: 'High staffing / Long stays',
    3: 'Mid staffing / Mid outcomes',
    4: 'Mid staffing / High stroke mortality',
}
REGION_ORDER = ['Northern', 'Western', 'Southern', 'Eastern']

# ── load data ───────────────────────────────────────────────────────────────
df       = pd.read_csv(PROCESSED + 'master_dataset.csv')
reg_df   = pd.read_csv(OUTPUTS   + 'regression_results.csv')
clus_df  = pd.read_csv(OUTPUTS   + 'cluster_assignments.csv')

nurses = df['nurses_per_10k'].mean()
ami    = df['mortality_ami_30d'].mean()
stroke = df['mortality_stroke_30d'].mean()
los    = df['avg_length_of_stay'].mean()

region_avg  = (df.groupby('region')[['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d']]
               .mean().round(2).loc[REGION_ORDER])
region_year = df.groupby(['year','region'])['nurses_per_10k'].mean().reset_index()
country_avg = (df.groupby(['country','iso3','region'])
               [['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d','avg_length_of_stay']]
               .mean().round(2).reset_index().dropna(subset=['nurses_per_10k']))

CFEATS      = ['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d','avg_length_of_stay','gdp_per_capita']
cluster_plot= df.groupby('country')[CFEATS].mean().dropna().merge(clus_df, on='country')

outcomes = reg_df['Outcome'].tolist()
coefs    = reg_df['Coefficient'].tolist()
ci_low   = reg_df['95% CI Low'].tolist()
ci_high  = reg_df['95% CI High'].tolist()
pvals    = reg_df['p-value'].tolist()

LAYOUT_BASE = dict(
    paper_bgcolor=PAGE_BG, plot_bgcolor=CARD_BG,
    font=dict(color=TEXT, family='Inter, Arial, sans-serif'),
    margin=dict(t=60, b=40, l=60, r=40),
    xaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
    yaxis=dict(gridcolor=GRID, zerolinecolor=GRID),
)

def base_layout(**kwargs):
    d = dict(LAYOUT_BASE)
    d.update(kwargs)
    return d

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 1 — KPIs + Europe Map
# ══════════════════════════════════════════════════════════════════════════════
country_avg['hover'] = country_avg.apply(
    lambda r: (
        f"<b>{r['country']}</b><br>"
        f"Nurses / 10k pop: <b>{r['nurses_per_10k']:.0f}</b><br>"
        f"AMI Mortality: <b>{r['mortality_ami_30d']:.1f}%</b><br>"
        f"Stroke Mortality: <b>{r['mortality_stroke_30d']:.1f}%</b><br>"
        f"Avg Length of Stay: <b>{r['avg_length_of_stay']:.1f} days</b>"
    ), axis=1
)

fig1 = make_subplots(
    rows=2, cols=4,
    row_heights=[0.16, 0.84],
    specs=[
        [{'type':'domain'},{'type':'domain'},{'type':'domain'},{'type':'domain'}],
        [{'type':'choropleth','colspan':4}, None, None, None],
    ],
    vertical_spacing=0.02,
    subplot_titles=['','','','',''],
)

kpi_data = [
    ('Avg Nurse Density',    nurses,  '',      'per 10,000 pop', ACC[0]),
    ('Avg AMI Mortality',    ami,     '%',     '30-day rate',    ACC[1]),
    ('Avg Stroke Mortality', stroke,  '%',     '30-day rate',    ACC[2]),
    ('Avg Length of Stay',   los,     ' days', 'hospital stays', ACC[3]),
]
for ci, (title, val, suf, sub, color) in enumerate(kpi_data, start=1):
    fig1.add_trace(go.Indicator(
        mode='number',
        value=val,
        number=dict(suffix=suf, font=dict(size=42, color=color), valueformat='.1f'),
        title=dict(
            text=f"<b style='color:{MUTED};font-size:13px'>{title}</b>"
                 f"<br><span style='color:{color};font-size:11px'>{sub}</span>",
            font=dict(size=13)
        ),
        domain=dict(x=[0,1], y=[0,1]),
    ), row=1, col=ci)

fig1.add_trace(go.Choropleth(
    locations=country_avg['iso3'],
    z=country_avg['nurses_per_10k'],
    text=country_avg['hover'],
    hovertemplate='%{text}<extra></extra>',
    colorscale=[[0,'#fc5c65'],[0.35,'#fd9644'],[0.65,'#45aaf2'],[1,'#26de81']],
    colorbar=dict(
        title=dict(text='Nurses<br>per 10k', font=dict(color=MUTED, size=11)),
        tickfont=dict(color=MUTED), x=1.01, thickness=14, bgcolor='rgba(0,0,0,0)',
        outlinecolor='rgba(0,0,0,0)',
    ),
    marker_line_color='rgba(255,255,255,0.25)', marker_line_width=0.7,
    zmin=country_avg['nurses_per_10k'].min(),
    zmax=country_avg['nurses_per_10k'].max(),
), row=2, col=1)

fig1.update_geos(
    scope='europe', projection_type='natural earth',
    showcoastlines=True, coastlinecolor='rgba(255,255,255,0.15)',
    showland=True, landcolor='#1a3550',
    showocean=True, oceancolor=BG,
    showlakes=False, lakecolor=BG,
    showcountries=True, countrycolor='rgba(255,255,255,0.2)',
    bgcolor=PAGE_BG,
    lataxis_range=[34,72], lonaxis_range=[-12,45],
)
fig1.update_layout(
    **base_layout(
        title=dict(text='<b>Nurse Staffing & Patient Outcomes in Europe</b>  ·  2000–2023',
                   font=dict(size=18, color=TEXT), x=0.5, xanchor='center'),
        height=820, autosize=True,
        margin=dict(t=55, b=5, l=5, r=80),
        clickmode='event+select',
        plot_bgcolor=PAGE_BG,
    )
)

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 2 — Staffing Trends + Regional Bars
# ══════════════════════════════════════════════════════════════════════════════
fig2 = make_subplots(
    rows=2, cols=3,
    row_heights=[0.55, 0.45],
    specs=[[{'colspan':3}, None, None],
           [{}, {}, {}]],
    subplot_titles=[
        'Nurse Staffing Trends by European Region  (2000–2023)',
        'Nurses per 10,000', '30-day AMI Mortality (%)', '30-day Stroke Mortality (%)'
    ],
    vertical_spacing=0.14, horizontal_spacing=0.07,
)

for region in REGION_ORDER:
    grp = region_year[region_year['region'] == region]
    fig2.add_trace(go.Scatter(
        x=grp['year'], y=grp['nurses_per_10k'],
        name=region, mode='lines+markers',
        line=dict(color=REG_COL[region], width=2.5),
        marker=dict(size=5),
        hovertemplate=f'<b>{region}</b><br>Year: %{{x}}<br>Nurses/10k: %{{y:.1f}}<extra></extra>',
    ), row=1, col=1)

# COVID shading
fig2.add_vrect(x0=2020, x1=2022, fillcolor='#fc5c65', opacity=0.08,
               layer='below', line_width=0, row=1, col=1)
fig2.add_annotation(x=2021, y=region_year['nurses_per_10k'].max()*0.97,
                    text='COVID', font=dict(color='#fc5c65', size=9),
                    showarrow=False, row=1, col=1)

metrics_info = [
    ('nurses_per_10k', 2),
    ('mortality_ami_30d', 3),
    ('mortality_stroke_30d', 4),
]
for col_i, (col, col_num) in enumerate(metrics_info, start=1):
    vals = region_avg[col].tolist()
    colors = [REG_COL[r] for r in REGION_ORDER]
    fig2.add_trace(go.Bar(
        x=REGION_ORDER, y=vals,
        marker_color=colors, marker_line_width=0,
        text=[f'{v:.1f}' for v in vals],
        textposition='outside', textfont=dict(color=TEXT, size=10),
        hovertemplate='<b>%{x}</b><br>Value: %{y:.1f}<extra></extra>',
        showlegend=False,
    ), row=2, col=col_i)

fig2.update_layout(**base_layout(
    title=dict(text='<b>Staffing Trends & Regional Comparison</b>',
               font=dict(size=17, color=TEXT), x=0.5, xanchor='center'),
    height=700, autosize=True, showlegend=True,
    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)',
                font=dict(color=TEXT), x=0.01, y=0.98),
    margin=dict(t=70, b=40, l=55, r=30),
))
fig2.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
fig2.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
for ann in fig2.layout.annotations:
    ann.font.color = MUTED
    ann.font.size  = 11

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 3 — Clusters + Regression
# ══════════════════════════════════════════════════════════════════════════════
fig3 = make_subplots(
    rows=1, cols=2,
    subplot_titles=['Country Clusters: Staffing vs AMI Mortality',
                    'Fixed Effects Regression — Nurse Staffing → Outcomes'],
    horizontal_spacing=0.12,
)

for k in sorted(cluster_plot['cluster'].unique()):
    grp = cluster_plot[cluster_plot['cluster'] == k]
    fig3.add_trace(go.Scatter(
        x=grp['nurses_per_10k'], y=grp['mortality_ami_30d'],
        mode='markers+text',
        name=f'C{k}: {CLUS_LBL[k]}',
        marker=dict(color=CLUS_COL[k], size=14,
                    line=dict(color='white', width=0.8)),
        text=grp['country'], textposition='top right',
        textfont=dict(size=9, color=TEXT),
        hovertemplate=(
            '<b>%{text}</b><br>'
            'Nurses/10k: %{x:.0f}<br>'
            'AMI Mortality: %{y:.1f}%<extra></extra>'
        ),
    ), row=1, col=1)

# Forest plot
for i, (out, coef, lo, hi, pval) in enumerate(zip(outcomes, coefs, ci_low, ci_high, pvals)):
    bar_color = ACC[1] if pval < 0.05 else '#445566'
    fig3.add_trace(go.Scatter(
        x=[lo, hi], y=[i, i],
        mode='lines',
        line=dict(color='white', width=2.5),
        showlegend=False,
        hoverinfo='skip',
    ), row=1, col=2)
    fig3.add_trace(go.Scatter(
        x=[coef], y=[i],
        mode='markers',
        marker=dict(color=bar_color, size=14, symbol='diamond',
                    line=dict(color='white', width=1)),
        name=out,
        hovertemplate=f'<b>{out}</b><br>β={coef:.4f}<br>p={pval:.3f}<br>95% CI [{lo:.4f}, {hi:.4f}]<extra></extra>',
        showlegend=False,
    ), row=1, col=2)

fig3.add_vline(x=0, line_dash='dash', line_color=MUTED, opacity=0.5, row=1, col=2)
fig3.update_yaxes(
    tickvals=list(range(len(outcomes))),
    ticktext=outcomes,
    tickfont=dict(color=TEXT, size=10),
    row=1, col=2
)

fig3.update_layout(**base_layout(
    title=dict(text='<b>Country Clusters & Regression Findings</b>',
               font=dict(size=17, color=TEXT), x=0.5, xanchor='center'),
    height=600, autosize=True,
    legend=dict(bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.1)',
                font=dict(color=TEXT, size=9), x=0.52, y=0.98),
    margin=dict(t=65, b=40, l=55, r=30),
))
fig3.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
fig3.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
for ann in fig3.layout.annotations:
    ann.font.color = MUTED
    ann.font.size  = 11

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD 4 — Full overview (all in one scrollable page using subplots)
# ══════════════════════════════════════════════════════════════════════════════
fig4 = make_subplots(
    rows=4, cols=4,
    row_heights=[0.12, 0.30, 0.28, 0.30],
    specs=[
        [{'type':'domain'},{'type':'domain'},{'type':'domain'},{'type':'domain'}],
        [{'colspan':4,'type':'choropleth'}, None, None, None],
        [{'colspan':2}, None, {}, {}],
        [{'colspan':4}, None, None, None],
    ],
    subplot_titles=[
        '','','','',
        'Nurse Density by Country',
        'Staffing Trends by Region','Nurses/10k','AMI Mortality %',
        'Country Clusters: Staffing vs AMI Mortality',
    ],
    vertical_spacing=0.06, horizontal_spacing=0.06,
)

# KPIs
for ci, (title, val, suf, sub, color) in enumerate(kpi_data, start=1):
    fig4.add_trace(go.Indicator(
        mode='number', value=val,
        number=dict(suffix=suf, font=dict(size=34, color=color), valueformat='.1f'),
        title=dict(
            text=f"<b style='color:{MUTED};font-size:12px'>{title}</b>"
                 f"<br><span style='color:{color};font-size:10px'>{sub}</span>",
        ),
    ), row=1, col=ci)

# Map
fig4.add_trace(go.Choropleth(
    locations=country_avg['iso3'], z=country_avg['nurses_per_10k'],
    text=country_avg['hover'], hovertemplate='%{text}<extra></extra>',
    colorscale=[[0,'#fc5c65'],[0.35,'#fd9644'],[0.65,'#45aaf2'],[1,'#26de81']],
    colorbar=dict(title=dict(text='Nurses<br>/10k', font=dict(color=MUTED,size=10)),
                  tickfont=dict(color=MUTED), x=1.01, thickness=12,
                  bgcolor='rgba(0,0,0,0)', outlinecolor='rgba(0,0,0,0)'),
    marker_line_color='rgba(255,255,255,0.2)', marker_line_width=0.6,
    showscale=True,
), row=2, col=1)
fig4.update_geos(
    scope='europe', projection_type='natural earth',
    showcoastlines=True, coastlinecolor='rgba(255,255,255,0.1)',
    showland=True, landcolor='#1a3550',
    showocean=True, oceancolor=BG,
    showcountries=True, countrycolor='rgba(255,255,255,0.15)',
    bgcolor=PAGE_BG,
    lataxis_range=[34,72], lonaxis_range=[-12,45],
)

# Trends
for region in REGION_ORDER:
    grp = region_year[region_year['region'] == region]
    fig4.add_trace(go.Scatter(
        x=grp['year'], y=grp['nurses_per_10k'],
        name=region, mode='lines+markers',
        line=dict(color=REG_COL[region], width=2),
        marker=dict(size=4), showlegend=True,
        hovertemplate=f'{region}: %{{y:.1f}}<extra></extra>',
    ), row=3, col=1)
fig4.add_shape(type='rect', x0=2020, x1=2022, y0=0, y1=1,
               yref='paper', xref='x5',
               fillcolor='#fc5c65', opacity=0.07, line_width=0, layer='below')

# Regional bars
for col_i, col in enumerate(['nurses_per_10k','mortality_ami_30d'], start=3):
    vals   = region_avg[col].tolist()
    colors = [REG_COL[r] for r in REGION_ORDER]
    fig4.add_trace(go.Bar(
        x=REGION_ORDER, y=vals, marker_color=colors, marker_line_width=0,
        text=[f'{v:.1f}' for v in vals], textposition='outside',
        textfont=dict(color=TEXT, size=9), showlegend=False,
        hovertemplate='<b>%{x}</b>: %{y:.1f}<extra></extra>',
    ), row=3, col=col_i)

# Clusters
for k in sorted(cluster_plot['cluster'].unique()):
    grp = cluster_plot[cluster_plot['cluster'] == k]
    fig4.add_trace(go.Scatter(
        x=grp['nurses_per_10k'], y=grp['mortality_ami_30d'],
        mode='markers+text',
        name=f'C{k}: {CLUS_LBL[k]}',
        marker=dict(color=CLUS_COL[k], size=12, line=dict(color='white',width=0.6)),
        text=grp['country'], textposition='top right',
        textfont=dict(size=8, color=TEXT), showlegend=False,
        hovertemplate='<b>%{text}</b><br>Nurses/10k: %{x:.0f}<br>AMI: %{y:.1f}%<extra></extra>',
    ), row=4, col=1)

fig4.update_layout(**base_layout(
    title=dict(text='<b>Nurse Staffing & Patient Outcomes in Europe  —  Full Overview</b>  ·  2000–2023',
               font=dict(size=17, color=TEXT), x=0.5, xanchor='center'),
    height=1400, autosize=True,
    showlegend=True,
    legend=dict(bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.1)',
                font=dict(color=TEXT, size=9), x=0.01, y=0.62),
    margin=dict(t=65, b=40, l=55, r=80),
    plot_bgcolor=PAGE_BG,
))
fig4.update_xaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
fig4.update_yaxes(gridcolor=GRID, zerolinecolor=GRID, tickfont=dict(color=MUTED))
for ann in fig4.layout.annotations:
    ann.font.color = MUTED
    ann.font.size  = 10

# ══════════════════════════════════════════════════════════════════════════════
# BUILD SINGLE HTML WITH 4 TABS
# ══════════════════════════════════════════════════════════════════════════════
def fig_to_div(fig):
    return pyo.plot(fig, output_type='div', include_plotlyjs=False,
                    config={'displayModeBar': True, 'responsive': True})

div1 = fig_to_div(fig1)
div2 = fig_to_div(fig2)
div3 = fig_to_div(fig3)
div4 = fig_to_div(fig4)

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Nurse Staffing & Patient Outcomes in Europe</title>
<script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ height: 100%; }}
  body {{ background: {PAGE_BG}; font-family: Inter, Arial, sans-serif; color: {TEXT}; display: flex; flex-direction: column; }}
  header {{
    background: {BG};
    padding: 16px 32px;
    border-bottom: 2px solid #7ec8a0;
    display: flex; align-items: center; justify-content: space-between;
    flex-shrink: 0;
  }}
  header h1 {{ font-size: 17px; font-weight: 700; color: {TEXT}; }}
  header span {{ font-size: 12px; color: {MUTED}; }}
  .tab-bar {{
    display: flex; gap: 4px; padding: 12px 24px 0;
    background: {BG}; border-bottom: 1px solid rgba(255,255,255,0.08);
    flex-shrink: 0;
  }}
  .tab-btn {{
    padding: 9px 24px; border: none; cursor: pointer;
    border-radius: 6px 6px 0 0; font-size: 13px; font-weight: 600;
    background: rgba(255,255,255,0.06); color: {MUTED};
    transition: all 0.18s;
  }}
  .tab-btn:hover  {{ background: rgba(255,255,255,0.12); color: {TEXT}; }}
  .tab-btn.active {{ background: {PAGE_BG}; color: {TEXT}; border-bottom: 2px solid #7ec8a0; }}
  .tab-panel {{ display: none; padding: 12px 8px 8px; width: 100%; }}
  .tab-panel.active {{ display: flex; flex-direction: column; }}
  .dash-title {{ font-size: 12px; color: {MUTED}; padding: 0 0 6px 6px; font-weight: 500; }}
  .tab-panel .js-plotly-plot,
  .tab-panel .plotly-graph-div {{ width: 100% !important; }}
</style>
</head>
<body>
<header>
  <h1>Nurse Staffing &amp; Patient Outcomes in Europe</h1>
  <span>36 European countries &nbsp;·&nbsp; 2000–2023 &nbsp;·&nbsp; OECD / WHO / Eurostat data</span>
</header>

<div class="tab-bar">
  <button class="tab-btn active" onclick="showTab(0)">Overview &amp; Map</button>
  <button class="tab-btn"        onclick="showTab(1)">Trends &amp; Regions</button>
  <button class="tab-btn"        onclick="showTab(2)">Clusters &amp; Regression</button>
  <button class="tab-btn"        onclick="showTab(3)">Full Dashboard</button>
</div>

<div class="tab-panel active" id="panel0">
  <p class="dash-title">KPI summary &nbsp;·&nbsp; hover over a country to see its stats &nbsp;·&nbsp; colour = nurse density</p>
  {div1}
</div>
<div class="tab-panel" id="panel1">
  <p class="dash-title">Staffing trends over time (2000–2023) and average outcomes by European region</p>
  {div2}
</div>
<div class="tab-panel" id="panel2">
  <p class="dash-title">K-means country clusters (k=5) and fixed-effects panel regression coefficients</p>
  {div3}
</div>
<div class="tab-panel" id="panel3">
  <p class="dash-title">All panels combined — KPIs, map, trends, bars, and cluster scatter</p>
  {div4}
</div>

<script>
function showTab(idx) {{
  document.querySelectorAll('.tab-panel').forEach((p,i) => {{
    p.classList.toggle('active', i === idx);
  }});
  document.querySelectorAll('.tab-btn').forEach((b,i) => {{
    b.classList.toggle('active', i === idx);
  }});
  // Force Plotly to resize all charts in the newly visible panel
  setTimeout(() => {{
    const panel = document.querySelectorAll('.tab-panel')[idx];
    panel.querySelectorAll('.js-plotly-plot').forEach(el => {{
      Plotly.relayout(el, {{autosize: true}});
    }});
  }}, 50);
}}
// Resize all charts on window resize
window.addEventListener('resize', () => {{
  document.querySelectorAll('.tab-panel.active .js-plotly-plot').forEach(el => {{
    Plotly.relayout(el, {{autosize: true}});
  }});
}});
</script>
</body>
</html>"""

os.makedirs('figures', exist_ok=True)
with open(OUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'Done! Open this file in your browser:')
print(f'  {os.path.abspath(OUT_FILE)}')
