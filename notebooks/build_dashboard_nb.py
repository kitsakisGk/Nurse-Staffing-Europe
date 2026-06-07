import json

setup_src = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

PROCESSED = '../data/processed/'
OUTPUTS   = '../data/outputs/'
FIGURES   = '../figures/'

BG       = '#1e3d59'
CARD_BG  = '#16324f'
PAGE_BG  = '#243b55'
TEXT     = 'white'
MUTED    = '#c8d6e5'
COLORS   = {'Northern': '#26de81', 'Western': '#45aaf2', 'Southern': '#fed330', 'Eastern': '#fc5c65'}
ACC      = ['#45aaf2', '#fc5c65', '#fd9644', '#26de81']
REGION_ORDER = ['Northern', 'Western', 'Southern', 'Eastern']

cluster_labels = {
    0: 'Low staffing / High AMI mortality',
    1: 'High staffing / Low mortality (Nordic)',
    2: 'High staffing / Long stays',
    3: 'Mid staffing / Mid outcomes',
    4: 'Mid staffing / High stroke mortality',
}
cluster_colors = ['#fc5c65', '#26de81', '#45aaf2', '#fd9644', '#a55eea']

df       = pd.read_csv(PROCESSED + 'master_dataset.csv')
reg_df   = pd.read_csv(OUTPUTS   + 'regression_results.csv')
clus_df  = pd.read_csv(OUTPUTS   + 'cluster_assignments.csv')

nurses = df['nurses_per_10k'].mean()
ami    = df['mortality_ami_30d'].mean()
stroke = df['mortality_stroke_30d'].mean()
los    = df['avg_length_of_stay'].mean()

region_avg  = df.groupby('region')[['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d']].mean().round(2).loc[REGION_ORDER]
region_year = df.groupby(['year','region'])['nurses_per_10k'].mean().reset_index()
country_avg = df.groupby(['country','iso3','region'])[['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d','avg_length_of_stay']].mean().round(2).reset_index().dropna(subset=['nurses_per_10k'])

CLUSTER_FEATURES = ['nurses_per_10k','mortality_ami_30d','mortality_stroke_30d','avg_length_of_stay','gdp_per_capita']
cluster_plot = df.groupby('country')[CLUSTER_FEATURES].mean().dropna().merge(clus_df, on='country')

outcomes = reg_df['Outcome'].tolist()
coefs    = reg_df['Coefficient'].tolist()
ci_low   = reg_df['95% CI Low'].tolist()
ci_high  = reg_df['95% CI High'].tolist()
pvals    = reg_df['p-value'].tolist()
y_pos    = list(range(len(outcomes)))

metrics = [
    ('nurses_per_10k',       'Nurses per 10,000',           ACC[0]),
    ('mortality_ami_30d',    '30-day AMI Mortality (%)',    ACC[1]),
    ('mortality_stroke_30d', '30-day Stroke Mortality (%)', ACC[2]),
]

print(f"Loaded: {df.shape} | {df['country'].nunique()} countries")
print(f"nurses={nurses:.1f}, ami={ami:.2f}%, stroke={stroke:.2f}%, los={los:.1f} days")
"""

d1_src = """country_avg['hover'] = country_avg.apply(
    lambda r: (
        f"<b>{r['country']}</b><br>"
        f"Nurses/10k: {r['nurses_per_10k']:.0f}<br>"
        f"AMI Mortality: {r['mortality_ami_30d']:.1f}%<br>"
        f"Stroke Mortality: {r['mortality_stroke_30d']:.1f}%<br>"
        f"Avg LOS: {r['avg_length_of_stay']:.1f} days"
    ),
    axis=1
)

fig = make_subplots(
    rows=2, cols=4,
    row_heights=[0.18, 0.82],
    specs=[
        [{'type':'domain'},{'type':'domain'},{'type':'domain'},{'type':'domain'}],
        [{'type':'choropleth','colspan':4}, None, None, None]
    ],
    vertical_spacing=0.02
)

kpi_vals = [
    ('Avg Nurse Density',    nurses,  '',      'per 10,000 pop',  ACC[0]),
    ('Avg AMI Mortality',    ami,     '%',     '30-day rate',     ACC[1]),
    ('Avg Stroke Mortality', stroke,  '%',     '30-day rate',     ACC[2]),
    ('Avg Length of Stay',   los,     ' days', 'hospital stays',  ACC[3]),
]
for col_i, (title, value, suffix, subtitle, color) in enumerate(kpi_vals, start=1):
    fig.add_trace(go.Indicator(
        mode='number',
        value=value,
        number={'suffix': suffix, 'font': {'size': 38, 'color': color}, 'valueformat': '.1f'},
        title={'text': f"<b>{title}</b><br><span style='font-size:11px;color:{MUTED}'>{subtitle}</span>",
               'font': {'size': 13, 'color': MUTED}},
    ), row=1, col=col_i)

