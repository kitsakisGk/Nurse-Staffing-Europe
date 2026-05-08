# 🏥 nurse-staffing-europe

> **Nurse Staffing Ratios & Patient Outcomes in Europe: A Post-COVID Data-Driven Analysis**  
> *A health informatics research project combining panel regression, XGBoost/SHAP, and Power BI*

---

## 📌 Overview

This repository contains all code, data, and notebooks for a peer-reviewed research project investigating whether nurse staffing levels across European countries are statistically associated with measurable patient outcomes — and whether COVID-19 widened existing disparities between well-staffed and understaffed health systems.

**Research Question:**
> *"To what extent do nurse staffing levels predict patient outcomes across European countries, and has the COVID-19 pandemic widened existing disparities between high- and low-staffed health systems?"*

**Target publication:** JMIR Medical Informatics / BMC Health Services Research  
**Author:** Giorgos Kitsakis  
**Status:** 🟡 Phase 1 — Data Collection

---

## 🗂️ Repository Structure

```
nurse-staffing-europe/
│
├── data/
│   ├── raw/                    ← original downloads (do not modify)
│   │   ├── who_nurses.csv
│   │   ├── oecd_mortality.csv
│   │   ├── oecd_length_of_stay.csv
│   │   ├── eurostat_nurses.csv
│   │   ├── worldbank_beds.csv
│   │   └── worldbank_gdp.csv
│   ├── processed/
│   │   └── master_dataset.csv  ← merged, cleaned dataset (Phase 1 output)
│   └── outputs/
│       ├── regression_results.csv
│       └── cluster_assignments.csv
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_regression.ipynb
│   └── 04_ml_xgboost_shap.ipynb
│
├── powerbi/
│   └── nurse_staffing_europe.pbix
│
├── paper/
│   └── manuscript_draft.docx
│
├── figures/                    ← all exported charts for the paper
│
├── requirements.txt
└── README.md
```

---

## 📊 Data Sources

All data is publicly available and free. No ethics approval required (country-level aggregated data).

| # | Source | What We Use | Direct Link |
|---|--------|-------------|-------------|
| 1 | **WHO European Health Information Gateway** | Practising nurses per 10,000 population | https://gateway.euro.who.int/en/indicators/hlthres_189-practising-nurses-per-10-000-population/ |
| 2 | **OECD Health Statistics** | 30-day mortality (AMI + stroke), avg length of stay | https://stats.oecd.org/ |
| 3 | **Eurostat hlth_rs_prs2** | Practising nurses per 100,000 by EU country | https://ec.europa.eu/eurostat/databrowser/view/hlth_rs_prs2/default/table?lang=en |
| 4 | **World Bank SH.MED.BEDS.ZS** | Hospital beds per 1,000 people | https://data.worldbank.org/indicator/SH.MED.BEDS.ZS |
| 5 | **World Bank SH.XPD.CHEX.GD.ZS** | Health expenditure % GDP | https://data.worldbank.org/indicator/SH.XPD.CHEX.GD.ZS |
| 6 | **World Bank NY.GDP.PCAP.CD** | GDP per capita (USD) | https://data.worldbank.org/indicator/NY.GDP.PCAP.CD |

---

## 🔬 Variables

### Independent (Staffing)
| Variable | Source | Description |
|----------|--------|-------------|
| `nurses_per_10k` | WHO/Eurostat | Practising nurses per 10,000 population |
| `nurse_change_rate` | Engineered | YoY % change in nurse density |

### Dependent (Patient Outcomes)
| Variable | Source | Description |
|----------|--------|-------------|
| `mortality_ami_30d` | OECD | 30-day in-hospital mortality after AMI (%) |
| `mortality_stroke_30d` | OECD | 30-day mortality after ischaemic stroke (%) |
| `avg_length_of_stay` | OECD | Average length of stay — all causes (days) |

### Controls
| Variable | Source | Description |
|----------|--------|-------------|
| `gdp_per_capita` | World Bank | GDP per capita (current USD) |
| `health_exp_pct_gdp` | World Bank | Health expenditure (% of GDP) |
| `beds_per_1000` | World Bank | Hospital beds per 1,000 population |
| `physicians_per_1000` | World Bank/OECD | Physicians per 1,000 population |

### Metadata
| Variable | Description |
|----------|-------------|
| `country` | Country name (standardised) |
| `iso3` | ISO 3166-1 alpha-3 code |
| `year` | Year of observation |
| `region` | EU region (Northern / Southern / Eastern / Western) |
| `covid_period` | pre (≤2019) / during (2020–2021) / post (≥2022) |

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/kitsakisGk/Nurse-Staffing-Europe.git
cd nurse-staffing-europe

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch Jupyter
jupyter notebook
```

---

## 📓 Notebooks

| Notebook | Phase | Description |
|----------|-------|-------------|
| `01_data_collection.ipynb` | Phase 1 | Load, inspect, and document each raw dataset |
| `02_eda.ipynb` | Phase 2 | Correlation matrix, time series, regional comparisons |
| `03_regression.ipynb` | Phase 3 | Fixed-effects panel regression + results tables |
| `04_ml_xgboost_shap.ipynb` | Phase 4 | XGBoost, SHAP explainability, K-means clustering |

---

## 📈 Methodology

```
Raw Data (6 sources)
       ↓
  Data Merging & Cleaning  →  master_dataset.csv
       ↓
  EDA + Descriptive Stats
       ↓
  Panel Regression (Fixed-Effects)  →  effect sizes, significance
       ↓
  XGBoost + SHAP               →  feature importance, top drivers
       ↓
  K-Means Clustering           →  country archetypes (3-4 clusters)
       ↓
  Power BI Dashboard           →  maps, trends, COVID comparison
       ↓
  Paper (IMRAD structure)      →  JMIR Medical Informatics
```

---

## 🗓️ Project Timeline

| Phase | Description | Duration | Status |
|-------|-------------|----------|--------|
| 1 | Data Collection & Preparation | 2–3 weeks | 🟡 In Progress |
| 2 | Exploratory Data Analysis | 2 weeks | ⬜ Pending |
| 3 | Statistical Modeling | 2–3 weeks | ⬜ Pending |
| 4 | ML Modeling (XGBoost + SHAP) | 2–3 weeks | ⬜ Pending |
| 5 | Power BI Dashboard | 2 weeks | ⬜ Pending |
| 6 | Paper Writing & Submission | 4–6 weeks | ⬜ Pending |

---

## 📄 License

Data sources are all public / open access. Code is MIT licensed.
