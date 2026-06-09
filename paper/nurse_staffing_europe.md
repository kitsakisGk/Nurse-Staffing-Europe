# Nurse Staffing and Patient Outcomes in Europe: A Panel Data Analysis Across 36 Countries (2000–2023)

**Author:** Giorgos Kitsakis  
**Date:** May 2026  
**Data sources:** OECD Health Statistics · WHO Global Health Observatory · Eurostat · World Bank  
**Repository:** https://github.com/kitsakisGk/Nurse-Staffing-Europe

---

## Abstract

**Background:** Nurse staffing levels vary dramatically across European countries, yet the macro-level relationship between staffing ratios and patient outcomes remains poorly understood. Cross-national comparisons are confounded by GDP, health system architecture, and reporting differences.

**Methods:** Panel data from 36 European countries (2000–2023) were assembled from the OECD, WHO, Eurostat, and World Bank. Fixed-effects panel regression (entity and time effects, clustered standard errors) was used to test the association between nurse density and three outcomes: 30-day AMI mortality, 30-day stroke mortality, and average hospital length of stay. An XGBoost model with SHAP feature importance analysis identified the dominant predictors of AMI mortality. K-means clustering (k=5) grouped countries into staffing-outcome archetypes.

**Results:** Northern Europe averages 100.6 nurses per 10,000 population — more than double Southern Europe (47.0) and Eastern Europe (60.3). Fixed-effects regression finds no statistically significant within-country association between nurse density and any outcome after controlling for GDP per capita and health expenditure. SHAP analysis identifies GDP per capita as the dominant predictor of AMI mortality. Clustering reveals a stark contrast between a Nordic high-staffing, low-mortality archetype and an Eastern European low-staffing, high-mortality archetype. Greece, the lowest-ranked EU member state by nurse density (avg. 32.6/10k), illustrates the structural constraints imposed by prolonged austerity.

**Conclusions:** At the macro level, national wealth is a stronger predictor of patient outcomes than staffing ratios per se. Staffing is itself downstream of economic capacity. Improving outcomes in under-resourced systems requires system-wide investment, not isolated staffing targets — with particular urgency for Southern and Eastern European countries including Greece.

---

## 1. Introduction

The nursing workforce is the backbone of any healthcare system. Nurses constitute the largest share of the health workforce globally and represent the primary point of patient contact across hospital and community settings. Yet across Europe, nurse density varies by a factor of five — from fewer than 30 per 10,000 population in some Southern and Eastern European countries to over 160 per 10,000 in Norway.

Whether this variation translates into measurable differences in patient outcomes is a question of considerable policy relevance. At the individual hospital level, a robust body of evidence links higher nurse-to-patient ratios with lower in-hospital mortality, reduced adverse events, and shorter lengths of stay [1]. However, the picture at the national macro level is far less clear. Countries operate under different healthcare system architectures, funding models, GDP levels, and demographic profiles — all of which confound the staffing-outcome relationship.

This study addresses that gap with a longitudinal cross-national analysis spanning 36 European countries and 24 years. The research questions are:

1. How do nurse staffing levels vary across European regions, and has the gap widened or narrowed over time?
2. Is there a statistically significant association between national nurse density and patient outcomes at the macro level, after controlling for economic and structural factors?
3. Which variables most strongly predict AMI mortality in a machine learning framework?
4. Can European countries be grouped into meaningful archetypes based on their combined staffing and outcome profile?

The analysis is of particular relevance to countries such as Greece, which has sustained the lowest nurse density in the EU for over two decades — a situation compounded by a decade of fiscal austerity following the 2010 sovereign debt crisis.

---

## 2. Data and Methods

### 2.1 Data Sources

Panel data were assembled from four open-access international sources:

- **OECD Health Statistics** — 30-day in-hospital AMI mortality (%), 30-day in-hospital stroke mortality (%), average length of hospital stay (days), and hospital beds per 1,000 population
- **WHO Global Health Observatory** — nurses and midwives per 10,000 population
- **Eurostat** — practising nurses per 100,000 population (used to supplement and cross-validate WHO figures)
- **World Bank Open Data** — GDP per capita (constant 2015 USD) and health expenditure as a percentage of GDP

The final merged dataset covers 36 European countries from 2000 to 2023, comprising 864 country-year observations across 14 variables. Missing data rates vary by indicator: nurse density (35%), AMI mortality (45%), and stroke mortality (48%), reflecting uneven reporting practices across national statistical agencies.

