import unittest
import pandas as pd
import sys
import os
import datetime

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.database import (
    init_db, get_or_create_athlete, save_performance_data,
    get_athlete_performance_data, save_form_analysis,
    get_athlete_form_analyses, get_all_athletes, delete_athlete,
    store_dataframe, load_dataframe, Athlete, PerformanceData, FormAnalysis
)

class TestDatabase(unittest.TestCase):
    """Tests for the database module."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the database for testing."""
        # Initialize the database
        init_db()
        
    def setUp(self):
        """Set up test data for each test."""
        # Create a test athlete
        self.test_athlete = get_or_create_athlete(
            name="TestAthlete",
            sport="Running",
            team="Test Team",
            age=25
        )
        
        # Create sample performance data
        self.sample_metrics = {
            "Strength": 85.0,
            "Speed": 92.0,
            "Endurance": 78.0,
            "Recovery Time": 24.0,
            "Technique Score": 88.0
        }
        
        # Create sample form analysis data
        self.sample_analysis = {
            "joint_angles": {
                "knee": 120,
                "hip": 100,
                "ankle": 80
            },
            "posture": "good",
            "balance": "excellent"
        }
        
        self.sample_recommendations = {
            "technique": ["Improve knee extension", "Maintain upright posture"],
            "training": ["Add plyometric exercises", "Focus on ankle mobility"]
        }
        
    def tearDown(self):
        """Clean up after each test."""
        # Delete the test athlete and all associated data
        delete_athlete("TestAthlete")
    
    def test_get_or_create_athlete(self):
        """Test creating and retrieving an athlete."""
        # Test creating a new athlete
        athlete = get_or_create_athlete(
            name="TestAthlete2",
            sport="Swimming",
            team="Test Team 2",
            age=28
        )
        self.assertIsNotNone(athlete)
        self.assertEqual(athlete.name, "TestAthlete2")
        self.assertEqual(athlete.sport, "Swimming")
        
        # Test retrieving an existing athlete
        same_athlete = get_or_create_athlete(name="TestAthlete2")
        self.assertEqual(same_athlete.id, athlete.id)
        
        # Clean up
        delete_athlete("TestAthlete2")
    
    def test_save_and_get_performance_data(self):
        """Test saving and retrieving performance data."""
        # Save performance data for the test athlete
        for metric, value in self.sample_metrics.items():
            save_performance_data(
                athlete_name="TestAthlete",
                metric_name=metric,
                metric_value=value,
                notes=f"Test {metric}"
            )
        
        # Retrieve the performance data
        performance_data = get_athlete_performance_data("TestAthlete")
        
        # Check if data was retrieved correctly
        self.assertFalse(performance_data.empty)
        self.assertEqual(len(performance_data), len(self.sample_metrics))
        
        # Check if all metrics are in the retrieved data
        for metric in self.sample_metrics.keys():
            self.assertIn(metric, performance_data.columns)
    
    def test_save_and_get_form_analysis(self):
        """Test saving and retrieving form analysis data."""
        # Save form analysis for the test athlete
        save_form_analysis(
            athlete_name="TestAthlete",
            exercise_type="Squat",
            analysis_data=self.sample_analysis,
            recommendations=self.sample_recommendations
        )
        
        # Retrieve the form analysis data
        form_analyses = get_athlete_form_analyses("TestAthlete")
        
        # Check if data was retrieved correctly
        self.assertEqual(len(form_analyses), 1)
        self.assertEqual(form_analyses[0]["exercise_type"], "Squat")
        
        # Check if analysis data and recommendations are in the retrieved data
        self.assertEqual(form_analyses[0]["analysis_data"]["posture"], "good")
        self.assertEqual(form_analyses[0]["recommendations"]["technique"][0], "Improve knee extension")
    
    def test_get_all_athletes(self):
        """Test retrieving all athletes."""
        # Get all athletes
        all_athletes = get_all_athletes()
        
        # Check if the test athlete is in the list
        found = False
        for athlete in all_athletes:
            if athlete["name"] == "TestAthlete":
                found = True
                break
        
        self.assertTrue(found)
    
    def test_store_and_load_dataframe(self):
        """Test storing and loading a DataFrame."""
        # Create a sample DataFrame
        df = pd.DataFrame({
            "Athlete": ["TestAthlete", "TestAthlete", "TestAthlete"],
            "Date": [pd.Timestamp("2023-01-01"), pd.Timestamp("2023-01-08"), pd.Timestamp("2023-01-15")],
            "Strength": [80, 82, 85],
            "Speed": [90, 92, 95],
            "Endurance": [70, 72, 75]
        })
        
        # Store the DataFrame
        success = store_dataframe("TestAthlete", df)
        self.assertTrue(success)
        
        # Load the DataFrame
        loaded_df = load_dataframe("TestAthlete")
        
        # Check if data was loaded correctly
        self.assertFalse(loaded_df.empty)
        self.assertIn("Strength", loaded_df.columns)
        self.assertIn("Speed", loaded_df.columns)
        self.assertIn("Endurance", loaded_df.columns)
    
    def test_delete_athlete(self):
        """Test deleting an athlete."""
        # Create a temporary athlete
        get_or_create_athlete(name="TempAthlete")
        
        # Delete the athlete
        success = delete_athlete("TempAthlete")
        self.assertTrue(success)
        
        # Check if the athlete was deleted
        all_athletes = get_all_athletes()
        found = False
        for athlete in all_athletes:
            if athlete["name"] == "TempAthlete":
                found = True
                break
        
        self.assertFalse(found)
    
if __name__ == '__main__':
    unittest.main()