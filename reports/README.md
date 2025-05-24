# Aarhus Workforce Forecast - Power BI Semantic Model

This document outlines the semantic data model for the Aarhus International Workforce Forecast (2026-2030) Power BI dashboard and was machine generated after feeding a LLM (Claude Sonnet 4) with project data.

## Project Overview

This Power BI model analyzes and forecasts international workforce trends in Aarhus Kommune through 2030, based on historical data from 2021-2025. The model focuses on the municipality's target of recruiting 7,500 additional international workers by 2030 (1,500 per year) and demonstrates how spouse employment scenarios can significantly reduce recruitment needs.

### Key Analysis Components
1. **Baseline Forecasting** - Projects current trends in international workers and migration
2. **Spouse Employment Scenarios** - Models the impact of partner employment rates on retention and workforce growth
3. **Recruitment Gap Analysis** - Calculates how many new households need to be recruited under different scenarios
4. **Untapped Workforce Potential** - Identifies existing partners who could contribute to workforce goals

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
- **Purpose**: Defines spouse employment scenarios and their parameters
- **Key Fields**:
  - `ScenarioID` (key) - Unique identifier
  - `ScenarioName` - Name of the scenario (e.g., "30% of partners work fulltime")
  - `PartnerEmploymentRate` - Percentage of accompanying partners employed (10%, 20%, 30%, 40%, 50%, 60%, 70%)
  - `RetentionRateWithEmployedPartner` - 61% (from Copenhagen data)
  - `RetentionRateWithUnemployedPartner` - 49% (from Copenhagen data)
  - `SingleWorkerRetentionRate` - Default retention rate for workers without partners
  - `IsDefault` - Boolean indicating the default scenario (30%)
  - `Description` - Detailed description of scenario assumptions

#### DimWorkerType
- **Purpose**: Categorizes international workers by household composition
- **Key Fields**:
  - `WorkerTypeID` (key) - Unique identifier
  - `WorkerTypeName` - Type ("Single worker", "Worker with accompanying partner", "Worker with Danish partner")
  - `HasPartner` - Boolean indicating if worker has a partner
  - `PartnerIsDanish` - Boolean indicating if partner is Danish
  - `BaseRetentionRate` - Base retention rate for this worker type
  - `ColorCode` - Color for visualizations

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

#### FactSpouseEmploymentAnalysis
- **Purpose**: Stores spouse employment scenario calculations
- **Key Fields**:
  - `Year` - Foreign key to DimDate
  - `ScenarioID` - Foreign key to DimScenario
  - `WorkerTypeID` - Foreign key to DimWorkerType
  - `EstimatedWorkers` - Number of workers of this type
  - `EstimatedPartners` - Number of accompanying partners
  - `EmployedPartners` - Number of partners employed (based on scenario rate)
  - `UnemployedPartners` - Number of partners not employed
  - `RetainedWorkers` - Workers retained based on partner employment status
  - `RetainedPartners` - Partners who become workers
  - `TotalContributingWorkers` - Sum of retained workers and working partners

#### FactRecruitmentGap
- **Purpose**: Calculates recruitment needs under different scenarios
- **Key Fields**:
  - `Year` - Foreign key to DimDate
  - `ScenarioID` - Foreign key to DimScenario
  - `AnnualTarget` - Target new workers per year (1,500)
  - `CumulativeTarget` - Cumulative target by this year
  - `BaselineForecast` - Workers expected under current trends
  - `SpouseEmploymentContribution` - Additional workers from spouse employment
  - `TotalProjectedWorkers` - Total workers including spouse employment effect
  - `AnnualGap` - Gap between target and projected workers
  - `CumulativeGap` - Cumulative gap by this year
  - `NewHouseholdsNeeded` - Number of new households to recruit annually
  - `UntappedWorkforce` - Existing partners who could work but don't

#### FactBaselineProjections
- **Purpose**: Stores baseline forecasts without spouse employment scenarios
- **Key Fields**:
  - `Year` - Foreign key to DimDate
  - `MetricID` - Foreign key to DimMetric
  - `ForecastValue` - Projected value under current trends
  - `UncertaintyValue` - Forecast uncertainty (± value)
  - `UncertaintyPct` - Uncertainty as percentage
  - `RSquared` - Statistical R² value
  - `ReliabilityID` - Foreign key to DimReliability

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

The model includes the following core calculated measures organized by display folder:

### Simple Metrics
| Measure Name | Description | Key Logic |
|--------------|-------------|-----------|
| Net Migration | Immigration minus emigration | `SUM(Immigration) - SUM(Emigration)` |
| Total with Work Permits | Sum of EU and 3rd country work permits | `SUM(Work permit 3rd country) + SUM(Work permit EU)` |
| Total with Work Permits (2025) | Baseline for 2025 calculations | Filtered to year 2025 |
| Total Full Time Foreign Workforce | All workers regardless of permit type | Includes work permits, family reunification, permanent residency, etc. |

