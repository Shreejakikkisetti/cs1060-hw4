"""
County Data API Endpoint
Created with assistance from Codeium AI
"""

from flask import Flask, request, jsonify
import sqlite3
import os
import csv

app = Flask(__name__)

VALID_MEASURES = {
    "Violent crime rate",
    "Unemployment",
    "Children in poverty",
    "Diabetic screening",
    "Mammography screening",
    "Preventable hospital stays",
    "Uninsured",
    "Sexually transmitted infections",
    "Physical inactivity",
    "Adult obesity",
    "Premature Death",
    "Daily fine particulate matter"
}

def create_tables(cursor):
    """Create the necessary tables"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS zip_county (
            zip TEXT,
            default_state TEXT,
            county TEXT,
            county_state TEXT,
            state_abbreviation TEXT,
            county_code TEXT,
            zip_pop TEXT,
            zip_pop_in_county TEXT,
            n_counties TEXT,
            default_city TEXT
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS county_health_rankings (
            state TEXT,
            county TEXT,
            state_code TEXT,
            county_code TEXT,
            year_span TEXT,
            measure_name TEXT,
            measure_id TEXT,
            numerator TEXT,
            denominator TEXT,
            raw_value TEXT,
            confidence_interval_lower_bound TEXT,
            confidence_interval_upper_bound TEXT,
            data_release_year TEXT,
            fipscode TEXT
        )
    ''')

def load_csv_data(cursor, csv_path, table_name):
    """Load data from CSV file into SQLite table"""
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        # Skip BOM if present
        first_char = csvfile.read(1)
        if first_char != '\ufeff':
            csvfile.seek(0)
        
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip header
        
        # Insert data in batches
        batch_size = 1000
        rows = []
        
        if table_name == 'zip_county':
            placeholders = ','.join(['?' for _ in range(10)])
        else:
            placeholders = ','.join(['?' for _ in range(14)])
            
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        
        for row in csv_reader:
            rows.append(row)
            if len(rows) >= batch_size:
                cursor.executemany(insert_sql, rows)
                rows = []
        
        if rows:
            cursor.executemany(insert_sql, rows)

def init_db():
    """Initialize in-memory database with data from CSV files"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create tables
    create_tables(cursor)
    
    # Get the directory containing the CSV files
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Load zip_county data
    zip_csv = os.path.join(base_dir, 'zip_county.csv')
    load_csv_data(cursor, zip_csv, 'zip_county')
    
    # Load health rankings data
    health_csv = os.path.join(base_dir, 'county_health_rankings.csv')
    load_csv_data(cursor, health_csv, 'county_health_rankings')
    
    conn.commit()
    return conn

def get_county_from_zip(zip_code, conn):
    """Get county information from zip code"""
    cursor = conn.cursor()
    cursor.execute(
        "SELECT county, state_abbreviation, county_code FROM zip_county WHERE zip = ?", 
        (zip_code,)
    )
    return cursor.fetchone()

def get_health_data(county, state, measure_name, conn):
    """Get health data for a specific county and measure"""
    cursor = conn.cursor()
    
    # Get all matching records
    cursor.execute("""
        SELECT *
        FROM county_health_rankings
        WHERE county = ? 
        AND state = ?
        AND measure_name = ?
    """, (county, state, measure_name))
    
    # Get column names
    columns = [description[0] for description in cursor.description]
    
    # Fetch all rows and convert to list of dicts
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append(dict(zip(columns, row)))
    
    return result

@app.route('/county_data', methods=['POST'])
def county_data():
    try:
        # Check content type
        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        data = request.get_json()
        
        # Check for teapot easter egg
        if data.get('coffee') == 'teapot':
            return "I'm a teapot", 418
        
        # Validate required fields
        zip_code = data.get('zip')
        measure_name = data.get('measure_name')
        
        if not zip_code or not measure_name:
            return jsonify({"error": "Both zip and measure_name are required"}), 400
            
        # Validate zip code format
        if not (isinstance(zip_code, str) and len(zip_code) == 5 and zip_code.isdigit()):
            return jsonify({"error": "Invalid zip code format"}), 400
            
        # Validate measure name
        if measure_name not in VALID_MEASURES:
            return jsonify({"error": "Invalid measure_name"}), 400
            
        # Initialize database
        conn = init_db()
        
        # Get county info from zip
        county_info = get_county_from_zip(zip_code, conn)
        if not county_info:
            conn.close()
            return jsonify({"error": f"No county found for zip code {zip_code}"}), 404
            
        county, state, county_code = county_info
        
        # Get health data
        results = get_health_data(county, state, measure_name, conn)
        conn.close()
        
        if not results:
            return jsonify({"error": f"No data found for {county}, {state} with measure {measure_name}"}), 404
            
        return jsonify(results)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Only run the app if this file is run directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
