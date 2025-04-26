import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import faiss
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for the knowledge base and vector index
kb_data = None
vectorizer = None
index = None
document_map = None

def initialize_kb():
    """
    Initialize the knowledge base by loading the data and creating vector embeddings.
    """
    global kb_data, vectorizer, index, document_map
    
    try:
        # Load the knowledge base data
        kb_file = "data/kb_sports_science.csv"
        kb_data = pd.read_csv(kb_file)
        
        logger.info(f"Loaded knowledge base with {len(kb_data)} documents")
        
        # Create TF-IDF vectorizer
        vectorizer = TfidfVectorizer(stop_words='english')
        
        # Combine title and content for better search
        documents = []
        for _, row in kb_data.iterrows():
            doc_text = f"{row['title']} {row['content']}"
            documents.append(doc_text)
        
        # Fit and transform the documents
        vectors = vectorizer.fit_transform(documents)
        
        # Convert sparse vectors to dense for FAISS
        dense_vectors = vectors.toarray().astype(np.float32)
        
        # Create a FAISS index for efficient similarity search
        dimension = dense_vectors.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(dense_vectors)
        
        # Create a mapping from index to document ID
        document_map = {i: i for i in range(len(kb_data))}
        
        logger.info("Knowledge base initialized successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error initializing knowledge base: {e}")
        return False

def query_knowledge_base(query, num_results=5):
    """
    Query the knowledge base for relevant information.
    
    Args:
        query (str): The query string
        num_results (int): Number of results to return
        
    Returns:
        dict: Query response with answer and sources
    """

    global kb_data, vectorizer, index, document_map
    
    # Quick topic filtering (simple keyword matching)
    sports_keywords = [
    "sports", "athlete", "performance", "training", "recovery", "exercise",
    "strength", "conditioning", "endurance", "mobility", "flexibility", "injury",
    "rehabilitation", "rehab", "stretching", "warmup", "cooldown", "nutrition",
    "hydration", "coaching", "workout", "drills", "technique", "form", "posture",
    "biomechanics", "sports science", "periodization", "fitness", "health",
    "aerobic", "anaerobic", "cardio", "power", "speed", "agility", "reaction time",
    "mental toughness", "focus", "sports psychology", "fatigue", "lactate threshold",
    "VO2 max", "muscle soreness", "DOMS", "overtraining", "tapering", "game strategy",
    "teamwork", "sportsmanship", "competition", "tournament", "match", "league",
    "Olympics", "Paralympics", "soccer", "football", "basketball", "baseball",
    "tennis", "swimming", "running", "cycling", "hockey", "rugby", "golf",
    "wrestling", "boxing", "MMA", "skiing", "snowboarding", "climbing", "rowing",
    "cricket", "badminton", "track and field", "triathlon", "surfing", "diving",
    "weightlifting", "bodybuilding", "yoga", "pilates", "muscle", "knee", "shouder", 
    "calf", "ankle", "elbow", "wrist", "hip", "back", "core", "abs", "glutes", "quads", 
    "hamstrings", "biceps", "triceps"
    ]

    
    # Lowercase query
    query_lower = query.lower()
    
    if not any(keyword in query_lower for keyword in sports_keywords):
        return {
            'query': query,
            'answer': "⚠️ Please ask questions related to sports, performance, recovery, or training.",
            'sources': []
        }
    
    # Check if the knowledge base is initialized
    if kb_data is None or vectorizer is None or index is None:
        logger.warning("Knowledge base not initialized, attempting to initialize now")
        initialize_kb()
    
    try:
        # Process the query
        query_vector = vectorizer.transform([query]).toarray().astype(np.float32)
        
        # Search the index
        D, I = index.search(query_vector, num_results)
        
        # Get the matching documents
        matches = [document_map[idx] for idx in I[0]]
        relevant_docs = kb_data.iloc[matches]
        
        # Generate the answer
        answer = generate_answer(query, relevant_docs)
        
        # Format the sources
        sources = []
        for _, doc in relevant_docs.iterrows():
            sources.append(f"{doc['title']} ({doc['source']})")
        
        return {
            'query': query,
            'answer': answer,
            'sources': sources
        }
    
    except Exception as e:
        logger.error(f"Error querying knowledge base: {e}")
        return {
            'query': query,
            'answer': "I'm sorry, I couldn't process your query due to an error.",
            'sources': []
        }

def generate_answer(query, relevant_docs):
    """
    Generate an answer based on the query and relevant documents.
    
    Args:
        query (str): The query string
        relevant_docs (pd.DataFrame): Relevant documents
        
    Returns:
        str: Generated answer
    """
    # In a real implementation, this would use an LLM to generate the answer
    # For this demo, we'll just combine information from the most relevant documents
    
    if relevant_docs.empty:
        return "I couldn't find any relevant information for your query."
    
    # Get the most relevant document
    most_relevant = relevant_docs.iloc[0]
    
    # Create a simple answer from the most relevant document content
    answer = most_relevant['content']
    
    # Add references to other relevant documents
    if len(relevant_docs) > 1:
        answer += "\n\nAdditional information:\n"
        for i in range(1, min(3, len(relevant_docs))):
            doc = relevant_docs.iloc[i]
            answer += f"\n- {doc['title']}: {doc['content'][:100]}..."
    
    return answer