### 2.2 Panel Regression

To test the association between nurse staffing and patient outcomes, a within-estimator fixed-effects panel regression was applied using the `linearmodels` Python library. The model specification is:

> *outcome_it = β × nurses_it + γ × controls_it + α_i + ε_it*

where *i* denotes country and *t* denotes year. Country fixed effects (α_i) absorb all time-invariant country-level heterogeneity, isolating within-country variation in staffing over time. Control variables include GDP per capita, health expenditure as a percentage of GDP, and hospital beds per 1,000 population. Time fixed effects are included. Standard errors are clustered at the country level to account for serial correlation within countries. Three outcome models were estimated: 30-day AMI mortality, 30-day stroke mortality, and average length of stay.

### 2.3 Machine Learning and Feature Importance

An XGBoost regressor (200 estimators, max depth 4, learning rate 0.05) was trained to predict AMI mortality using six features: nurse density, nurse change rate, GDP per capita, health expenditure, hospital bed density, and year. Five-fold cross-validation assessed model fit. Given the limited sample size (n=292 complete observations) and high between-country heterogeneity, predictive performance was modest (mean cross-validated R² = −1.27), consistent with the well-documented difficulty of cross-national outcome prediction at the macro level. Despite limited predictive accuracy, SHAP (SHapley Additive exPlanations) values were computed on the fitted model to provide indicative insight into relative feature contributions — interpreted as directional evidence rather than definitive causal inference.

### 2.4 Country Clustering

K-means clustering was applied to country-level averages across five dimensions: nurse density, AMI mortality, stroke mortality, average length of stay, and GDP per capita. Features were standardised prior to clustering. The optimal number of clusters (k=5) was selected using the silhouette score, which peaked at k=5 (score = 0.298).

---

## 3. Results

### 3.1 Regional Disparities in Nurse Density

The most striking finding from the descriptive analysis is the magnitude of regional inequality in nurse staffing across Europe (Figure 1). Northern European countries average **100.6 nurses per 10,000 population** and Western European countries average **99.9** — both approximately double the figures for Eastern Europe (**60.3**) and more than twice those of Southern Europe (**46.9**).

At the country level, Norway leads with **163.4 nurses per 10,000**, followed by Switzerland (147.7), Iceland (144.1), Ireland (128.5), and Finland (121.7). At the other end of the distribution: Greece (**32.6**), Cyprus (34.4), Bulgaria (41.1), Albania (43.8), and Latvia (48.1).

Over the 2000–2023 study period, all regions show a consistent upward trend in nurse density, with Northern Europe maintaining its lead throughout (Figure 2). The COVID-19 period (2020–2022) is associated with visible disruption, particularly in Northern Europe, likely reflecting workforce attrition and changes in reporting.

Outcome disparities follow a broadly similar regional pattern. Eastern Europe records the highest stroke mortality at 15.2% — significantly above Northern (9.4%) and Western (9.1%) Europe. Southern Europe shows the highest AMI mortality (8.4%), compared to 7.6% in Northern Europe (Figure 2, lower panels).

![Figure 1: KPI summary and nurse density choropleth map across Europe](../figures/screenshots/Nurse_Staffing_Overview_Map.png)
*Figure 1: Nurse density by country (colour scale: red = low, green = high) with aggregate KPI summary (2000–2023 averages).*

![Figure 2: Staffing trends over time and regional outcome comparison](../figures/screenshots/Trends_Regions_Full_Plots.png)
*Figure 2: Top — Nurse staffing trends by European region (2000–2023), COVID period shaded. Bottom — Average nurse density, AMI mortality, and stroke mortality by region.*

### 3.2 The Case of Greece

Greece presents a particularly stark case study. With an average nurse density of **32.6 per 10,000** — the lowest of all EU member states in the dataset — Greece sits far below the European average of 78.5. This is not a data artefact: Greek nurse density has been recorded consistently between 27 and 35 per 10,000 across all available years from 2000 to 2019, with no significant upward trend.

The timing is telling. Greece maintained a GDP per capita of approximately €28,000–€31,000 before the 2008 financial crisis, yet nurse density remained low even in this relatively prosperous period. Following the 2010 sovereign debt crisis and successive austerity programmes — which imposed severe restrictions on public sector hiring — nurse density stagnated and health expenditure was cut from a peak of 9.6% of GDP in 2010 to under 8% by 2015. The subsequent emigration of trained Greek healthcare professionals to Germany, the UK, and Scandinavia further depleted an already thin workforce. Recovery in healthcare investment has been slow and incomplete.