fig.add_trace(go.Choropleth(
    locations=country_avg['iso3'],
    z=country_avg['nurses_per_10k'],
    text=country_avg['hover'],
    hovertemplate='%{text}<extra></extra>',
    colorscale=[[0.0,'#fc5c65'],[0.35,'#fd9644'],[0.65,'#45aaf2'],[1.0,'#26de81']],
    colorbar=dict(
        title=dict(text='Nurses<br>per 10k', font=dict(color=MUTED, size=11)),
        tickfont=dict(color=MUTED), x=1.01, thickness=14, bgcolor='rgba(0,0,0,0)'
    ),
    marker_line_color='rgba(255,255,255,0.3)',
    marker_line_width=0.8,
    zmin=country_avg['nurses_per_10k'].min(),
    zmax=country_avg['nurses_per_10k'].max(),
), row=2, col=1)

fig.update_geos(
    scope='europe', projection_type='natural earth',
    showcoastlines=True, coastlinecolor='rgba(255,255,255,0.2)',
    showland=True, landcolor='#16324f',
    showocean=True, oceancolor='#1e3d59',
    showlakes=False,
    showcountries=True, countrycolor='rgba(255,255,255,0.2)',
    bgcolor=PAGE_BG,
    lataxis_range=[34, 72], lonaxis_range=[-12, 45],
)

fig.update_layout(
    title=dict(text='<b>Nurse Staffing & Patient Outcomes in Europe</b>  |  2000-2023',
               font=dict(size=18, color=TEXT), x=0.5, xanchor='center'),
    paper_bgcolor=PAGE_BG, plot_bgcolor=PAGE_BG,
    font=dict(color=TEXT),
    margin=dict(t=60, b=10, l=10, r=80),
    height=820, clickmode='event+select',
)

out_path = FIGURES + 'dashboard_1_interactive.html'
pyo.plot(fig, filename=out_path, auto_open=False)
print(f'Saved: {out_path}')
fig.show()
"""

d2_src = """fig = plt.figure(figsize=(18, 13))
fig.patch.set_facecolor(PAGE_BG)
fig.suptitle('Nurse Staffing — Trends & Regional Comparison',
             color=TEXT, fontsize=15, fontweight='bold', y=0.98)

gs = gridspec.GridSpec(2, 1, figure=fig, hspace=0.38, top=0.94, bottom=0.06)

ax = fig.add_subplot(gs[0])
ax.set_facecolor(CARD_BG)
for region in REGION_ORDER:
    grp = region_year[region_year['region'] == region]
    ax.plot(grp['year'], grp['nurses_per_10k'],
            color=COLORS[region], linewidth=2.5, marker='o', markersize=4, label=region)
ax.axvspan(2020, 2022, alpha=0.12, color='#fc5c65')
ax.text(2020.2, region_year['nurses_per_10k'].min() + 2, 'COVID',
        color='#fc5c65', fontsize=8.5, alpha=0.8)
ax.set_xlabel('Year', color=MUTED, fontsize=10)
ax.set_ylabel('Nurses per 10,000 population', color=MUTED, fontsize=10)
ax.set_title('Nurse Staffing Trends by European Region  (2000-2023)',
             color=TEXT, fontsize=11, fontweight='bold', pad=10)
ax.tick_params(colors=MUTED, labelsize=9)
ax.spines[['top','right']].set_visible(False)
ax.spines[['left','bottom']].set_color('#334466')
ax.legend(framealpha=0.15, labelcolor=TEXT, facecolor=PAGE_BG, edgecolor='none', fontsize=10)
ax.set_xlim(2000, 2023)

