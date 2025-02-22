"""
Optimize the CSV data for Vercel deployment
Creates a compressed JSON file that's optimized for our API queries
"""

import csv
import json
import gzip
import os

def process_csvs():
    # Create api directory if it doesn't exist
    os.makedirs('api', exist_ok=True)
    
    # Process zip_county.csv
    zip_to_county = {}
    with open('zip_county.csv', 'r') as f:
        # Skip BOM if present
        f.seek(0)
        first_char = f.read(1)
        if first_char != '\ufeff':
            f.seek(0)
        
        reader = csv.DictReader(f)
        for row in reader:
            zip_code = row['zip'].strip()
            zip_to_county[zip_code] = {
                'county': row['county'].strip(),
                'state': row['state_abbreviation'].strip()
            }
    
    # Process county_health_rankings.csv
    health_data = {}
    with open('county_health_rankings.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row['County'].strip(), row['State'].strip(), row['Measure_name'].strip())
            if key not in health_data:
                health_data[key] = []
            health_data[key].append({
                'year_span': row['Year_span'].strip(),
                'measure_id': row['Measure_id'].strip(),
                'numerator': row['Numerator'].strip(),
                'denominator': row['Denominator'].strip(),
                'raw_value': row['Raw_value'].strip(),
                'confidence_interval_lower_bound': row['Confidence_Interval_Lower_Bound'].strip(),
                'confidence_interval_upper_bound': row['Confidence_Interval_Upper_Bound'].strip(),
                'data_release_year': row['Data_Release_Year'].strip(),
                'fipscode': row['fipscode'].strip()
            })
    
    # Convert to a format that can be serialized
    health_data_serializable = {
        f"{county}|{state}|{measure}": data 
        for (county, state, measure), data in health_data.items()
    }
    
    # Create the optimized data structure
    optimized_data = {
        'zip_to_county': zip_to_county,
        'health_data': health_data_serializable
    }
    
    # Save as compressed JSON
    with gzip.open('api/optimized_data.json.gz', 'wt') as f:
        json.dump(optimized_data, f)

if __name__ == '__main__':
    process_csvs()
    print("Created optimized data file: api/optimized_data.json.gz")
