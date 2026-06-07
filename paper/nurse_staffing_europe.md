# Nurse Staffing and Patient Outcomes in Europe: A Panel Data Analysis Across 36 Countries (2000–2023)

**Author:** Giorgos Kitsakis  
**Date:** May 2026  
**Data sources:** OECD Health Statistics, WHO Global Health Observatory, Eurostat, World Bank

---

## Abstract

Nurse staffing levels vary dramatically across European countries, yet the relationship between staffing ratios and patient outcomes remains poorly understood at the macro level. This study analyses panel data from 36 European countries over the period 2000–2023, combining nurse density figures from the OECD, WHO, and Eurostat with patient outcome indicators including 30-day AMI mortality, 30-day stroke mortality, and average hospital length of stay. Fixed-effects panel regression, XGBoost machine learning, SHAP feature importance analysis, and K-means clustering are employed to examine this relationship from multiple analytical angles. Results reveal stark regional disparities — Northern European countries maintain nurse densities more than double those of Southern and Eastern counterparts — yet fixed-effects regression finds no statistically significant association between staffing and outcomes after controlling for GDP per capita, health expenditure, and hospital bed density. GDP per capita emerges as the dominant driver of outcome variation in the ML analysis. Greece, the lowest-ranked EU member state by nurse density, illustrates the structural constraints that economic crises impose on healthcare workforces. The findings suggest that staffing ratios alone are insufficient without accompanying investment in system-wide healthcare infrastructure.

---

## 1. Introduction

The nursing workforce is the backbone of any healthcare system. Nurses constitute the largest share of the health workforce globally and are the primary point of contact for most patients across hospital and community settings. Yet across Europe, the density of nurses per population varies by a factor of five — from fewer than 30 per 10,000 in some Southern and Eastern European countries to over 160 per 10,000 in Norway.

Whether this variation translates into measurable differences in patient outcomes is a question of considerable policy relevance. At the individual hospital level, a robust body of evidence links higher nurse-to-patient ratios with lower in-hospital mortality, reduced adverse events, and shorter lengths of stay. However, the picture at the national macro level is far less clear. Countries operate under different healthcare system architectures, funding models, GDP levels, and demographic profiles — all of which confound the staffing-outcome relationship.

This study addresses that gap with a longitudinal cross-national analysis spanning 36 European countries and 24 years. The research questions are:

1. How do nurse staffing levels vary across European regions, and has the gap widened or narrowed over time?
2. Is there a statistically significant association between national nurse density and patient outcomes at the macro level, controlling for economic and structural factors?
3. Which variables most strongly predict AMI mortality in a machine learning framework?
4. Can European countries be grouped into meaningful archetypes based on their staffing and outcomes profile?

The analysis is of particular relevance to countries such as Greece, which has sustained the lowest nurse density in the EU for over two decades — a situation worsened by a decade of austerity and structural adjustment following the 2010 sovereign debt crisis.

---

## 2. Data and Methods

### 2.1 Data Sources

Panel data were assembled from four open-access international sources:

- **OECD Health Statistics** — 30-day in-hospital AMI mortality (%), 30-day in-hospital stroke mortality (%), average length of hospital stay (days), and hospital beds per 1,000 population
- **WHO Global Health Observatory** — nurses and midwives per 10,000 population
- **Eurostat** — practising nurses per 100,000 population (used to supplement and cross-validate WHO figures)
- **World Bank Open Data** — GDP per capita (constant 2015 USD) and health expenditure as a percentage of GDP

The final merged dataset covers 36 European countries from 2000 to 2023, comprising 864 country-year observations across 14 variables. Missing data rates vary by indicator: nurse density (35%), AMI mortality (45%), and stroke mortality (48%), reflecting the uneven reporting practices of different national statistical agencies.

### 2.2 Panel Regression

To test the association between nurse staffing and patient outcomes, within-estimator fixed-effects panel regression was applied using the `linearmodels` library in Python. The model specification is:

> *outcome_it = β × nurses_it + γ × controls_it + α_i + ε_it*

where *i* denotes country and *t* denotes year. Country fixed effects (α_i) absorb all time-invariant country-level heterogeneity, isolating the within-country variation in staffing. Control variables include GDP per capita, health expenditure as a percentage of GDP, and hospital beds per 1,000 population. Time fixed effects are also included. Standard errors are clustered at the country level to account for serial correlation within countries.

Three outcome models were estimated: 30-day AMI mortality, 30-day stroke mortality, and average length of stay.

### 2.3 Machine Learning and Feature Importance

An XGBoost regressor was trained to predict AMI mortality using six features: nurse density, nurse change rate, GDP per capita, health expenditure, hospital bed density, and year. Five-fold cross-validation was used to assess model performance. SHAP (SHapley Additive exPlanations) values were computed to rank feature contributions to each prediction, providing interpretable insight into which variables drive the model most.

### 2.4 Country Clustering