gs_bottom = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs[1], wspace=0.22)
for idx, (col, label, color) in enumerate(metrics):
    ax_b = fig.add_subplot(gs_bottom[idx])
    ax_b.set_facecolor(CARD_BG)
    bars = ax_b.bar(REGION_ORDER, region_avg[col],
                    color=[COLORS[r] for r in REGION_ORDER], edgecolor='none', width=0.55)
    for bar, val in zip(bars, region_avg[col]):
        ax_b.text(bar.get_x() + bar.get_width()/2,
                  bar.get_height() + region_avg[col].max()*0.02,
                  f'{val:.1f}', ha='center', va='bottom',
                  color=TEXT, fontsize=9.5, fontweight='bold')
    ax_b.set_title(label, color=TEXT, fontsize=10, fontweight='bold', pad=8)
    ax_b.tick_params(colors=MUTED, labelsize=9)
    ax_b.spines[['top','right','left','bottom']].set_visible(False)
    ax_b.yaxis.set_visible(False)
    for lt in ax_b.get_xticklabels():
        lt.set_color(MUTED)
        lt.set_fontsize(9)

plt.savefig(FIGURES + 'dashboard_2_trends_regions.png', bbox_inches='tight', facecolor=PAGE_BG, dpi=150)
plt.show()
print('Saved dashboard_2_trends_regions.png')
"""

d3_src = """fig = plt.figure(figsize=(20, 10))
fig.patch.set_facecolor(PAGE_BG)
fig.suptitle('Country Clusters & Regression Findings',
             color=TEXT, fontsize=15, fontweight='bold', y=0.99)

gs = gridspec.GridSpec(1, 2, figure=fig, wspace=0.28,
                       left=0.05, right=0.97, top=0.92, bottom=0.09)

ax_l = fig.add_subplot(gs[0])
ax_l.set_facecolor(CARD_BG)
for k in sorted(cluster_plot['cluster'].unique()):
    grp = cluster_plot[cluster_plot['cluster'] == k]
    ax_l.scatter(grp['nurses_per_10k'], grp['mortality_ami_30d'],
                 color=cluster_colors[k], s=140, zorder=3,
                 edgecolors='white', linewidths=0.5,
                 label=f'Cluster {k}: {cluster_labels[k]}')
    for _, row in grp.iterrows():
        ax_l.annotate(row['country'],
                      (row['nurses_per_10k'], row['mortality_ami_30d']),
                      textcoords='offset points', xytext=(6, 4),
                      fontsize=8, color=TEXT, alpha=0.9)
ax_l.set_xlabel('Nurses per 10,000 population', color=MUTED, fontsize=10)
ax_l.set_ylabel('30-day AMI Mortality (%)', color=MUTED, fontsize=10)
ax_l.set_title('Country Clusters: Staffing vs AMI Mortality',
               color=TEXT, fontsize=11, fontweight='bold', pad=10)
ax_l.tick_params(colors=MUTED, labelsize=9)
ax_l.spines[['top','right']].set_visible(False)
ax_l.spines[['left','bottom']].set_color('#334466')
ax_l.legend(framealpha=0.15, labelcolor=TEXT, facecolor=PAGE_BG,
            edgecolor='none', fontsize=8.5, loc='upper right')

ax_r = fig.add_subplot(gs[1])
ax_r.set_facecolor(CARD_BG)
reg_bar_colors = [ACC[1] if p < 0.05 else '#445566' for p in pvals]
ax_r.barh(y_pos, coefs, color=reg_bar_colors, height=0.45, zorder=3)
ci_range = max(ci_high) - min(ci_low)
for i, (lo, hi) in enumerate(zip(ci_low, ci_high)):
    ax_r.plot([lo, hi], [i, i], color='white', linewidth=2, zorder=4)
    ax_r.plot([lo, lo], [i-0.13, i+0.13], color='white', linewidth=2, zorder=4)
    ax_r.plot([hi, hi], [i-0.13, i+0.13], color='white', linewidth=2, zorder=4)
    ax_r.text(hi + ci_range*0.04, i,
              f'beta={coefs[i]:.4f}   p={pvals[i]:.3f}',
              va='center', color=MUTED, fontsize=10)
ax_r.axvline(0, color=MUTED, linewidth=1.2, linestyle='--', alpha=0.5)
ax_r.set_yticks(y_pos)
ax_r.set_yticklabels(outcomes, color=TEXT, fontsize=10)
ax_r.set_xlabel('Coefficient  (effect of nurses_per_10k)', color=MUTED, fontsize=9)
ax_r.set_title('Fixed Effects Panel Regression\\n(entity + time FE, clustered SE)',
               color=TEXT, fontsize=11, fontweight='bold', pad=10)
