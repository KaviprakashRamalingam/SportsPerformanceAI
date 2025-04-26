import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.recommendation_engine import (
    generate_recommendations,
    _generate_performance_recommendations,
    _generate_form_recommendations,
    _generate_general_recommendations,
    _calculate_trend
)

class TestRecommendationEngine(unittest.TestCase):
    """Tests for the recommendation engine module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a sample performance dataset
        self.sample_data = pd.DataFrame({
            'Athlete': ['Athlete1', 'Athlete1', 'Athlete1', 'Athlete2', 'Athlete2'],
            'Date': pd.date_range(start='2023-01-01', periods=5),
            'Strength': [80, 82, 85, 75, 78],
            'Speed': [90, 89, 92, 88, 87],
            'Endurance': [70, 72, 75, 80, 82],
            'Recovery Time': [24, 22, 20, 26, 24],
            'Technique Score': [85, 86, 88, 80, 82]
        })
        
        # Create a sample form analysis
        self.sample_form_analysis = {
            "posture": "slight forward lean",
            "joint_angles": {
                "knee_angle_left": 110,
                "knee_angle_right": 105,
                "hip_angle_left": 95,
                "hip_angle_right": 92,
                "ankle_angle_left": 80,
                "ankle_angle_right": 82
            },
            "symmetry": {
                "upper_body": "good",
                "lower_body": "moderate asymmetry"
            },
            "overall_score": 75
        }
    
    def test_generate_recommendations(self):
        """Test generating full recommendations."""
        # Generate recommendations using both performance data and form analysis
        recommendations = generate_recommendations(
            performance_data=self.sample_data,
            athlete="Athlete1",
            form_analysis=self.sample_form_analysis
        )
        
        # Check if recommendations contain expected categories
        self.assertIn("Strength Training", recommendations)
        self.assertIn("Speed Development", recommendations)
        self.assertIn("Endurance Training", recommendations)
        self.assertIn("Recovery Strategies", recommendations)
        self.assertIn("Form Improvement", recommendations)
        
        # Check if each category has recommendations
        for category, recs in recommendations.items():
            self.assertTrue(len(recs) > 0)
    
    def test_generate_performance_recommendations(self):
        """Test generating recommendations from performance data only."""
        # Generate recommendations from performance data
        athlete_data = self.sample_data[self.sample_data['Athlete'] == 'Athlete1']
        recommendations = _generate_performance_recommendations(athlete_data, "Athlete1")
        
        # Check if recommendations contain expected categories
        self.assertIn("Strength Training", recommendations)
        self.assertIn("Speed Development", recommendations)
        self.assertIn("Endurance Training", recommendations)
        self.assertIn("Recovery Strategies", recommendations)
        
        # Check if each category has recommendations
        for category, recs in recommendations.items():
            self.assertTrue(len(recs) > 0)
    
    def test_generate_form_recommendations(self):
        """Test generating recommendations from form analysis only."""
        # Generate recommendations from form analysis
        recommendations = _generate_form_recommendations(self.sample_form_analysis)
        
        # Check if recommendations contain expected categories
        self.assertIn("Form Improvement", recommendations)
        self.assertIn("Symmetry Work", recommendations)
        self.assertIn("Mobility Exercises", recommendations)
        
        # Check if each category has recommendations
        for category, recs in recommendations.items():
            self.assertTrue(len(recs) > 0)
            
        # Check if recommendations address identified issues
        form_recs = recommendations["Form Improvement"]
        symmetry_recs = recommendations["Symmetry Work"]
        
        # There should be recommendations for posture issues
        posture_addressed = any("posture" in rec.lower() for rec in form_recs)
        self.assertTrue(posture_addressed)
        
        # There should be recommendations for lower body asymmetry
        asymmetry_addressed = any("asymmetry" in rec.lower() or "imbalance" in rec.lower() for rec in symmetry_recs)
        self.assertTrue(asymmetry_addressed)
    
    def test_generate_general_recommendations(self):
        """Test generating general recommendations."""
        # Generate general recommendations
        recommendations = _generate_general_recommendations()
        
        # Check if recommendations contain expected categories
        self.assertIn("Training Structure", recommendations)
        self.assertIn("Nutrition", recommendations)
        self.assertIn("Recovery", recommendations)
        
        # Check if each category has recommendations
        for category, recs in recommendations.items():
            self.assertTrue(len(recs) > 0)
    
    def test_calculate_trend(self):
        """Test trend calculation."""
        # Test increasing trend
        increasing_series = pd.Series([80, 82, 85, 87, 90])
        trend = _calculate_trend(increasing_series)
        self.assertEqual(trend, "increasing")
        
        # Test decreasing trend
        decreasing_series = pd.Series([90, 87, 85, 82, 80])
        trend = _calculate_trend(decreasing_series)
        self.assertEqual(trend, "decreasing")
        
        # Test stable trend
        stable_series = pd.Series([85, 84, 86, 85, 86])
        trend = _calculate_trend(stable_series)
        self.assertEqual(trend, "stable")
        
        # Test with missing values
        missing_series = pd.Series([80, 82, np.nan, 87, 90])
        trend = _calculate_trend(missing_series)
        self.assertEqual(trend, "increasing")
        
if __name__ == '__main__':
    unittest.main()