K-means clustering was applied to country-level averages across five dimensions: nurse density, AMI mortality, stroke mortality, average length of stay, and GDP per capita. The optimal number of clusters (k=5) was selected using the silhouette score. All features were standardised prior to clustering.

---

## 3. Results

### 3.1 Regional Disparities in Nurse Density

The most striking finding from the descriptive analysis is the magnitude of regional inequality in nurse staffing across Europe. Northern European countries average **100.6 nurses per 10,000 population**, and Western European countries average **99.9** — both approximately double the figures for Eastern Europe (**60.3**) and more than twice those of Southern Europe (**46.9**).

At the country level, Norway leads with **163.4 nurses per 10,000**, followed by Switzerland (147.7), Iceland (144.1), Ireland (128.5), and Finland (121.7). At the other end of the distribution sit Greece (**32.6**), Cyprus (34.4), Bulgaria (41.1), Albania (43.8), and Latvia (48.1).

Over the 2000–2023 period, the data reveal a consistent upward trend in nurse density across all regions, with Northern Europe maintaining its lead throughout. The COVID-19 period (2020–2022) coincides with a visible disruption in the trend, particularly in Northern Europe, likely reflecting both workforce attrition and changes in reporting.

### 3.2 The Case of Greece

Greece presents a particularly stark case study. With an average nurse density of just **32.6 per 10,000** — the lowest of all 28 EU member states in the dataset — Greece sits far below the EU average of 78.5. This is not a data artefact: Greek nurse density has been recorded consistently between 27 and 35 per 10,000 across all available years from 2000 to 2019, with no significant upward trend.

The timing is telling. Greece maintained a GDP per capita of approximately €28,000–€31,000 before the 2008 financial crisis, yet nurse density remained low even in this relatively prosperous period. Following the 2010 sovereign debt crisis and the implementation of successive austerity programmes — which imposed severe restrictions on public sector hiring — nurse density stagnated and health expenditure was cut from a peak of 9.6% of GDP in 2010 to under 8% by 2015. Recovery in healthcare investment has been slow.

This matters for patient outcomes. While Greek AMI and stroke mortality data are not available in the OECD dataset for the period studied, Southern Europe as a region has the highest AMI mortality rate at **8.4%** — compared to 7.6% in Northern Europe and 7.3% in Eastern Europe. Italy and Spain, the best-represented Southern European countries in the outcomes data, show AMI mortality rates of 6.0% and 8.9% respectively. Greece's structural under-staffing, in the context of a healthcare system under prolonged fiscal pressure, raises serious concerns that are not yet fully captured in cross-national outcome data.

### 3.3 Regression Results

Despite the clear descriptive association between low staffing and Southern/Eastern Europe's worse aggregate outcomes, the fixed-effects panel regression finds **no statistically significant association** between nurse density and any of the three outcome measures at the within-country level:

| Outcome | Coefficient | p-value | 95% CI |
|---|---|---|---|
| AMI Mortality | +0.0179 | 0.428 | [−0.026, +0.062] |
| Stroke Mortality | −0.0612 | 0.269 | [−0.170, +0.048] |
| Length of Stay | −0.0147 | 0.344 | [−0.045, +0.016] |

None of these coefficients reaches conventional significance thresholds (p < 0.05). The positive coefficient for AMI mortality — while not significant — is counterintuitive and warrants discussion (see Section 4).

These results are consistent with several macro-level studies that find confounding by wealth and health system organisation obscures the staffing-outcome relationship at the national level. When country fixed effects absorb structural differences, the year-to-year variation in nurse staffing within a country does not appear to generate detectable changes in outcomes within the time horizon studied.

### 3.4 Feature Importance: What Actually Drives AMI Mortality?

The XGBoost model's SHAP analysis reveals that **GDP per capita** is the single most important predictor of 30-day AMI mortality across the dataset, followed by **year** (capturing the secular trend of improving outcomes over time), and **health expenditure as a percentage of GDP**. Nurse density ranks lower in feature importance than economic and structural variables.

This finding reinforces the regression results: at the macro level, national wealth and the overall resourcing of the healthcare system are stronger predictors of mortality outcomes than staffing ratios per se. This does not mean nurses do not matter — the ward-level evidence is unambiguous that they do — but it suggests that at the country level, nurse staffing is itself a downstream consequence of a country's economic capacity and health system investment decisions.

### 3.5 Country Clusters

K-means clustering (k=5) groups the 23 countries with complete data into five coherent archetypes:

- **Cluster 1 — Nordic leaders** (Norway, Sweden, Iceland, Denmark, Ireland): highest nurse density (avg. 127.8/10k), lowest AMI mortality (6.2%), high GDP
- **Cluster 2 — High staffing, long stays** (Finland, Germany, Switzerland, Luxembourg, Netherlands): high staffing (avg. 113.8/10k) but longer average stays (10.3 days), reflecting different hospital utilisation models
- **Cluster 3 — Mid-range, mixed outcomes** (Austria, Belgium, Estonia, Italy, Poland, Slovenia, Spain, UK): average staffing (~83/10k), average outcomes — the most heterogeneous group
- **Cluster 0 — Low staffing, high AMI mortality** (Latvia, Romania, Lithuania, Hungary): lowest staffing in the cluster analysis (avg. 61.1/10k), highest AMI mortality (11.8%)
- **Cluster 4 — Outlier** (Czech Republic): mid-range staffing but anomalously high stroke mortality (24.3%)