### Measures from Constants (Research-Based)
| Measure Name | Description | Source |
|--------------|-------------|--------|
| Current percentage with a partner | Percentage of workers with partners | Research constants table |
| Current percentage with an accompanying partner | Partners who moved to Denmark | Research constants × accompanying rate |
| Current percentage with a Danish partner | Partners who are Danish citizens | Research constants × Danish rate |
| Current Percentage With working Accompanying Partner | Partners currently employed | Based on Copenhagen employment rates |
| SpouseEmploymentRate | Overall spouse employment rate | Copenhagen research data |
| SpouseUnemploymentRate | Spouse unemployment rate | Copenhagen research data |
| Spouse FullTime Rate | Full-time employment rate for spouses | Copenhagen research data |

### Measures from Slicers (Interactive)
| Measure Name | Description | User Control |
|--------------|-------------|--------------|
| Selected percentage With Working Accompanying Partner | User-selected employment rate | Slicer: 10%-70% |
| Selected percentage With unemployed or underemployed Accompanying Partner | Inverse of selected employment | `1 - Selected employment rate` |
| Potential Extra Workers | Additional workers from spouse employment | `Workers × Selected employment rate` |

### Segmented Analysis
| Measure Name | Description | Purpose |
|--------------|-------------|---------|
| SegmentedCurrentEstimates | Current worker distribution by segment | Baseline segmentation |
| SegmentedProjection | Projected workers under scenarios | Scenario-based segmentation |
| Current Estimate of Workers with an accompanying partner (2025) | Workers with partners in 2025 | Key baseline calculation |
| Estimate of Number of Un and Underemployed Partners | Current untapped workforce | Gap analysis |
| Potential Number of Un and Underemployed Partners | Scenario-based untapped workforce | Interactive calculation |

### Retention Analysis
| Measure Name | Description | Research Basis |
|--------------|-------------|----------------|
| Retention All Unemployed Partners (2025-2030) | Workers retained if no partners work | 49% retention rate (Copenhagen) |
| Retention Selected Value of Employed Partners (2025-2030) | Workers retained with employed partners | 61% retention rate (Copenhagen) |
| Retention Selected Value of Unemployed Partners (2025-2030) | Workers retained with unemployed partners | 49% retention rate (Copenhagen) |
| Retention Selected Total | Total retained workers under scenario | Sum of employed + unemployed segments |

### Recruitment Strategy Analysis
| Measure Name | Description | Strategic Purpose |
|--------------|-------------|-------------------|
| Approximate recruitment of single workers per year needed to allow for five year retention | Single-worker strategy requirements | `7500 ÷ (retention rate × 5 years)` |
| Recruitment of households needed to allow for five year retention per year | Household-based strategy requirements | Accounts for dual-career benefits |

### Forecasting & Graphing
| Measure Name | Description | Purpose |
|--------------|-------------|---------|
| Total Work Permits Forecast | Projected work permits | Baseline projection |
| Total Net Migration Forecast | Projected net migration | Migration trends |
| Target Line Workers | Target trajectory (1500/year) | Goal visualization |
| Work Permits Uncertainty Positive/Negative | Forecast confidence bands | Error bars for charts |
| Net migration Uncertainty Positive/Negative | Migration forecast uncertainty | Error bars for charts |

### Text Measures (Dynamic Narratives)
| Measure Name | Description | Updates Based On |
|--------------|-------------|------------------|
| Title Page 1 | "Aarhus Could Gain X Extra Workers..." | Selected employment rate |
| Title Page 2 | "How Many New Households..." | Static title |
| Narrative Page 1 Part 1 | Explains current situation | Current statistics |
| Narrative Page 1 Part 2 | Explains retention scenarios | Selected parameters |
| Narrative Page 2 Part 1 | Single worker strategy text | Static |
| Narrative Page 2 Part 2 | Household strategy text | Selected employment rate |
| Footer | Attribution and data refresh date | Metadata table |

## Core Model Logic

### Spouse Employment Scenario Calculations
1. **Baseline Segmentation**:
   - Single workers: `[Current Percentage of single workers with work permits]`
   - Workers with Danish partners: `[Current percentage with a Danish partner]`
   - Workers with accompanying partners: `[Current percentage with an accompanying partner]`

2. **Employment Scenarios**:
   - Employed partners: `[Total Partners] × [Selected percentage With Working Accompanying Partner]`
   - Unemployed partners: `[Total Partners] × [Selected percentage With unemployed Accompanying Partner]`

3. **Retention Calculations**:
   - High retention (employed partner): 61% over 5 years
   - Low retention (unemployed partner): 49% over 5 years
   - Dual career benefit: Counts both worker and partner as contributors

