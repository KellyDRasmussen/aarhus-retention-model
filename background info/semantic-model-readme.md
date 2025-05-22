# Aarhus Workforce Forecast - Power BI Semantic Model

This document outlines the semantic data model for the Aarhus International Workforce Forecast (2026-2030) Power BI dashboard.

## Project Overview

This Power BI model analyzes and forecasts international workforce trends in Aarhus Kommune through 2030, based on historical data from 2021-2025. The model focuses on the municipality's target of recruiting 1,500 new international workers annually and identifies the associated migration needs.

## Semantic Model Structure

The data model uses a dimensional structure with star schema principles to enable flexible analysis and scenario modeling.

### Dimension Tables



### Fact Tables



## Key Calculated Measures

The model includes the following core calculated measures:

| Measure Name | Description | DAX Formula (simplified) |
|--------------|-------------|--------------------------|
| Projected Annual Worker Growth | Sum of forecasted worker growth | `SUM(FactMetricValues[Value])` where MetricName = "Total workers" and ValueType = "Forecast" |
| Gap to Target | Difference between target and projected growth | `[WorkforceTarget] - [Projected Annual Worker Growth]` |
| Required Migration | Migration needed to achieve target | `([Target] + [Emigration]) / [WorkerToImmigrationRatio]` |
| Efficiency Rate | Ratio of worker growth to immigration | `DIVIDE([Worker Growth], [Immigration])` |
| Retention Rate | Percentage of foreign population not emigrating | `1 - DIVIDE([Emigration], [Foreign Population])` |

## Data Relationships

![Data Model Diagram](model_diagram.png)

The model uses the following key relationships:
- `FactMetricValues` connects to `DimDate`, `DimMetric`, and `DimReliability`
- `FactTargetAnalysis` connects to `DimDate` and `DimScenario`
- `DimMetric` connects to `DimCategory`

## Usage Guidelines

### Best Practices
1. Always filter by scenario when doing target analysis
2. Use reliability classifications to assess forecast confidence
3. When comparing historical vs. forecast data, use the ValueType field

### Known Limitations
1. The model assumes constant conversion efficiency over time without policy changes
2. Uncertainty grows with forecast horizon and should be considered when making decisions
3. Historical patterns may not continue if significant policy or demographic changes occur

## Maintenance

### Adding New Data
1. Historical data: Add new records to the historical source files
2. Forecasts: Re-run the forecast model with updated historical data
3. Update the `LastUpdated` field in the `MetaDataInfo` table

### Adding New Scenarios
1. Add a new record to the `DimScenario` table
2. Run the forecast model with the new parameters
3. Add the results to `FactTargetAnalysis` with the appropriate ScenarioID

---

*Last Updated: May 22, 2025*