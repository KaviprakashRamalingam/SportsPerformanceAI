import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_processor import (
    process_performance_data,
    calculate_trend,
    identify_strengths_weaknesses,
    extract_key_metrics
)

class TestDataProcessor(unittest.TestCase):
    """Tests for the data_processor module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a sample DataFrame for testing
        self.sample_data = pd.DataFrame({
            'Athlete': ['Athlete1', 'Athlete1', 'Athlete1', 'Athlete2', 'Athlete2'],
            'Date': pd.date_range(start='2023-01-01', periods=5),
            'Strength': [80, 82, 85, 75, 78],
            'Speed': [90, 89, 92, 88, 87],
            'Endurance': [70, 72, 75, 80, 82],
            'Recovery Time': [24, 22, 20, 26, 24],
            'Technique Score': [85, 86, 88, 80, 82]
        })
        
    def test_process_performance_data(self):
        """Test processing of performance data."""
        # Process data for Athlete1
        results = process_performance_data(self.sample_data, 'Athlete1')
        
        # Check if results contains expected keys
        self.assertIn('strengths', results)
        self.assertIn('weaknesses', results)
        self.assertIn('trends', results)
        self.assertIn('avg_metrics', results)
        
        # Check if strengths and weaknesses are identified
        self.assertTrue(len(results['strengths']) > 0)
        self.assertTrue(len(results['weaknesses']) > 0)
        
        # Check that results are specific to Athlete1
        self.assertEqual(len(results['avg_metrics']), 5)  # 5 metrics

    def test_calculate_trend(self):
        """Test trend calculation."""
        # Test increasing trend
        increasing_series = pd.Series([10, 15, 20, 25, 30])
        self.assertEqual(calculate_trend(increasing_series), 'increasing')
        
        # Test decreasing trend
        decreasing_series = pd.Series([30, 25, 20, 15, 10])
        self.assertEqual(calculate_trend(decreasing_series), 'decreasing')
        
        # Test stable trend
        stable_series = pd.Series([20, 21, 19, 20, 21])
        self.assertEqual(calculate_trend(stable_series), 'stable')
        
    def test_identify_strengths_weaknesses(self):
        """Test identification of strengths and weaknesses."""
        # Filter data for Athlete1
        athlete_data = self.sample_data[self.sample_data['Athlete'] == 'Athlete1']
        
        # Get metric columns
        metrics = ['Strength', 'Speed', 'Endurance', 'Recovery Time', 'Technique Score']
        
        # Identify strengths and weaknesses
        strengths, weaknesses = identify_strengths_weaknesses(athlete_data, metrics)
        
        # Check that strengths and weaknesses are identified
        self.assertTrue(len(strengths) > 0)
        self.assertTrue(len(weaknesses) > 0)
        
        # Check that all identified strengths and weaknesses are from the metrics list
        for strength in strengths:
            self.assertIn(strength, metrics)
        for weakness in weaknesses:
            self.assertIn(weakness, metrics)
            
    def test_extract_key_metrics(self):
        """Test extraction of key metrics."""
        # Extract key metrics for Athlete1
        key_metrics = extract_key_metrics(self.sample_data, 'Athlete1')
        
        # Check if key metrics contains expected keys
        self.assertIn('Strength', key_metrics)
        self.assertIn('Speed', key_metrics)
        self.assertIn('Endurance', key_metrics)
        
        # Check if values are correct (should be the latest values for Athlete1)
        self.assertEqual(key_metrics['Strength'], 85)
        self.assertEqual(key_metrics['Speed'], 92)
        self.assertEqual(key_metrics['Endurance'], 75)
        
if __name__ == '__main__':
    unittest.main()