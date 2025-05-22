#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Aarhus International Workforce Forecast (2026-2030)
---------------------------------------------------

This script forecasts international workforce trends in Aarhus Kommune through 2030,
based on historical data from 2021-2025. It includes detailed projections for population,
worker categories, migration, and permits.

Author: Kelly Rasmussen
Date: May 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import os
import sys

# Create output directory if it doesn't exist
os.makedirs('../outputs', exist_ok=True)

# Display forecasting limitations warning
print("⚠️ FORECASTING LIMITATION WARNING ⚠️")
print("This script projects future trends based solely on historical patterns.")
print("Real-world events (economic shifts, policy changes, geopolitical events)")
print("will likely cause significant deviations from these projections.")
print("Use these forecasts as a baseline, not as definitive predictions.\n")


def load_data():
    """Load and prepare all datasets from the processed data directory"""
    # Load work permits data
    work_permits = pd.read_csv('../data/processed/fact_work_permits.csv')
    work_permits['Total workers'] = work_permits['Full time third country workers'] + work_permits['Full time EU workers']
    
    # Load migration data
    migration = pd.read_csv('../data/processed/fact_migration.csv')
    migration['Net migration'] = migration['Immigration foreign citizens 20-64 years'] - migration['Emigration foreign citizens 20-64 years']
    
    # Load population data
    population = pd.read_csv('../data/processed/fact_population.csv')
    population.rename(columns={' "Foreign citizens 20-64 years"': 'Foreign citizens 20-64 years'}, inplace=True)
    
    # Load retention percentage data
    retention = pd.read_csv('../data/processed/fact_retention_percentage.csv')
    
    # Load all permits data
    all_permits = pd.read_csv('../data/processed/fact_all_permits.csv')
    
    return work_permits, migration, population, retention, all_permits


def generate_forecast_table(historical_dfs, target_columns, years_to_forecast=5, include_cv=True, include_r2=True):
    """
    Generate a forecast table with predictions and realistic uncertainty metrics
    
    Parameters:
    -----------
    historical_dfs : dict
        Dictionary of {name: dataframe} containing historical data
        Each dataframe must have a 'Year' column
    target_columns : dict of lists
        Dictionary of {name: [column_names]} specifying which columns to forecast in each dataframe
    years_to_forecast : int, default=5
        Number of years to forecast
    include_cv : bool, default=True
        Whether to include coefficient of variation in output
    include_r2 : bool, default=True
        Whether to include R-squared in output
    
    Returns:
    --------
    forecast_table : pandas.DataFrame
        A table with columns: Year, Category, Metric, Forecast, Uncertainty
    """
    # Get last year from data
    last_year = max([df['Year'].max() for df in historical_dfs.values()])
    
    # Generate forecast years
    forecast_years = range(last_year + 1, last_year + years_to_forecast + 1)
    
    # Initialize results table
    results = []
    
    # Process each dataset
    for category, df in historical_dfs.items():
        columns = target_columns[category]
        
        for column in columns:
            # Skip columns with missing data
            if df[column].isnull().any():
                continue
                
            # Create model
            X = df['Year'].values.reshape(-1, 1)
            y = df[column].values
            
            model = LinearRegression()
            model.fit(X, y)
            
            # Get y-values for calculation
            y_pred = model.predict(X)
            absolute_deviations = np.abs(y - y_pred)
            
            # Calculate Mean Absolute Error (MAE)
            mae = np.mean(absolute_deviations)
            
            # Coefficient of variation (%)
            mean_value = np.mean(y)
            cv = (np.std(y) / mean_value) * 100 if mean_value != 0 else np.inf
            
            # Get R-squared
            r2 = model.score(X, y)
            
            # Calculate Mean Absolute Percentage Error (MAPE)
            # Avoid division by zero
            valid_y = y[y != 0]
            valid_pred = y_pred[y != 0]
            if len(valid_y) > 0:
                mape = np.mean(np.abs((valid_y - valid_pred) / valid_y)) * 100
            else:
                mape = np.nan
            
            # Generate forecast for future years
            for i, year in enumerate(forecast_years):
                # Calculate how many years into the future
                years_out = i + 1
                
                # Get forecast value
                forecast_value = model.predict([[year]])[0]
                
                # Calculate uncertainty based on MAE with increasing factor
                # We use square root scaling to reduce the growth rate
                uncertainty_factor = np.sqrt(years_out)
                uncertainty = mae * uncertainty_factor
                
                # Cap uncertainty as percentage of forecast value
                max_uncertainty_pct = 50  # Maximum 50% uncertainty
                max_uncertainty = abs(forecast_value) * (max_uncertainty_pct / 100)
                uncertainty = min(uncertainty, max_uncertainty)
                
                # For values near zero, use a minimum absolute uncertainty
                min_uncertainty = 50  # Minimum uncertainty of 50 units
                if abs(forecast_value) < 1000:
                    uncertainty = max(uncertainty, min_uncertainty)
                
                # Create a row for the results table
                result_row = {
                    'Year': year,
                    'Category': category,
                    'Metric': column,
                    'Forecast': round(forecast_value),
                    'Uncertainty (±)': round(uncertainty)
                }
                
                # Add optional columns
                if include_cv:
                    result_row['CV (%)'] = round(cv, 1)
                if include_r2:
                    result_row['R²'] = round(r2, 3)
                
                # Add MAPE
                result_row['MAPE (%)'] = round(mape, 1) if not np.isnan(mape) else None
                
                # Add to results
                results.append(result_row)
    
    # Convert to DataFrame and sort
    forecast_table = pd.DataFrame(results)
    forecast_table = forecast_table.sort_values(['Year', 'Category', 'Metric'])
    
    return forecast_table


