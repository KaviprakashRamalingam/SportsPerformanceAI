import unittest
import numpy as np
import sys
import os
from unittest.mock import patch

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.image_analyzer import (
    analyze_form,
    analyze_keypoints,
    calculate_angle,
    detect_pose
)

class TestImageAnalyzer(unittest.TestCase):
    """Tests for the image_analyzer module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a dummy image array
        self.dummy_image = np.zeros((300, 300, 3), dtype=np.uint8)
        
        # Create a sample of keypoints
        self.sample_keypoints = {
            "nose": (150, 50),
            "left_shoulder": (120, 100),
            "right_shoulder": (180, 100),
            "left_elbow": (100, 150),
            "right_elbow": (200, 150),
            "left_wrist": (90, 200),
            "right_wrist": (210, 200),
            "left_hip": (130, 170),
            "right_hip": (170, 170),
            "left_knee": (120, 220),
            "right_knee": (180, 220),
            "left_ankle": (110, 270),
            "right_ankle": (190, 270)
        }
    
    def test_calculate_angle(self):
        """Test calculation of angles between points."""
        # Test angle between three points (elbow angle)
        angle = calculate_angle(
            self.sample_keypoints["left_shoulder"],
            self.sample_keypoints["left_elbow"],
            self.sample_keypoints["left_wrist"]
        )
        # The angle should be approximately 180 degrees (straight arm)
        self.assertAlmostEqual(angle, 180.0, delta=10.0)
        
        # Test angle with vertical line
        angle = calculate_angle(
            self.sample_keypoints["left_hip"],
            self.sample_keypoints["left_knee"],
            vertical=True
        )
        # Should be close to 0 (vertical alignment)
        self.assertLess(angle, 20.0)
    
    def test_analyze_keypoints(self):
        """Test analysis of keypoints."""
        # Test with our sample keypoints
        image_shape = (300, 300)
        analysis_results = analyze_keypoints(self.sample_keypoints, image_shape)
        
        # Check if the results contain expected keys
        self.assertIn("posture", analysis_results)
        self.assertIn("joint_angles", analysis_results)
        self.assertIn("symmetry", analysis_results)
        self.assertIn("overall_score", analysis_results)
        
        # Check if joint angles are calculated
        self.assertIn("knee_angle_left", analysis_results["joint_angles"])
        self.assertIn("knee_angle_right", analysis_results["joint_angles"])
        self.assertIn("hip_angle_left", analysis_results["joint_angles"])
        self.assertIn("hip_angle_right", analysis_results["joint_angles"])
        
    @patch('utils.image_analyzer.detect_pose')
    def test_analyze_form(self, mock_detect_pose):
        """Test form analysis from an image."""
        # Mock the detect_pose function to return our sample keypoints
        mock_detect_pose.return_value = self.sample_keypoints
        
        # Analyze form using the dummy image
        form_analysis, annotated_image = analyze_form(self.dummy_image)
        
        # Check if form analysis contains expected keys
        self.assertIn("posture", form_analysis)
        self.assertIn("joint_angles", form_analysis)
        self.assertIn("symmetry", form_analysis)
        self.assertIn("overall_score", form_analysis)
        
        # Check if the annotated image is returned
        self.assertIsNotNone(annotated_image)
        self.assertEqual(annotated_image.shape, self.dummy_image.shape)
    
    @patch('utils.image_analyzer.cv2.dnn.readNetFromTensorflow')
    @patch('utils.image_analyzer.cv2.dnn.blobFromImage')
    @patch('utils.image_analyzer.cv2.dnn.Net.forward')
    def test_detect_pose(self, mock_forward, mock_blob, mock_read_net):
        """Test pose detection from an image."""
        # Mock the output of the neural network
        mock_net_output = np.zeros((1, 19, 14, 14))
        # Set some confidence values for keypoints
        for i in range(14):
            mock_net_output[0, i, 7, 7] = 0.9  # High confidence at center
        mock_forward.return_value = mock_net_output
        
        # Detect pose
        keypoints = detect_pose(self.dummy_image)
        
        # Check if keypoints are detected
        self.assertIsNotNone(keypoints)
        self.assertTrue(len(keypoints) > 0)

if __name__ == '__main__':
    unittest.main()