"""
Test suite for County Health API
"""

import unittest
import json
import os
from api.county_data import app

class TestCountyHealthAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_valid_request(self):
        """Test valid API request"""
        data = {
            'zip': '84102',
            'measure_name': 'Adult obesity'
        }
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) > 0)
        
        # Verify required fields are present
        required_fields = [
            'county', 'state', 'measure_name', 'raw_value',
            'year_span', 'confidence_interval_lower_bound',
            'confidence_interval_upper_bound'
        ]
        for field in required_fields:
            self.assertIn(field, result[0])
        
        # Verify data consistency
        self.assertEqual(result[0]['measure_name'], 'Adult obesity')
        self.assertEqual(result[0]['county'], 'Salt Lake County')
        self.assertEqual(result[0]['state'], 'UT')

    def test_invalid_zip(self):
        """Test invalid ZIP code"""
        data = {
            'zip': '00000',
            'measure_name': 'Adult obesity'
        }
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertIn('No county found for zip code', result['error'])

    def test_invalid_measure(self):
        """Test invalid measure name"""
        data = {
            'zip': '84102',
            'measure_name': 'Invalid Measure'
        }
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Invalid measure_name')

    def test_missing_fields(self):
        """Test missing required fields"""
        # Test missing zip
        data = {'measure_name': 'Adult obesity'}
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Both zip and measure_name are required')
        
        # Test missing measure_name
        data = {'zip': '84102'}
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Both zip and measure_name are required')

    def test_invalid_content_type(self):
        """Test invalid content type"""
        response = self.client.post('/county_data',
                                  data='not json',
                                  content_type='text/plain')
        
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertIn('error', result)
        self.assertEqual(result['error'], 'Content-Type must be application/json')

    def test_teapot_easter_egg(self):
        """Test teapot easter egg"""
        data = {'coffee': 'teapot'}
        response = self.client.post('/county_data',
                                  data=json.dumps(data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.data.decode(), "I'm a teapot")

    def test_all_valid_measures(self):
        """Test all valid measures with a known ZIP code"""
        valid_measures = [
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
        ]
        
        for measure in valid_measures:
            data = {
                'zip': '84102',
                'measure_name': measure
            }
            response = self.client.post('/county_data',
                                      data=json.dumps(data),
                                      content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            result = json.loads(response.data)
            self.assertIsInstance(result, list)
            if len(result) > 0:  # Some measures might not have data
                self.assertEqual(result[0]['measure_name'], measure)

if __name__ == '__main__':
    unittest.main()