def assess_forecast_reliability(forecast_table):
    """
    Assess and categorize the reliability of each forecast
    
    Parameters:
    -----------
    forecast_table : pandas.DataFrame
        The forecast table generated by generate_forecast_table
        
    Returns:
    --------
    reliability_table : pandas.DataFrame
        The forecast table with added reliability assessment
    """
    # Create a copy to avoid modifying the original
    reliability_table = forecast_table.copy()
    
    # Calculate uncertainty as percentage of forecast
    reliability_table['Uncertainty (%)'] = (reliability_table['Uncertainty (±)'] / reliability_table['Forecast'].abs()) * 100
    
    # Reliability categories based on uncertainty percentage and R²
    conditions = [
        (reliability_table['Uncertainty (%)'] <= 10) & (reliability_table['R²'] >= 0.9),
        (reliability_table['Uncertainty (%)'] <= 25) & (reliability_table['R²'] >= 0.7),
        (reliability_table['Uncertainty (%)'] <= 40) & (reliability_table['R²'] >= 0.5),
        (reliability_table['Uncertainty (%)'] <= 60),
        (reliability_table['Uncertainty (%)'] > 60)
    ]
    
    categories = [
        'High Reliability',
        'Good Reliability',
        'Moderate Reliability',
        'Low Reliability',
        'Very Low Reliability'
    ]
    
    reliability_table['Reliability'] = np.select(conditions, categories, default='Unknown')
    
    # Round the uncertainty percentage
    reliability_table['Uncertainty (%)'] = reliability_table['Uncertainty (%)'].round(1)
    
    return reliability_table


