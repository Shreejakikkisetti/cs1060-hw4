#!/usr/bin/env python3

"""
CSV to SQLite Converter
This script converts CSV files to SQLite database tables.

Author: Created with assistance from Codeium AI
Sources: 
- SQLite documentation: https://docs.python.org/3/library/sqlite3.html
- CSV documentation: https://docs.python.org/3/library/csv.html
"""

import sqlite3
import csv
import sys
import os

def normalize_column_name(name: str) -> str:
    """
    Normalize column names to match the expected format.
    
    Args:
        name (str): Original column name
    Returns:
        str: Normalized column name
    """
    # Remove any BOM character that might be present
    name = name.replace('\ufeff', '')
    # Convert to lowercase for consistency
    return name.lower()

def create_table_from_csv(db_path: str, csv_path: str) -> None:
    """
    Create a SQLite table from a CSV file.
    
    Args:
        db_path (str): Path to the SQLite database
        csv_path (str): Path to the CSV file
    """
    # Get the table name from the CSV filename without extension
    table_name = os.path.splitext(os.path.basename(csv_path))[0]
    
    try:
        # Read CSV header to get column names
        with open(csv_path, 'r', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            headers = [normalize_column_name(header) for header in next(csv_reader)]
            
            # Create SQL column definitions (all columns as TEXT)
            columns = [f"{header} TEXT" for header in headers]
            
            # Connect to SQLite database
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table with the columns from CSV
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            cursor.execute(create_table_sql)
            
            # Read and insert data
            for row in csv_reader:
                # Create placeholders for the INSERT statement
                placeholders = ','.join(['?' for _ in row])
                insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
                cursor.execute(insert_sql, row)
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
    except Exception as e:
        print(f"Error processing {csv_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to handle command line arguments and execute the conversion."""
    if len(sys.argv) != 4:
        print("Usage: python3 csv_to_sqlite.py <database_file> <zip_county_csv> <health_rankings_csv>", file=sys.stderr)
        sys.exit(1)
    
    db_path = sys.argv[1]
    zip_csv = sys.argv[2]
    health_csv = sys.argv[3]
    
    # Verify CSV files exist
    for csv_path in [zip_csv, health_csv]:
        if not os.path.exists(csv_path):
            print(f"Error: CSV file '{csv_path}' not found", file=sys.stderr)
            sys.exit(1)
    
    create_table_from_csv(db_path, zip_csv)
    create_table_from_csv(db_path, health_csv)

if __name__ == "__main__":
    main()