ax_r.tick_params(colors=MUTED, labelsize=9)
ax_r.spines[['top','right']].set_visible(False)
ax_r.spines[['left','bottom']].set_color('#334466')
sig_p   = mpatches.Patch(color=ACC[1],    label='p < 0.05')
insig_p = mpatches.Patch(color='#445566', label='p >= 0.05')
ax_r.legend(handles=[sig_p, insig_p], framealpha=0.15, labelcolor=TEXT,
            facecolor=PAGE_BG, edgecolor='none', fontsize=9)

plt.savefig(FIGURES + 'dashboard_3_clusters_regression.png', bbox_inches='tight', facecolor=PAGE_BG, dpi=150)
plt.show()
print('Saved dashboard_3_clusters_regression.png')
"""

d4_src = """fig = plt.figure(figsize=(22, 26))
fig.patch.set_facecolor(PAGE_BG)
fig.suptitle('Nurse Staffing & Patient Outcomes in Europe  |  2000-2023',
             color=TEXT, fontsize=17, fontweight='bold', y=0.995)

gs = gridspec.GridSpec(4, 3, figure=fig,
                       hspace=0.40, wspace=0.28,
                       top=0.97, bottom=0.04, left=0.06, right=0.97)

kpi_vals = [
    ('Avg Nurse Density',    f'{nurses:.0f}',   'per 10,000 pop', ACC[0]),
    ('Avg AMI Mortality',    f'{ami:.1f}%',      '30-day rate',    ACC[1]),
    ('Avg Stroke Mortality', f'{stroke:.1f}%',   '30-day rate',    ACC[2]),
    ('Avg Length of Stay',   f'{los:.1f} days',  'hospital stays', ACC[3]),
]
gs_kpi = gridspec.GridSpecFromSubplotSpec(1, 4, subplot_spec=gs[0, :], wspace=0.12)
for i, (title, value, subtitle, color) in enumerate(kpi_vals):
    ax = fig.add_subplot(gs_kpi[i])
    ax.set_facecolor(PAGE_BG)
    fancy = mpatches.FancyBboxPatch(
        (0.04, 0.06), 0.92, 0.88,
        boxstyle='round,pad=0.05', linewidth=2.5,
        edgecolor=color, facecolor=CARD_BG,
        transform=ax.transAxes, clip_on=False)
    ax.add_patch(fancy)
    ax.text(0.5, 0.76, title,    ha='center', va='center', transform=ax.transAxes,
            color=MUTED, fontsize=9.5, fontweight='bold')
    ax.text(0.5, 0.47, value,    ha='center', va='center', transform=ax.transAxes,
            color=TEXT, fontsize=23, fontweight='bold')
    ax.text(0.5, 0.16, subtitle, ha='center', va='center', transform=ax.transAxes,
            color=color, fontsize=8.5)
    ax.axis('off')

for idx, (col, label, color) in enumerate(metrics):
    ax_b = fig.add_subplot(gs[1, idx])
    ax_b.set_facecolor(CARD_BG)
    bars = ax_b.bar(REGION_ORDER, region_avg[col],
                    color=[COLORS[r] for r in REGION_ORDER], edgecolor='none', width=0.55)
    for bar, val in zip(bars, region_avg[col]):
        ax_b.text(bar.get_x() + bar.get_width()/2,
                  bar.get_height() + region_avg[col].max()*0.02,
                  f'{val:.1f}', ha='center', va='bottom',
                  color=TEXT, fontsize=8.5, fontweight='bold')
    ax_b.set_title(label, color=TEXT, fontsize=9, fontweight='bold', pad=8)
    ax_b.tick_params(colors=MUTED, labelsize=8)
    ax_b.spines[['top','right','left','bottom']].set_visible(False)
    ax_b.yaxis.set_visible(False)
    for lt in ax_b.get_xticklabels():
        lt.set_color(MUTED)

ax_trend = fig.add_subplot(gs[2, :2])
ax_trend.set_facecolor(CARD_BG)
for region in REGION_ORDER:
    grp = region_year[region_year['region'] == region]
    ax_trend.plot(grp['year'], grp['nurses_per_10k'],
                  color=COLORS[region], linewidth=2.2, marker='o', markersize=3.5, label=region)
ax_trend.axvspan(2020, 2022, alpha=0.1, color='#fc5c65')
ax_trend.set_title('Staffing Trends by Region  (2000-2023)', color=TEXT, fontsize=9, fontweight='bold', pad=8)
ax_trend.tick_params(colors=MUTED, labelsize=8)
ax_trend.spines[['top','right']].set_visible(False)
ax_trend.spines[['left','bottom']].set_color('#334466')
ax_trend.legend(framealpha=0.15, labelcolor=TEXT, facecolor=PAGE_BG, edgecolor='none', fontsize=8)
ax_trend.set_xlim(2000, 2023)

