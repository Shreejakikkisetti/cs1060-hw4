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

def create_table_from_csv(cursor: sqlite3.Cursor, csv_path: str) -> None:
    """
    Create a SQLite table from a CSV file.
    
    Args:
        cursor: SQLite cursor
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
            
            # Create table with the columns from CSV
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
            cursor.execute(create_table_sql)
            
            # Prepare the INSERT statement once
            placeholders = ','.join(['?' for _ in headers])
            insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
            
            # Read and insert data in batches
            batch_size = 1000
            rows = []
            
            for row in csv_reader:
                rows.append(row)
                if len(rows) >= batch_size:
                    cursor.executemany(insert_sql, rows)
                    rows = []
            
            # Insert any remaining rows
            if rows:
                cursor.executemany(insert_sql, rows)
            
    except Exception as e:
        print(f"Error processing {csv_path}: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    """Main function to handle command line arguments and execute the conversion."""
    if len(sys.argv) < 3:
        print("Usage: python3 csv_to_sqlite.py <database_file> <csv_file> [<csv_file> ...]", file=sys.stderr)
        sys.exit(1)
    
    db_path = sys.argv[1]
    csv_files = sys.argv[2:]
    
    # Verify CSV files exist
    for csv_path in csv_files:
        if not os.path.exists(csv_path):
            print(f"Error: CSV file '{csv_path}' not found", file=sys.stderr)
            sys.exit(1)
    
    # Use a single database connection for all operations
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Process each CSV file
        for csv_path in csv_files:
            create_table_from_csv(cursor, csv_path)
        
        # Commit all changes at once
        conn.commit()
    finally:
        # Always close the connection
        conn.close()

if __name__ == "__main__":
    main()
