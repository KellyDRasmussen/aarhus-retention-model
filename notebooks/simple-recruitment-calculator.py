#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simple Recruitment Target Calculator
-----------------------------------

This script calculates how many people need to be recruited each year to achieve
the target of 1,500 new full-time workers per year, taking into account the 
historical and forecasted emigration rates.

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data
print("Loading data...")
migration = pd.read_csv('../data/processed/fact_migration.csv')
work_permits = pd.read_csv('../data/processed/fact_work_permits.csv')

# Calculate key ratios from historical data
print("\nAnalyzing historical patterns (2021-2024):")

# Calculate total workers
work_permits['Total workers'] = work_permits['Full time third country workers'] + work_permits['Full time EU workers']

# Calculate net migration
migration['Net migration'] = migration['Immigration foreign citizens 20-64 years'] - migration['Emigration foreign citizens 20-64 years']

# Calculate the ratio of emigration to foreign population
# This gives us an idea of what percentage of the foreign population leaves each year
emigration_rates = []
for year in range(2021, 2025):
    year_emigration = migration[migration['Year'] == year]['Emigration foreign citizens 20-64 years'].values[0]
    year_immigration = migration[migration['Year'] == year]['Immigration foreign citizens 20-64 years'].values[0]
    emigration_rate = year_emigration / year_immigration
    emigration_rates.append(emigration_rate)
    print(f"  {year}: {year_emigration} emigrants / {year_immigration} immigrants = {emigration_rate:.2f} ratio")

# Calculate average emigration ratio
avg_emigration_rate = sum(emigration_rates) / len(emigration_rates)
print(f"\nAverage emigration/immigration ratio: {avg_emigration_rate:.2f}")

# Calculate the ratio of new workers to new immigrants
# This tells us what percentage of immigrants become full-time workers
worker_conversion_rates = []
for i in range(1, len(work_permits)):
    year = work_permits.iloc[i]['Year']
    prev_year = work_permits.iloc[i-1]['Year']
    
    # Skip if not consecutive years
    if year != prev_year + 1:
        continue
    
    # Calculate new workers
    new_workers = work_permits.iloc[i]['Total workers'] - work_permits.iloc[i-1]['Total workers']
    
    # Get immigration for this year
    year_immigration = migration[migration['Year'] == year]['Immigration foreign citizens 20-64 years'].values[0]
    
    # Calculate conversion rate
    if year_immigration > 0:
        conversion_rate = new_workers / year_immigration
        worker_conversion_rates.append(conversion_rate)
        print(f"  {year}: {new_workers} new workers / {year_immigration} immigrants = {conversion_rate:.2f} ratio")

# Calculate average worker conversion ratio
avg_worker_conversion_rate = sum(worker_conversion_rates) / len(worker_conversion_rates)
print(f"\nAverage new worker/immigration ratio: {avg_worker_conversion_rate:.2f}")

# Calculate required recruitment for future years
print("\nCalculating required recruitment to achieve 1,500 new workers per year:")

# Formula:
# To get 1,500 net new workers, we need:
# Raw Recruitment = Target / (conversion_rate × (1 - emigration_rate))

# For each year 2026-2030, calculate required recruitment
target_new_workers = 1500
years = list(range(2026, 2031))
required_recruitment = []

for year in years:
    # Using our average rates
    raw_recruitment = target_new_workers / (avg_worker_conversion_rate * (1 - avg_emigration_rate))
    
    # Add to results
    required_recruitment.append({
        'Year': year,
        'Target New Workers': target_new_workers,
        'Required Recruitment': int(round(raw_recruitment)),
        'Anticipated Emigration': int(round(raw_recruitment * avg_emigration_rate)),
        'Expected New Workers': int(round(raw_recruitment * avg_worker_conversion_rate * (1 - avg_emigration_rate)))
    })
    
    print(f"  {year}: Need to recruit {int(round(raw_recruitment))} people to gain {target_new_workers} workers")

# Convert to DataFrame
results_df = pd.DataFrame(required_recruitment)

# Print summary
print("\nDetailed Results:")
print(results_df.to_string(index=False))

# Calculate totals
total_recruitment = results_df['Required Recruitment'].sum()
total_new_workers = results_df['Expected New Workers'].sum()
total_emigration = results_df['Anticipated Emigration'].sum()

print(f"\nSUMMARY (2026-2030):")
print(f"Total recruitment needed: {total_recruitment:,}")
print(f"Total anticipated emigration: {total_emigration:,}")
print(f"Total net new workers: {total_new_workers:,}")
print(f"Annual recruitment target: {int(round(total_recruitment/5)):,} per year")

# Create visualization
plt.figure(figsize=(10, 6))
plt.bar(years, [r['Required Recruitment'] for r in required_recruitment], color='blue', alpha=0.7, label='Required Recruitment')
plt.bar(years, [r['Anticipated Emigration'] for r in required_recruitment], color='red', alpha=0.7, label='Anticipated Emigration')
plt.bar(years, [r['Target New Workers'] for r in required_recruitment], color='green', alpha=0.7, label='Target New Workers')

plt.title('Annual Recruitment Needed to Achieve 1,500 New Workers')
plt.xlabel('Year')
plt.ylabel('Number of People')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('../outputs/recruitment_target.png')
print(f"\nSaved visualization to ../outputs/recruitment_target.png")

# Save results to CSV
results_df.to_csv('../outputs/recruitment_target.csv', index=False)
print(f"Saved detailed results to ../outputs/recruitment_target.csv")
