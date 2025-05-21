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
Forecasts retention of international workers arriving 2025–2029, with toggles for:
- EU vs non-EU recruitment shares
- % of workers who bring a spouse
- % of spouses who get jobs
- Scenario-based attrition rates by year

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