The separation between Clusters 1 and 0 is the most policy-relevant finding: countries with the lowest nurse density also face the highest AMI mortality burden. Latvia's average AMI mortality of 14.3% — nearly three times Norway's 5.3% — illustrates what the aggregate statistics obscure.

---

## 4. Discussion

### 4.1 The Confounding Role of GDP

The central tension in these findings is the disconnect between the descriptive regional pattern — where lower-staffed regions have worse outcomes — and the null result in the within-country fixed-effects regression. This is best explained by confounding: the countries with low nurse density are also, broadly, the countries with lower GDP, lower health expenditure, older infrastructure, and less developed primary care systems. When country fixed effects control for all of this, the residual year-to-year variation in staffing is too small and too noisy to produce a detectable signal in outcomes over a 20-year window.

This does not mean staffing is irrelevant. It means that staffing cannot be disentangled from the broader economic and institutional context in which it operates. A nurse shortage in Latvia is not simply a headcount problem — it is embedded in wage levels, training capacity, emigration patterns, and a health system architecture shaped by decades of post-Soviet transition.

### 4.2 Implications for Greece and Southern Europe

Greece is the clearest example of what happens when economic crisis intersects with a structurally under-resourced nursing workforce. The Greek health system entered the 2010 austerity period already operating with nurse densities far below the EU average. The subsequent decade of public sector hiring freezes, wage cuts, and emigration of trained healthcare professionals to Germany, the UK, and Scandinavia further depleted an already thin workforce.

The policy implication is straightforward: reversing this trajectory requires not just headcount investment but structural reform — competitive nursing wages, domestic training expansion, and active retention policies to counter the pull of better-paying systems in Northern and Western Europe. EU structural funds and the European Health Union framework offer potential financing mechanisms, but political will at the national level has been inconsistent.

### 4.3 Limitations

Several limitations should be noted. First, the outcome variables used — OECD administrative mortality figures — measure only a narrow slice of healthcare quality. Nurse-sensitive outcomes such as pressure ulcers, medication errors, and patient falls are not captured at the national level in internationally comparable form. Second, the aggregation to country-year level masks enormous within-country variation between hospital types, regions, and specialties. Third, missing data — particularly for Greece's outcome indicators — limits the ability to draw country-specific conclusions for the cases most relevant to the policy discussion.

---

## 5. Conclusion

This study provides a comprehensive cross-national analysis of nurse staffing and patient outcomes across 36 European countries from 2000 to 2023. The findings document persistent and large inequalities in nurse density — with Northern Europe maintaining a 2:1 advantage over Southern Europe throughout the study period — but find no statistically significant within-country effect of staffing on outcomes once economic and structural confounders are controlled for.

The dominant predictor of patient outcomes at the macro level is national wealth, not staffing ratios per se. This finding should not be misread as suggesting that nurses do not matter — the ward-level evidence is clear that they do. Rather, it reflects the reality that at the country level, nurse density is itself a product of a healthcare system's overall investment level, and that improving outcomes requires system-wide resource commitments rather than isolated staffing targets.

For Greece and the broader Southern and Eastern European context, the message is urgent: two decades of structural under-investment in nursing — compounded in Greece's case by a decade of austerity — has created a workforce deficit that will not resolve itself. As European populations age and chronic disease burdens grow, the countries already operating at the bottom of the staffing distribution face the greatest pressure with the fewest resources to respond.

Addressing this requires coordinated European-level policy — on nursing wages, cross-border workforce flows, and health system investment — alongside national commitments to treat nursing capacity as a strategic infrastructure priority rather than a discretionary budget line.

---

## References

1. Aiken, L.H. et al. (2014). Nurse staffing and education and hospital mortality in nine European countries. *The Lancet*, 383(9931), 1824–1830.
2. OECD (2023). *Health at a Glance 2023: OECD Indicators*. OECD Publishing, Paris.
3. WHO (2023). *Global Health Observatory Data Repository*. World Health Organization.
4. Eurostat (2024). *Healthcare personnel statistics — nursing and caring professionals*. European Commission.
5. World Bank (2024). *World Development Indicators*. The World Bank Group.
6. Papanicolas, I., Woskie, L.R. & Jha, A.K. (2018). Health care spending in the United States and other high-income countries. *JAMA*, 319(10), 1024–1039.
7. Vandoros, S. & Stargardt, T. (2013). Reforms in the Greek pharmaceutical market during the financial crisis. *Health Policy*, 109(1), 1–6.
8. Lundström, M. et al. (2021). Nursing staff-to-patient ratios and patient outcomes. *BMC Health Services Research*, 21, 1:25.