def plot_forecasts(historical_dfs, forecast_table, metrics_to_plot, output_dir='../outputs/plots'):
    """
    Create visualizations of historical data and forecasts
    
    Parameters:
    -----------
    historical_dfs : dict
        Dictionary of {name: dataframe} containing historical data
    forecast_table : pandas.DataFrame
        Forecast table from generate_forecast_table
    metrics_to_plot : list of tuples
        List of (category, metric) tuples to plot
    output_dir : str
        Directory to save plots
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    for category, metric in metrics_to_plot:
        # Get historical data
        hist_df = historical_dfs[category]
        hist_years = hist_df['Year']
        hist_values = hist_df[metric]
        
        # Get forecast data
        forecast_filter = (forecast_table['Category'] == category) & (forecast_table['Metric'] == metric)
        forecast_df = forecast_table[forecast_filter]
        forecast_years = forecast_df['Year']
        forecast_values = forecast_df['Forecast']
        forecast_lower = forecast_values - forecast_df['Uncertainty (±)']
        forecast_upper = forecast_values + forecast_df['Uncertainty (±)']
        
        # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plot historical data
        ax.plot(hist_years, hist_values, 'o-', color='blue', label='Historical')
        
        # Plot forecast
        ax.plot(forecast_years, forecast_values, 'x--', color='red', label='Forecast')
        
        # Plot uncertainty
        ax.fill_between(forecast_years, forecast_lower, forecast_upper, 
                        color='red', alpha=0.2, label='Uncertainty Range')
        
        # Add vertical line at current year
        current_year = hist_years.max()
        ax.axvline(x=current_year, color='gray', linestyle=':', label='Present')
        
        # Add labels and title
        r2 = forecast_df['R²'].iloc[0]
        reliability = assess_forecast_reliability(forecast_df)['Reliability'].iloc[0]
        ax.set_title(f"{category}: {metric}\nR² = {r2:.3f}, {reliability}")
        ax.set_xlabel('Year')
        ax.set_ylabel(metric)
        
        # Add legend
        ax.legend()
        
        # Save the plot
        safe_metric = metric.replace(' ', '_').replace('/', '_')
        plt.tight_layout()
        plt.savefig(f"{output_dir}/{category}_{safe_metric}.png")
        plt.close()


def print_statistical_concepts():
    """Print explanation of statistical concepts used in the analysis"""
    print("\n" + "="*80)
    print("STATISTICAL CONCEPTS USED IN THIS ANALYSIS".center(80))
    print("="*80)
    print("""
1. LINEAR REGRESSION
   A statistical method that models the relationship between a dependent variable
   and one or more independent variables. In a line graph, it's the gradient or "m".

2. R² (R-SQUARED)
   A statistical measure that represents the proportion of variance in the dependent
   variable that is predictable from the independent variable(s). Values range from
   0 to 1:
   - R² = 0.9+ indicates an excellent fit (trends are highly linear)
   - R² = 0.7-0.9 indicates a good fit (trends are mostly linear)
   - R² = 0.5-0.7 indicates a moderate fit (some variability around the trend)
   - R² < 0.5 indicates a poor fit (high variability or non-linear patterns)

3. MEAN ABSOLUTE ERROR (MAE)
   The average of the absolute differences between predicted values and actual values.
   It gives an idea of how large errors are on average, in the original units of the
   data. We use MAE as the foundation for our uncertainty estimates.

4. MEAN ABSOLUTE PERCENTAGE ERROR (MAPE)
   Expresses the average error as a percentage of the actual values, making it easier
   to understand the relative size of errors.

5. COEFFICIENT OF VARIATION (CV)
   A measure of relative variability calculated as (standard deviation ÷ mean) × 100%.
   Higher values indicate more volatile data that may be harder to predict accurately.

UNCERTAINTY CALCULATION
For each forecast, we calculate uncertainty as follows:
1. Start with the Mean Absolute Error (MAE) from the historical data
2. Increase uncertainty by a factor of √years for each year into the future
3. Cap the maximum uncertainty at 50% of the forecast value
4. Set a minimum uncertainty floor of 50 units for very small values

