# Nurse Staffing & Patient Outcomes in Europe

> A cross-national panel data study across 36 European countries (2000–2023)

**Author:** Giorgos Kitsakis  
**Data sources:** OECD · WHO · Eurostat · World Bank  
**Status:** Complete

---

## Overview

This repository contains the full research pipeline for a study investigating whether nurse staffing levels across European countries are statistically associated with patient outcomes — and what structural factors drive the large disparities between well-staffed and under-staffed health systems.

**Research question:**
> *To what extent do nurse staffing levels predict patient outcomes across European countries, and what structural factors explain the persistent gap between Northern and Southern/Eastern Europe?*

**Key findings:**
- Northern Europe averages 100+ nurses per 10,000 population — more than double Southern Europe (47) and Eastern Europe (60)
- Greece has the lowest nurse density in the EU (avg. 32.6/10k), structurally constrained by a decade of austerity
- Fixed-effects panel regression finds no statistically significant within-country effect of staffing on outcomes once GDP and health expenditure are controlled for
- GDP per capita is the dominant predictor of AMI mortality in the XGBoost/SHAP analysis
- K-means clustering identifies 5 country archetypes — Nordic leaders (lowest mortality) vs. Eastern European cluster (highest AMI mortality, lowest staffing)

---

## Repository Structure

```
nurse-staffing-europe/
│
├── data/
│   ├── raw/                        ← original downloads (gitignored)
│   ├── processed/
│   │   └── master_dataset.csv      ← 864 rows, 36 countries, 14 variables
│   └── outputs/
│       ├── regression_results.csv
│       └── cluster_assignments.csv
│
├── notebooks/
│   ├── 01_data_collection.ipynb    ← WHO, OECD, Eurostat, World Bank merge
│   ├── 02_eda.ipynb                ← EDA, regional stats, COVID comparison
│   ├── 03_regression.ipynb         ← Fixed-effects panel regression
│   ├── 04_ml_xgboost_shap.ipynb    ← XGBoost, SHAP, K-means clustering
│   ├── 05_dashboard.ipynb          ← Publication-ready static figures
│   └── build_html_dashboard.py     ← Interactive HTML dashboard builder
│
├── figures/                        ← All exported charts + interactive dashboard
│   └── dashboard.html              ← 4-tab interactive Plotly dashboard
│
├── powerbi/
│   └── Nurse_Staffing_Europe.pbix  ← Power BI dashboard
│
├── paper/
│   └── nurse_staffing_europe.md    ← Full research paper (2,500 words)
│
├── requirements.txt
└── README.md
```

---

## Data Sources

All data is publicly available. No ethics approval required (country-level aggregated data).

| Source | Variables |
|--------|-----------|
| WHO Global Health Observatory | Nurses per 10,000 population |
| OECD Health Statistics | 30-day AMI mortality, stroke mortality, avg length of stay |
| Eurostat hlth_rs_prs2 | Practising nurses per 100,000 (EU countries) |
| World Bank | GDP per capita, health expenditure % GDP, hospital beds per 1,000 |

---

## Methodology

```
6 raw data sources (WHO / OECD / Eurostat / World Bank)
        ↓
  Data merging & cleaning  →  master_dataset.csv (864 rows, 36 countries)
        ↓
  Exploratory data analysis  →  regional comparisons, trends, COVID impact
        ↓
  Fixed-effects panel regression  →  AMI mortality, stroke mortality, LOS
        ↓
  XGBoost + SHAP  →  feature importance, non-linear effects
        ↓
  K-means clustering (k=5)  →  country archetypes
        ↓
  Interactive dashboard  →  dashboard.html (Plotly, 4 tabs)
        ↓
  Research paper  →  nurse_staffing_europe.md
```

---

## Setup

```bash
git clone https://github.com/kitsakisGk/Nurse-Staffing-Europe.git
cd Nurse-Staffing-Europe
pip install -r requirements.txt
jupyter notebook
```

To rebuild the interactive dashboard:
```bash
py notebooks/build_html_dashboard.py
# opens figures/dashboard.html in your browser
```

---

## Notebooks

| Notebook | Description |
|----------|-------------|
| `01_data_collection.ipynb` | Load and merge 6 raw datasets into master_dataset.csv |
| `02_eda.ipynb` | Correlation matrix, time series, regional bar charts, COVID comparison |
| `03_regression.ipynb` | PanelOLS fixed-effects models with clustered standard errors |
| `04_ml_xgboost_shap.ipynb` | XGBoost regression, SHAP feature importance, K-means clustering |
| `05_dashboard.ipynb` | Publication-ready static figures (PNG exports) |
| `build_html_dashboard.py` | Generates self-contained interactive HTML dashboard |

---

## License

Data sources are all public / open access. Code is MIT licensed.
