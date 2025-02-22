"""
Test suite for CSV to SQLite conversion
"""

import unittest
import sqlite3
import os
import csv
import tempfile
from csv_to_sqlite import normalize_column_name, create_table_from_csv

class TestCSVToSQLite(unittest.TestCase):
    def setUp(self):
        # Create temporary directory for test files
        self.test_dir = tempfile.mkdtemp()
        
        # Create test CSV files
        self.test_zip_csv = os.path.join(self.test_dir, 'test_zip.csv')
        self.test_health_csv = os.path.join(self.test_dir, 'test_health.csv')
        
        # Create sample zip data
        with open(self.test_zip_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['zip', 'county', 'state'])
            writer.writerow(['12345', 'Test County', 'NY'])
            writer.writerow(['67890', 'Another County', 'CA'])
        
        # Create sample health data
        with open(self.test_health_csv, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['county', 'state', 'measure_name', 'value'])
            writer.writerow(['Test County', 'NY', 'Test Measure', '10'])
            writer.writerow(['Another County', 'CA', 'Test Measure', '20'])
        
        # Create test database
        self.db_path = os.path.join(self.test_dir, 'test.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close database connection
        self.conn.close()
        
        # Clean up test files
        os.remove(self.test_zip_csv)
        os.remove(self.test_health_csv)
        os.remove(self.db_path)
        os.rmdir(self.test_dir)

    def test_normalize_column_name(self):
        """Test column name normalization"""
        test_cases = [
            ('\ufeffColumn', 'column'),  # Test BOM handling
            ('UPPER CASE', 'upper case'),  # Test case conversion
            ('Mixed Case', 'mixed case'),  # Test mixed case
            ('special!@#chars', 'special!@#chars'),  # Test special characters
        ]
        
        for input_name, expected in test_cases:
            self.assertEqual(normalize_column_name(input_name), expected)

    def test_create_table_from_csv(self):
        """Test table creation from CSV"""
        # Create tables from test CSVs
        create_table_from_csv(self.cursor, self.test_zip_csv)
        create_table_from_csv(self.cursor, self.test_health_csv)
        self.conn.commit()
        
        # Verify zip table structure
        self.cursor.execute("PRAGMA table_info(test_zip)")
        columns = [row[1] for row in self.cursor.fetchall()]
        self.assertEqual(columns, ['zip', 'county', 'state'])
        
        # Verify health table structure
        self.cursor.execute("PRAGMA table_info(test_health)")
        columns = [row[1] for row in self.cursor.fetchall()]
        self.assertEqual(columns, ['county', 'state', 'measure_name', 'value'])
        
        # Verify data in zip table
        self.cursor.execute("SELECT * FROM test_zip")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ('12345', 'Test County', 'NY'))
        
        # Verify data in health table
        self.cursor.execute("SELECT * FROM test_health")
        rows = self.cursor.fetchall()
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ('Test County', 'NY', 'Test Measure', '10'))

    def test_handle_missing_file(self):
        """Test handling of missing CSV file"""
        with self.assertRaises(FileNotFoundError):
            create_table_from_csv(self.cursor, 'nonexistent.csv')

if __name__ == '__main__':
    unittest.main()