RELIABILITY ASSESSMENT
Each forecast is categorized based on its uncertainty percentage and R² value:
- High Reliability: Uncertainty ≤ 10% and R² ≥ 0.9
- Good Reliability: Uncertainty ≤ 25% and R² ≥ 0.7
- Moderate Reliability: Uncertainty ≤ 40% and R² ≥ 0.5
- Low Reliability: Uncertainty ≤ 60%
- Very Low Reliability: Uncertainty > 60%
""")
    print("="*80 + "\n")


def main():
    """Main function to run the forecast analysis"""
    # Print explanation of statistical concepts
    print_statistical_concepts()
    
    # Load data
    print("Loading and preparing data...")
    work_permits, migration, population, retention, all_permits = load_data()
    
    # Display data summary
    print("\nData Summary (2021-2025):")
    print(f"Foreign worker population (2025): {population['Foreign citizens 20-64 years'].iloc[-1]:,}")
    print(f"Latest annual net migration (2024): {migration['Net migration'].iloc[-1]:,}")
    print(f"Total international workers (2025): {work_permits['Total workers'].iloc[-1]:,}")
    print("---")
    
    # Define the metrics to forecast
    print("\nDefining forecast parameters...")
    columns_to_forecast = {
        'Foreign Workers': [
            'Full time third country workers', 
            'Full time EU workers',
            'Total workers'
        ],
        'Migration': [
            'Immigration foreign citizens 20-64 years',
            'Emigration foreign citizens 20-64 years',
            'Net migration'
        ],
        'Foreign Population': [
            'Foreign citizens 20-64 years'
        ],
        'Work Permits': [
            'Work permit 3rd country',
            'Work permit EU',
            'Study permit',
            'Family reunification',
            'Permanent residency',
            'Ukraine Emergency Law'
        ]
    }
    
    # Generate forecasts
    print("\nGenerating forecasts for 2026-2030...")
    detailed_forecast = generate_forecast_table(
        historical_dfs={
            'Foreign Workers': work_permits,
            'Migration': migration,
            'Foreign Population': population,
            'Work Permits': all_permits
        },
        target_columns=columns_to_forecast,
        years_to_forecast=5
    )
    
    # Save forecast to CSV
    detailed_forecast.to_csv('../outputs/detailed_forecast_table_2026_2030.csv', index=False)
    print(f"Saved detailed forecasts to ../outputs/detailed_forecast_table_2026_2030.csv")
    
    # Create a pivot table for easier reading
    pivot_by_category = pd.pivot_table(
        detailed_forecast,
        values=['Forecast', 'Uncertainty (±)'],
        index=['Year', 'Category', 'Metric'],
        aggfunc='first'
    ).reset_index()
    
    # Save pivot table
    pivot_by_category.to_csv('../outputs/forecast_pivot_table.csv', index=False)
    print(f"Saved pivot table to ../outputs/forecast_pivot_table.csv")
    
    # Assess reliability
    print("\nAssessing forecast reliability...")
    reliability_assessment = assess_forecast_reliability(detailed_forecast)
    
    # Save reliability assessment
    reliability_assessment.to_csv('../outputs/forecast_reliability_assessment.csv', index=False)
    print(f"Saved reliability assessment to ../outputs/forecast_reliability_assessment.csv")
    
    # Display the most reliable metrics for 2026
    most_reliable = reliability_assessment[reliability_assessment['Year'] == 2026].sort_values(['Uncertainty (%)'])
    
    print("\nMost Reliable Metrics for 2026:")
    print(most_reliable[['Category', 'Metric', 'Forecast', 'Uncertainty (%)', 'Reliability']].head(5).to_string(index=False))
    
    # Display the least reliable metrics for 2026
    least_reliable = reliability_assessment[reliability_assessment['Year'] == 2026].sort_values(['Uncertainty (%)'], ascending=False)
    
    print("\nLeast Reliable Metrics for 2026:")
    print(least_reliable[['Category', 'Metric', 'Forecast', 'Uncertainty (%)', 'Reliability']].head(5).to_string(index=False))
    
    # Generate plots for key metrics
    print("\nGenerating plots for key metrics...")
    metrics_to_plot = [
        ('Foreign Workers', 'Total workers'),
        ('Foreign Population', 'Foreign citizens 20-64 years'),
        ('Migration', 'Net migration'),
        ('Work Permits', 'Work permit 3rd country'),
        ('Work Permits', 'Work permit EU')
    ]
    
    plot_forecasts(
        historical_dfs={
            'Foreign Workers': work_permits,
            'Migration': migration,
            'Foreign Population': population,
            'Work Permits': all_permits
        },
        forecast_table=detailed_forecast,
        metrics_to_plot=metrics_to_plot
    )
    print(f"Saved plots to ../outputs/plots/")
    
    # Summarize reliability by category
    print("\nReliability Summary by Category and Metric:")
    reliability_summary = reliability_assessment.groupby(['Category', 'Metric', 'Reliability']).size().reset_index(name='Count')
    print(reliability_summary.to_string(index=False))
    
 

if __name__ == "__main__":
    main()
