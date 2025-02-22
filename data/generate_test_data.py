#!/usr/bin/env python3
import csv
import os

def create_test_data():
    # Sample ZIP codes and their counties
    zip_data = [
        ['02138', 'MA', 'Middlesex County', 'Massachusetts', 'MA', '017', '36125', '1', '1', 'Cambridge'],
        ['10001', 'NY', 'New York County', 'New York', 'NY', '061', '21102', '1', '1', 'New York'],
        ['90210', 'CA', 'Los Angeles County', 'California', 'CA', '037', '20372', '1', '1', 'Beverly Hills'],
        ['60601', 'IL', 'Cook County', 'Illinois', 'IL', '031', '15734', '1', '1', 'Chicago'],
        ['98101', 'WA', 'King County', 'Washington', 'WA', '033', '11188', '1', '1', 'Seattle']
    ]
    
    # Sample health data
    health_data = []
    measures = [
        "Adult obesity",
        "Physical inactivity",
        "Violent crime rate",
        "Children in poverty"
    ]
    
    for state, county, state_code, county_code in [
        ('MA', 'Middlesex County', '25', '017'),
        ('NY', 'New York County', '36', '061'),
        ('CA', 'Los Angeles County', '06', '037'),
        ('IL', 'Cook County', '17', '031'),
        ('WA', 'King County', '53', '033')
    ]:
        for measure in measures:
            health_data.append([
                state, county, state_code, county_code,
                '2010', measure, '11', '1000',
                '10000', '0.1', '0.08', '0.12',
                '2012', f'{state_code}{county_code}'
            ])
    
    # Write test data
    with open('data/zip_county.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['zip', 'default_state', 'county', 'county_state', 
                        'state_abbreviation', 'county_code', 'zip_pop',
                        'zip_pop_in_county', 'n_counties', 'default_city'])
        writer.writerows(zip_data)
    
    with open('data/county_health_rankings.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['state', 'county', 'state_code', 'county_code',
                        'year_span', 'measure_name', 'measure_id', 'numerator',
                        'denominator', 'raw_value', 'confidence_interval_lower_bound',
                        'confidence_interval_upper_bound', 'data_release_year', 'fipscode'])
        writer.writerows(health_data)

if __name__ == '__main__':
    create_test_data()
