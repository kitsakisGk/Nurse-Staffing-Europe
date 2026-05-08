# 🏥 nurse-staffing-europe
 
> **Nurse Staffing Ratios & Patient Outcomes in Europe: A Post-COVID Data-Driven Analysis**  
> *A health informatics research project combining panel regression, XGBoost/SHAP, and Power BI*
 
---
 
## 📌 Overview
 
This repository contains all code, data, and notebooks for a peer-reviewed research project investigating whether nurse staffing levels across European countries are statistically associated with measurable patient outcomes — and whether COVID-19 widened existing disparities between well-staffed and understaffed health systems.
 
**Research Question:**
> *"To what extent do nurse staffing levels predict patient outcomes across European countries, and has the COVID-19 pandemic widened existing disparities between high- and low-staffed health systems?"*
 
**Target publication:** JMIR Medical Informatics / BMC Health Services Research  
**Authors:** Giorgos (Data Lead) · Ioanna (Clinical Lead)  
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
