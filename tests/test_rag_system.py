import unittest
import pandas as pd
import numpy as np
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.rag_system import (
    initialize_kb,
    query_knowledge_base,
    generate_answer
)

class TestRAGSystem(unittest.TestCase):
    """Tests for the RAG system module."""
    
    def setUp(self):
        """Set up test data."""
        # Create a sample knowledge base
        self.sample_kb = pd.DataFrame({
            'content': [
                "Recovery time between high-intensity workouts should be 48-72 hours for optimal results.",
                "Sleep plays a crucial role in athletic performance by enhancing recovery and hormone regulation.",
                "Vertical jump can be improved through plyometric exercises, strength training, and technique work.",
                "Nutritional needs vary between training phases: more carbs during high-volume phases, more protein during recovery.",
                "The most effective treatment for muscle cramps includes stretching, hydration, and electrolyte replacement."
            ],
            'title': [
                "Recovery Protocols",
                "Sleep and Performance",
                "Jump Training",
                "Nutritional Periodization",
                "Muscle Cramp Treatment"
            ],
            'source': [
                "Journal of Sports Science 2022",
                "Sleep Medicine Reviews 2021",
                "Strength and Conditioning Journal 2020",
                "International Journal of Sport Nutrition 2019",
                "Sports Medicine 2018"
            ]
        })
        
        # Sample embeddings (simplified for testing)
        self.sample_embeddings = np.random.rand(5, 128)  # 5 documents, 128-dimensional embeddings
    
    @patch('utils.rag_system.pd.read_csv')
    @patch('utils.rag_system.faiss.IndexFlatL2')
    @patch('utils.rag_system.np.load')
    def test_initialize_kb(self, mock_np_load, mock_faiss_index, mock_read_csv):
        """Test knowledge base initialization."""
        # Mock the dependencies
        mock_read_csv.return_value = self.sample_kb
        mock_np_load.return_value = self.sample_embeddings
        mock_index = MagicMock()
        mock_faiss_index.return_value = mock_index
        
        # Initialize the knowledge base
        initialize_kb()
        
        # Check if the knowledge base was loaded
        mock_read_csv.assert_called_once()
        mock_np_load.assert_called_once()
        
        # Check if the index was created and populated
        mock_index.add.assert_called_once()
    
    @patch('utils.rag_system.generate_answer')
    def test_query_knowledge_base(self, mock_generate_answer):
        """Test querying the knowledge base."""
        # Mock the dependencies
        mock_generate_answer.return_value = "Recovery time varies but is typically 48-72 hours."
        
        # Set up a mock for relevant docs
        with patch('utils.rag_system.kb_index') as mock_kb_index:
            mock_kb_index.search.return_value = (
                np.array([[0.1, 0.2, 0.3]]),  # Distances
                np.array([[0, 1, 2]])  # Indices
            )
            
            # Set up a mock for the knowledge base
            with patch('utils.rag_system.kb_data', self.sample_kb):
                # Query the knowledge base
                result = query_knowledge_base("What is the optimal recovery time between workouts?")
                
                # Check if the result contains expected keys
                self.assertIn('answer', result)
                self.assertIn('sources', result)
                
                # Check if sources are provided
                self.assertTrue(len(result['sources']) > 0)
    
    def test_generate_answer(self):
        """Test answer generation from relevant documents."""
        query = "How important is sleep for athletes?"
        relevant_docs = self.sample_kb.iloc[[1, 0, 3]]  # Sleep, Recovery, Nutrition
        
        # Generate an answer
        answer = generate_answer(query, relevant_docs)
        
        # Check if an answer is generated
        self.assertIsNotNone(answer)
        self.assertTrue(len(answer) > 0)
        
        # Check if the answer uses information from the most relevant document
        self.assertIn("sleep", answer.lower())

if __name__ == '__main__':
    unittest.main()