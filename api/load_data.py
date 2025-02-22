"""
Data loading script for the County Health API
This script runs during build time to prepare the data for the API
"""

import csv
import json
import os

def load_csv_to_dict(csv_path):
    """Load CSV file into a list of dictionaries"""
    data = []
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def main():
    # Get the base directory (where the CSV files are)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load both CSV files
    zip_data = load_csv_to_dict(os.path.join(base_dir, 'zip_county.csv'))
    health_data = load_csv_to_dict(os.path.join(base_dir, 'county_health_rankings.csv'))
    
    # Create zip code to county mapping for faster lookups
    zip_mapping = {}
    for row in zip_data:
        zip_mapping[row['zip']] = {
            'county': row['county'],
            'state': row['state_abbreviation'],
            'county_code': row['county_code']
        }
    
    # Create county to health data mapping for faster lookups
    health_mapping = {}
    for row in health_data:
        key = (row['county'], row['state'], row['measure_name'])
        if key not in health_mapping:
            health_mapping[key] = []
        health_mapping[key].append(row)
    
    # Save the processed data
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    with open(os.path.join(data_dir, 'zip_mapping.json'), 'w') as f:
        json.dump(zip_mapping, f)
    
    with open(os.path.join(data_dir, 'health_mapping.json'), 'w') as f:
        json.dump(health_mapping, f)

if __name__ == '__main__':
    main()
