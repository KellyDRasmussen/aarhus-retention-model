# Aarhus Workforce Retention Model (2025-2030)

This project models how Aarhus Kommune can achieve its target of recruiting 1,500 additional international workers annually for the next 5 years through a focus on **family retention strategies**.

## 🎯 Executive Summary

Aarhus Kommune aims to add 1,500 new international workers each year through 2030. Our analysis shows that **spouse employment is a critical factor** in talent retention:

- Workers with employed partners are **61% likely to stay after 5 years** vs. only 49% for those whose partners don't work
- After just 3 years, the retention gap is already 12 percentage points (75% vs 63%)
- Effective spouse employment policies could reduce the annual recruitment need by up to 300-400 workers

## 🧠 Why This Matters

International recruitment is expensive and resource-intensive. Our data shows that focusing on spouse employment can create a **multiplier effect** that:

- Reduces turnover costs
- Improves ROI on integration programs
- Turns "trailing spouses" into taxpaying contributors
- Creates a more resilient international community

## 📊 Key Data Insights

### Retention Rate by Partner Status (%)

| Years in Aarhus | No Partner | Partner No Job | Partner With Job | Difference |
|-----------------|------------|----------------|------------------|------------|
| 1 year          | 70%        | 89%            | 91%              | +2%        |
| 2 years         | 55%        | 75%            | 80%              | +5%        |
| 3 years         | 50%        | 63%            | 75%              | +12%       |
| 4 years         | 47%        | 56%            | 66%              | +10%       |
| 5 years         | 41%        | 49%            | 61%              | +12%       |

### Recent International Worker Trends

- In 2025, Aarhus is projected to have 6,345 full-time international workers (1,631 non-EU, 4,714 EU)
- Foreign citizen population (20-64 years) has grown from 25,811 in 2021 to 32,479 in 2025
- Annual immigration of working-age foreign citizens averaged 4,947 over 2021-2024

## 🔍 Project Components

**Part 1 – Workforce Retention Model**  
Forecasts how Aarhus can reach its 1,500 worker target through two scenarios:
- **Baseline Scenario**: Current spouse employment rate (~40%)
- **Enhanced Spouse Employment Scenario**: Increased rate (~60%)

Our model demonstrates how the enhanced scenario can:
- Reduce annual recruitment needs by 20-25%
- Increase workforce stability
- Lower integration costs

**Part 2 – School Capacity Projection** *(Coming Next Week)*  
Will assess international school capacity needs based on workforce retention projections.

## 📁 Folder Structure

```
├── data/
│   ├── raw/                   # Original Statbank exports
│   └── processed/             # Cleaned data files
├── notebooks/
│   └── retention-model.ipynb  # Main forecasting logic
├── outputs/
│   ├── charts/                # Visualizations
│   └── forecast_tables/       # Scenario outputs
├── README.md                  # This file
└── requirements.txt
```

## 🚧 Status

**Work in progress.**  
- Part 1 (Workforce Retention Model) is under development
- Part 2 (School Capacity Projection) will begin next week
- Final outputs will include interactive dashboards and forecast tables

## 📜 License

Creative Commons Attribution-NonCommercial



# Aarhus Retention Forecasting Model (2025–2030)

This project models the capacity of Aarhus to retain international professionals through to 2030, and simulates the impact of dual-career families on workforce targets and international school enrolment.

It combines public datasets from Statistics Denmark with forecasting to estimate:
- How many international hires will still be in Aarhus in 2030
- How spouse employment influences retention
- When Aarhus International School (AIS) will reach capacity
- What policy scenarios lead to sustainable workforce growth

---

## 🧠 Why this matters

International recruitment is costly — in money, housing, integration, and time. Retaining existing talent is far more efficient. This model helps cities see that clearly by visualising:

- Workforce impact of recruiting 1 vs 2 working adults
- Retention improvements from supporting spouses
- Schooling bottlenecks under different growth scenarios

---

## 🔍 Project Components

**Part 1 – Workforce Retention Forecast**  
Forecasts of international workers arriving 2025–2029, with toggles for:
- % of workers who bring a spouse
- % of spouses who get jobs
- Scenario-based attrition rates by year
- How to reach the 1500 target

**Part 2 – School Capacity Projection**  
Estimates when Aarhus International School (AIS) will reach enrolment limits, based on:
- Student throughput by year
- % of new workers with school-age children
- School choice rates (AIS vs folkeskole vs other privates)

---

## 📁 Folder Structure

```
├── data/
│   ├── raw/                   # Original Statbank exports (not committed)
│   └── processed/             # Cleaned data for modeling
├── notebooks/
│   └── forecast-scenarios.ipynb  # Main logic & simulation
├── outputs/
│   ├── charts/                # Visualisations
│   └── forecast_tables/       # CSV outputs for Power BI or TE3
├── reports/
│   └── README.md              # This file
├── .gitignore
└── requirements.txt
```

---

## 🚧 Status

**Work in progress.**  
Data loading, forecasting logic, and scenario toggles are under development.  
Outputs will include interactive Power BI dashboards and published CSV tables.

---

## 📜 License

Creative Commons. 