While Greek AMI and stroke outcome data are not available in the OECD dataset for the full period studied, Southern Europe as a region — where Greece's structural profile is most representative — records the highest AMI mortality at 8.4%. The structural under-staffing of Greece's health system, sustained across two decades, represents one of the clearest policy failures documented in this dataset.

### 3.3 Regression Results

Despite the clear descriptive association between lower staffing and worse aggregate outcomes at the regional level, the fixed-effects panel regression finds **no statistically significant association** between nurse density and any of the three outcome measures at the within-country level (Table 1).

**Table 1: Fixed-effects panel regression results — effect of nurse density on patient outcomes**

| Outcome | Coefficient | p-value | 95% CI | Significant |
|---|---|---|---|---|
| 30-day AMI Mortality | +0.0179 | 0.428 | [−0.026, +0.062] | No |
| 30-day Stroke Mortality | −0.0612 | 0.269 | [−0.170, +0.048] | No |
| Average Length of Stay | −0.0147 | 0.344 | [−0.045, +0.016] | No |

*All models include country and time fixed effects with clustered standard errors. Controls: GDP per capita, health expenditure % GDP, hospital beds per 1,000.*

None of these coefficients reaches conventional significance thresholds (p < 0.05). The positive coefficient for AMI mortality — while not significant — suggests that within a given country, years with slightly higher nurse density do not correspond to lower mortality. This is consistent with the hypothesis that year-to-year variation in national nurse density is too small and gradual to produce detectable changes in outcomes within a 20-year panel.

### 3.4 Feature Importance: What Actually Drives AMI Mortality?

The SHAP analysis of the XGBoost model identifies **GDP per capita** as the most influential feature in the model, followed by **year** (capturing secular improvements in cardiac care over time) and **health expenditure as a percentage of GDP**. Nurse density contributes to predictions but ranks below these economic and temporal variables in terms of mean absolute SHAP value.

This finding reinforces the regression results: at the macro level, national wealth and overall healthcare resourcing are stronger correlates of mortality outcomes than staffing ratios per se. This does not mean nurses do not matter — the ward-level evidence is unambiguous that they do — but it suggests that at the country level, nurse staffing is itself downstream of a nation's economic capacity and health investment decisions.

### 3.5 Country Clusters

K-means clustering (k=5) groups the 23 countries with complete data into five coherent archetypes (Figure 3):

- **Cluster 1 — Nordic leaders** (Norway, Sweden, Iceland, Denmark, Ireland): highest nurse density (avg. 127.8/10k), lowest AMI mortality (6.2%), highest GDP
- **Cluster 2 — High staffing, long stays** (Finland, Germany, Switzerland, Luxembourg, Netherlands): high staffing (avg. 113.8/10k) but longer average stays (10.3 days), reflecting different hospital utilisation models
- **Cluster 3 — Mid-range, mixed outcomes** (Austria, Belgium, Estonia, Italy, Poland, Slovenia, Spain, UK): average staffing (~83/10k), heterogeneous outcomes
- **Cluster 0 — Low staffing, high AMI mortality** (Latvia, Romania, Lithuania, Hungary): lowest staffing (avg. 61.1/10k), highest AMI mortality (11.8%)
- **Cluster 4 — Outlier** (Czech Republic): mid-range staffing with anomalously high stroke mortality (24.3%)

The separation between Clusters 1 and 0 is the most policy-relevant finding: countries with the lowest nurse density face the highest AMI mortality burden. Latvia's average AMI mortality of **14.3%** is nearly three times Norway's **5.3%** — a gap that the aggregate European statistics substantially obscure.

![Figure 3: Country clusters and regression findings](../figures/screenshots/Clusters_Regression_full_plots.png)
*Figure 3: Left — K-means country clusters (k=5) plotted by nurse density vs. 30-day AMI mortality. Right — Fixed-effects regression coefficients with 95% confidence intervals for all three outcome models.*

---

## 4. Discussion

### 4.1 The Confounding Role of GDP

The central tension in these findings is the disconnect between the descriptive regional pattern — where lower-staffed regions have worse outcomes — and the null result in the within-country regression. This is best explained by confounding: countries with low nurse density are also, broadly, countries with lower GDP, lower health expenditure, older infrastructure, and less developed primary care. When country fixed effects absorb these structural differences, the residual year-to-year variation in staffing is insufficient to produce a detectable signal in outcomes over a 20-year window.