ax_reg = fig.add_subplot(gs[2, 2])
ax_reg.set_facecolor(CARD_BG)
reg_bar_colors = [ACC[1] if p < 0.05 else '#445566' for p in pvals]
ax_reg.barh(y_pos, coefs, color=reg_bar_colors, height=0.45, zorder=3)
for i, (lo, hi) in enumerate(zip(ci_low, ci_high)):
    ax_reg.plot([lo, hi], [i, i], color='white', linewidth=1.5, zorder=4)
    ax_reg.plot([lo, lo], [i-0.1, i+0.1], color='white', linewidth=1.5, zorder=4)
    ax_reg.plot([hi, hi], [i-0.1, i+0.1], color='white', linewidth=1.5, zorder=4)
ax_reg.axvline(0, color=MUTED, linewidth=1, linestyle='--', alpha=0.5)
ax_reg.set_yticks(y_pos)
ax_reg.set_yticklabels(outcomes, color=TEXT, fontsize=8)
ax_reg.set_title('Regression Coefficients\\n(nurse staffing -> outcomes)',
                 color=TEXT, fontsize=9, fontweight='bold', pad=8)
ax_reg.tick_params(colors=MUTED, labelsize=7)
ax_reg.spines[['top','right']].set_visible(False)
ax_reg.spines[['left','bottom']].set_color('#334466')

ax_clus = fig.add_subplot(gs[3, :])
ax_clus.set_facecolor(CARD_BG)
for k in sorted(cluster_plot['cluster'].unique()):
    grp = cluster_plot[cluster_plot['cluster'] == k]
    ax_clus.scatter(grp['nurses_per_10k'], grp['mortality_ami_30d'],
                    color=cluster_colors[k], s=120, zorder=3,
                    edgecolors='white', linewidths=0.5,
                    label=f'Cluster {k}: {cluster_labels[k]}')
    for _, row in grp.iterrows():
        ax_clus.annotate(row['country'],
                         (row['nurses_per_10k'], row['mortality_ami_30d']),
                         textcoords='offset points', xytext=(6, 3),
                         fontsize=8, color=TEXT, alpha=0.9)
ax_clus.set_xlabel('Nurses per 10,000 population', color=MUTED, fontsize=9)
ax_clus.set_ylabel('30-day AMI Mortality (%)', color=MUTED, fontsize=9)
ax_clus.set_title('Country Clusters: Staffing Profile vs AMI Mortality',
                  color=TEXT, fontsize=9, fontweight='bold', pad=8)
ax_clus.tick_params(colors=MUTED, labelsize=8)
ax_clus.spines[['top','right']].set_visible(False)
ax_clus.spines[['left','bottom']].set_color('#334466')
ax_clus.legend(framealpha=0.15, labelcolor=TEXT, facecolor=PAGE_BG,
               edgecolor='none', fontsize=8, loc='upper right')

plt.savefig(FIGURES + 'dashboard_4_full_overview.png', bbox_inches='tight', facecolor=PAGE_BG, dpi=150)
plt.show()
print('Saved dashboard_4_full_overview.png')
"""

def code_cell(src):
    return {'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': src}

def md_cell(src):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': src}

cells = [
    md_cell('# Phase 5 — Dashboards\n\nFour dashboards:\n1. **Interactive HTML** — KPI banner + clickable Europe choropleth map\n2. **Trends & Regions** — Staffing trends over time + regional bar comparison\n3. **Clusters & Regression** — Country cluster scatter + regression forest plot\n4. **Full Overview** — All panels combined'),
    code_cell(setup_src),
    md_cell('## Dashboard 1 — Interactive HTML: KPIs + Europe Map'),
    code_cell(d1_src),
    md_cell('## Dashboard 2 — Staffing Trends & Regional Comparison'),
    code_cell(d2_src),
    md_cell('## Dashboard 3 — Country Clusters & Regression Results'),
    code_cell(d3_src),
    md_cell('## Dashboard 4 — Full Overview (All Panels)'),
    code_cell(d4_src),
]

nb = {
    'cells': cells,
    'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3.11.0'}
    },
    'nbformat': 4,
    'nbformat_minor': 5
}

with open('05_dashboard.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print('05_dashboard.ipynb written successfully')
