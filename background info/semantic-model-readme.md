# Aarhus Workforce Forecast - Power BI Semantic Model

This document outlines the semantic data model for the Aarhus International Workforce Forecast (2026-2030) Power BI dashboard.

## Project Overview

This Power BI model analyzes and forecasts international workforce trends in Aarhus Kommune through 2030, based on historical data from 2021-2025. The model focuses on the municipality's target of recruiting 1,500 new international workers annually and identifies the associated migration needs.

## Semantic Model Structure

The data model uses a dimensional structure with star schema principles to enable flexible analysis and scenario modeling.

### Dimension Tables

#### DimDate
- **Purpose**: Provides time context for all measurements
- **Key Fields**:
  - `Year` (key) - The calendar year (2021-2030)
  - `IsHistorical` - Boolean flag (TRUE for 2021-2025, FALSE for 2026-2030)
  - `YearType` - Categorization ("Historical", "Forecast", "Target")
  - `DisplayText` - Formatted year label for visualizations

#### DimCategory
- **Purpose**: Categorizes metrics into logical groupings
- **Key Fields**:
  - `CategoryID` (key) - Unique identifier
  - `CategoryName` - Name (e.g., "Foreign Workers", "Migration", "Foreign Population")
  - `CategoryDescription` - Detailed description
  - `AnalysisType` - Broad classification for analysis purposes

#### DimMetric
- **Purpose**: Defines individual measurements tracked in the model
- **Key Fields**:
  - `MetricID` (key) - Unique identifier
  - `MetricName` - Technical name (e.g., "Full time EU workers")
  - `CategoryID` - Foreign key to DimCategory
  - `DisplayName` - User-friendly name for visualizations
  - `Description` - Detailed description including data source
  - `MetricType` - Classification (e.g., "Direct Workforce", "Migration")
  - `UnitOfMeasure` - Measurement unit (e.g., "People", "Percentage")

#### DimReliability
- **Purpose**: Defines forecast reliability classification levels
- **Key Fields**:
  - `ReliabilityID` (key) - Unique identifier
  - `ReliabilityLevel` - Classification (e.g., "High Reliability", "Moderate Reliability")
  - `ColorCode` - Hex color code for visualizations
  - `Description` - Explanation of the reliability level
  - `AssessmentCriteria` - How this level is determined

#### DimScenario
- **Purpose**: Defines different modeling scenarios
- **Key Fields**:
  - `ScenarioID` (key) - Unique identifier
  - `ScenarioName` - Name of the scenario
  - `WorkerToImmigrationRatio` - Conversion efficiency parameter
  - `WorkerToNetMigrationRatio` - Alternative efficiency parameter
  - `SpouseEmploymentRate` - Percentage of spouses employed
  - `IsDefault` - Boolean indicating the default scenario
  - `Description` - Detailed description of scenario parameters

### Fact Tables

#### FactMetricValues
- **Purpose**: Stores all metric values (historical and forecast)
- **Key Fields**:
  - `Year` - Foreign key to DimDate
  - `MetricID` - Foreign key to DimMetric
  - `Value` - The actual or forecasted value
  - `ValueType` - Classification ("Actual", "Forecast", "Lower Bound", "Upper Bound")
  - `UncertaintyValue` - Absolute uncertainty (± value)
  - `RSquared` - Statistical R² value for forecasts
  - `ReliabilityID` - Foreign key to DimReliability
  - `MAPE` - Mean Absolute Percentage Error
  - `CV` - Coefficient of Variation

#### FactTargetAnalysis
- **Purpose**: Stores target-related calculations and gap analysis
- **Key Fields**:
  - `Year` - Foreign key to DimDate
  - `WorkforceTarget` - Annual worker target (typically 1,500)
  - `ProjectedGrowth` - Forecasted growth under current trends
  - `Gap` - Difference between target and projected growth
  - `RequiredRecruitment` - Number of workers needed to be recruited
  - `RequiredMigration` - Total migration needed to achieve target
  - `ScenarioID` - Foreign key to DimScenario

### Parameter Tables

#### ParamSystemSettings
- **Purpose**: Stores global settings and parameters
- **Key Fields**:
  - `SettingName` (key) - Name of the setting
  - `SettingValue` - Value of the setting
  - `Description` - Explanation of the setting's purpose
  - `Category` - Classification of the setting

### Metadata Table

#### MetaDataInfo
- **Purpose**: Documents model metadata
- **Key Fields**:
  - `DataVersion` (key) - Version identifier
  - `LastUpdated` - Timestamp of last update
  - `DataSource` - Description of data sources
  - `Notes` - General notes about the model
  - `Assumptions` - Key assumptions made in the analysis
  - `AnalysisScope` - Scope definition
  - `Author` - Model creator

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