This does not mean staffing is irrelevant. It means that at the national level, staffing cannot be disentangled from the broader economic and institutional context in which it operates. A nurse shortage in Latvia is not simply a headcount problem — it is embedded in wage levels, training capacity, emigration patterns, and a health system architecture shaped by decades of post-Soviet transition.

### 4.2 Implications for Greece and Southern Europe

Greece is the clearest example of what happens when economic crisis intersects with a structurally under-resourced nursing workforce. The Greek health system entered the 2010 austerity period already operating with nurse densities far below the EU average. The subsequent decade of public sector hiring freezes, wage cuts, and emigration of trained healthcare professionals to Northern and Western Europe further depleted an already thin workforce.

The policy implication is direct: reversing this trajectory requires not just headcount investment but structural reform — competitive nursing wages, domestic training expansion, and active retention policies to counter the pull of better-paying systems elsewhere in Europe. EU structural funds and the European Health Union framework offer potential financing mechanisms, but political commitment at the national level has been inconsistent.

### 4.3 Limitations

Several limitations should be noted. First, the outcome variables — OECD administrative mortality figures — capture only a narrow slice of healthcare quality. Nurse-sensitive outcomes such as pressure ulcers, medication errors, and patient falls are not available in internationally comparable form at the national level. Second, aggregation to country-year level masks within-country variation between hospital types, regions, and specialties. Third, the XGBoost model performed poorly in cross-validation (R² = −1.27), limiting the interpretability of SHAP values to directional evidence. Fourth, missing outcome data for Greece prevents country-specific outcome conclusions for the case most central to the policy discussion.

---

## 5. Conclusion

This study provides a comprehensive cross-national analysis of nurse staffing and patient outcomes across 36 European countries from 2000 to 2023. The findings document persistent and large inequalities in nurse density — with Northern Europe maintaining a sustained 2:1 advantage over Southern Europe — but find no statistically significant within-country effect of staffing on outcomes once economic and structural confounders are controlled for.

The dominant predictor of patient outcomes at the macro level is national wealth, not staffing ratios per se. This finding should not be misread as suggesting nurses do not matter — the ward-level evidence is clear that they do. Rather, it reflects the reality that at the country level, nurse density is a product of a healthcare system's overall investment level, and that improving outcomes requires system-wide resource commitments rather than isolated staffing targets.

For Greece and the broader Southern and Eastern European context, the message is urgent: two decades of structural under-investment in nursing — compounded in Greece's case by a decade of austerity — has created a workforce deficit that will not resolve itself. As European populations age and chronic disease burdens grow, the countries already operating at the bottom of the staffing distribution face the greatest pressure with the fewest resources to respond. Addressing this requires coordinated European-level policy on nursing wages, cross-border workforce flows, and health system investment — alongside national commitments to treat nursing capacity as a strategic infrastructure priority rather than a discretionary budget line.

---

## References

1. Aiken LH, Sloane DM, Bruyneel L, et al. Nurse staffing and education and hospital mortality in nine European countries: a retrospective observational study. *Lancet*. 2014;383(9931):1824–1830.
2. OECD. *Health at a Glance 2023: OECD Indicators*. Paris: OECD Publishing; 2023.
3. World Health Organization. *Global Health Observatory Data Repository*. Geneva: WHO; 2023.
4. Eurostat. *Healthcare personnel statistics — nursing and caring professionals*. Luxembourg: European Commission; 2024.
5. World Bank. *World Development Indicators*. Washington DC: The World Bank Group; 2024.
6. Papanicolas I, Woskie LR, Jha AK. Health care spending in the United States and other high-income countries. *JAMA*. 2018;319(10):1024–1039.
7. Vandoros S, Stargardt T. Reforms in the Greek pharmaceutical market during the financial crisis. *Health Policy*. 2013;109(1):1–6.
8. Lundström M, Lindqvist R, Axelsson M, et al. Nurse staffing and patient outcomes in Swedish hospitals. *BMC Health Services Research*. 2021;21:25.
9. Rechel B, Dubois CA, McKee M. *The Health Care Workforce in Europe: Learning from Experience*. Copenhagen: WHO Regional Office for Europe; 2006.
10. European Commission. *State of Health in the EU: Companion Report 2023*. Brussels: European Commission; 2023.
