"""
Create a representative test dataset for Vercel deployment
This script samples the full CSV files to create a smaller but representative dataset
"""

import csv
import random

# List of ZIP codes we want to include (one from each region)
TARGET_ZIPS = [
    "02138",  # Cambridge, MA
    "10001",  # New York, NY
    "90001",  # Los Angeles, CA
    "60601",  # Chicago, IL
    "75001",  # Dallas, TX
    "98101",  # Seattle, WA
    "33101",  # Miami, FL
    "80201",  # Denver, CO
    "19101",  # Philadelphia, PA
    "20001",  # Washington, DC
]

def sample_zip_data():
    """Create a sample zip_county dataset"""
    with open('zip_county.csv', 'r') as infile, \
         open('test_zip_county.csv', 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        # Keep track of counties we need health data for
        counties = set()
        
        for row in reader:
            if row['zip'] in TARGET_ZIPS:
                writer.writerow(row)
                counties.add((row['county'], row['state_abbreviation']))
        
        return counties

def sample_health_data(counties):
    """Create a sample health rankings dataset"""
    with open('county_health_rankings.csv', 'r') as infile, \
         open('test_county_health_rankings.csv', 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
        writer.writeheader()
        
        for row in reader:
            if (row['county'], row['state']) in counties:
                writer.writerow(row)

if __name__ == '__main__':
    print("Creating sample datasets...")
    counties = sample_zip_data()
    sample_health_data(counties)
    print("Done! Created test_zip_county.csv and test_county_health_rankings.csv")