4. **Recruitment Strategy Comparison**:
   - Single strategy: `7500 ÷ (single retention rate × 5)`
   - Household strategy: `7500 ÷ (weighted average retention × household multiplier × 5)`

## Data Relationships

The model uses the following key relationships:
- **fact_all_permits** connects to **dim_calendar** (Year)
- **fact_migration** connects to **dim_calendar** (Year) 
- **fact_population** connects to **dim_calendar** (Year)
- **fact_forecast** connects to **dim_calendar** (Year)
- **fact_retention** provides lookup data for retention calculations
- **dim_Segments** provides segmentation context for worker categorization
- **param_% Employment of Accompanying Partner** drives interactive scenario calculations
- All measures in **Measures Folder** reference these fact and dimension tables

## Model Refresh Strategy

Based on your refresh configuration, the model updates:
1. **Fact tables** (permits, migration, population, forecast) - Core data refresh
2. **Dimension tables** (calendar, segments, constants) - Reference data
3. **Parameter tables** - Interactive scenario controls  
4. **Metadata** - Model documentation and timestamps
5. **Measures Folder** - Calculated measure container

### Refresh Dependencies
- **Historical data** (fact_all_permits, fact_migration, fact_population) should refresh first
- **Forecast data** (fact_forecast) depends on updated historical data
- **Constants and parameters** provide stable reference values
- **Measures** calculate dynamically based on refreshed fact data

## Interactive Elements

### Key Slicer: Partner Employment Rate
- **Purpose**: Allows users to explore different spouse employment scenarios
- **Values**: 10%, 20%, 30% (default), 40%, 50%, 60%, 70%
- **Impact**: Dynamically updates all recruitment and retention calculations

### Dashboard Pages
1. **Untapped Workforce** - Shows potential within existing population
2. **Internationalisation Ambitions** - Shows recruitment needs under different scenarios

## Usage Guidelines

### Scenario Analysis Best Practices
1. Use the partner employment rate slicer to explore different policy outcomes
2. Compare "New households needed" between single vs. couple recruitment strategies
3. Focus on the "Untapped Workforce" metric to quantify internal opportunities
4. Use retention rate differentials to justify spouse employment investments

### Key Insights from the Model
1. **Current inefficiency**: Only ~44% of partners work, leaving ~700 potential workers untapped
2. **Retention multiplier**: Employed partners increase household retention from 49% to 61%
3. **Recruitment efficiency**: Couple-focused strategy needs ~300 fewer households annually than single-focused
4. **Dual benefit**: Spouse employment both adds workers directly AND improves retention

### Known Limitations
1. **Copenhagen data proxy**: Uses Copenhagen spouse employment rates as proxy for Aarhus
2. **Retention assumption**: Applies Copenhagen retention rates (61% vs 49%) to Aarhus context
3. **Static scenarios**: Doesn't model dynamic changes in employment rates over time
4. **Household composition**: Assumes fixed ratios of single vs. coupled workers
5. **New arrival assumption**: Treats all workers as new arrivals due to data limitations

## Maintenance

### Adding New Scenarios
1. Add new partner employment rates to the slicer range
2. Update scenario parameters in `DimScenario`
3. Refresh calculated measures that depend on scenario selection

### Updating with New Data
1. **Historical data**: Add new records to fact_all_permits, fact_migration, fact_population
2. **Forecast updates**: Re-run forecast scripts and update fact_forecast table
3. **Research constants**: Update dim_constants_research if new retention studies become available
4. **Parameter ranges**: Modify param_% Employment of Accompanying Partner if expanding scenario range
5. **Metadata refresh**: Update MetaData table with new refresh timestamps

### Model Validation Checklist
1. **Parameter consistency**: Ensure employment percentages sum correctly across segments
2. **Retention logic**: Verify that higher employment rates produce higher retention calculations  
3. **Forecast alignment**: Check that baseline forecasts align with historical trends
4. **Text measure updates**: Confirm dynamic narratives reflect current parameter selections
5. **Total reconciliation**: Verify that segmented calculations sum to expected totals

### Data Quality Monitoring
- **Missing values**: Monitor for gaps in historical permit and migration data
- **Outlier detection**: Flag unusual spikes in immigration or permit numbers
- **Consistency checks**: Compare forecast uncertainty bounds with historical volatility
- **Parameter bounds**: Ensure interactive slicers stay within realistic ranges (0-100%)

---

*This model demonstrates the strategic value of spouse employment policies in achieving workforce targets more efficiently than pure recruitment strategies. The interactive design allows policy makers to explore different scenarios and understand the multiplicative effects of dual-career household support.*

*Model Database: retention*  
*Last Updated: May 24, 2025*