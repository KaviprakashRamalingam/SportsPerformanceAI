# Sports Performance Analysis Assistant - Development Guide

## Getting Started with Development

This guide provides information for developers who want to extend or modify the Sports Performance Analysis Assistant. Follow these guidelines to ensure consistent development practices.

## Project Structure

```
sports-performance-assistant/
├── app.py                     # Main Streamlit application
├── README.md                  # Project overview
├── requirements.txt           # Dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── assets/                    # Static assets
├── data/                      # Data files
├── utils/                     # Utility modules
├── tests/                     # Test suite
└── docs/                      # Documentation
```

## Setting Up Development Environment

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sports-performance-assistant.git
   cd sports-performance-assistant
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install development dependencies:
   ```
   pip install pytest black flake8 sphinx
   ```

5. Set up the database:
   - Install PostgreSQL if not already installed
   - Create a database for development
   - Set environment variables with database credentials

## Development Workflow

### Code Style Guidelines

- Follow PEP 8 coding standards
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Use meaningful variable and function names

### Formatting Code

Run Black to format your code:

```
black .
```

### Linting

Run Flake8 to check your code for errors:

```
flake8 .
```

### Running Tests

Run the test suite:

```
pytest
```

Run tests with coverage:

```
pytest --cov=utils
```

### Adding New Features

1. Create a new branch for your feature:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature
3. Write tests for your new code
4. Update documentation
5. Submit a pull request

## Module-Specific Guidelines

### Data Processor Module

When extending the data processor:

1. Add new functions to `utils/data_processor.py`
2. Ensure functions are pure and return processed data rather than modifying in place
3. Add comprehensive error handling for different data formats
4. Write unit tests for each new function

Example:
```python
def calculate_advanced_metric(data, athlete, base_metrics):
    """
    Calculate an advanced performance metric from base metrics.
    
    Args:
        data (pd.DataFrame): Performance data
        athlete (str): Athlete name
        base_metrics (list): List of base metrics to use
        
    Returns:
        float: The calculated advanced metric
    """
    # Implementation
    pass
```

### Image Analyzer Module

When extending the image analyzer:

1. Add new functions to `utils/image_analyzer.py`
2. Keep computationally intensive operations optimized
3. Make sure functions work with various image formats and resolutions
4. Use optional parameters for fine-tuning

Example:
```python
def analyze_movement_pattern(frames, keypoints_sequence, pattern_type="running"):
    """
    Analyze a sequence of frames for a specific movement pattern.
    
    Args:
        frames (list): List of image frames
        keypoints_sequence (list): Sequence of keypoints
        pattern_type (str): Type of movement pattern
        
    Returns:
        dict: Analysis results
    """
    # Implementation
    pass
```

### Database Module

When extending the database module:

1. Add new models to `utils/database.py`
2. Follow SQLAlchemy best practices
3. Add appropriate indexes for performance
4. Ensure proper relationship cascades

Example:
```python
class TrainingPlan(Base):
    """Model for storing athlete training plans."""
    __tablename__ = 'training_plans'
    
    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    plan_data = Column(Text)  # JSON string
    
    athlete = relationship("Athlete", back_populates="training_plans")
```

### RAG System Module

When extending the RAG system:

1. Add new functions to `utils/rag_system.py`
2. Keep the knowledge base modular and extensible
3. Ensure proper vector embeddings for new content
4. Optimize for query performance

Example:
```python
def filter_knowledge_base(query, domain="general"):
    """
    Filter the knowledge base by domain before querying.
    
    Args:
        query (str): User query
        domain (str): Knowledge domain to filter by
        
    Returns:
        pd.DataFrame: Filtered knowledge base
    """
    # Implementation
    pass
```

## Streamlit UI Development

### Page Structure

When adding a new page to the application:

1. Add a new option to the sidebar navigation in `app.py`
2. Create a new section in the main conditional block
3. Follow the existing pattern for page organization

Example:
```python
elif page == "New Feature":
    st.title("New Feature")
    
    # Add feature description
    st.markdown("""
    This feature allows you to...
    """)
    
    # Add feature implementation
    # ...
```

### UI Components

Follow these guidelines for UI components:

1. Group related inputs in columns or expanders
2. Use consistent styling across the application
3. Add helpful descriptions with `st.markdown()` or tooltips
4. Keep the most important information at the top of the page
5. Use tabs to organize complex sections

Example:
```python
st.subheader("Feature Settings")
col1, col2 = st.columns(2)

with col1:
    param1 = st.slider("Parameter 1", 0, 100, 50)
    param2 = st.selectbox("Parameter 2", ["Option A", "Option B", "Option C"])

with col2:
    param3 = st.number_input("Parameter 3", 0.0, 1.0, 0.5)
    param4 = st.checkbox("Enable advanced options")
```

### State Management

Guidelines for Streamlit state management:

1. Use `st.session_state` for persistent state
2. Initialize all state variables at the start of the application
3. Use key parameters consistently
4. Use callbacks for complex state updates

Example:
```python
# Initialize state
if 'feature_settings' not in st.session_state:
    st.session_state.feature_settings = {
        'param1': 50,
        'param2': 'Option A'
    }

# Update state
def update_settings():
    st.session_state.feature_settings['param1'] = param1
    st.session_state.feature_settings['param2'] = param2

# UI with state
param1 = st.slider("Parameter 1", 0, 100, 
                  st.session_state.feature_settings['param1'],
                  key="param1_slider")
param2 = st.selectbox("Parameter 2", 
                     ["Option A", "Option B", "Option C"],
                     ["Option A", "Option B", "Option C"].index(st.session_state.feature_settings['param2']),
                     key="param2_select")

if st.button("Save Settings"):
    update_settings()
```

## Testing Guidelines

### Unit Tests

Write unit tests for individual functions:

1. Test both success and failure cases
2. Use fixtures for common test data
3. Mock external dependencies
4. Test edge cases

### Integration Tests

Write integration tests for workflows:

1. Test interactions between modules
2. Verify database operations
3. Test end-to-end functionality

### UI Tests

Consider UI tests using Streamlit's testing utilities:

1. Test UI component rendering
2. Test state management
3. Test user interactions

## Documentation Guidelines

### Function Docstrings

Follow this format for function docstrings:

```python
def function_name(param1, param2):
    """
    Short description of function.
    
    Longer description if needed.
    
    Args:
        param1 (type): Description of param1
        param2 (type): Description of param2
        
    Returns:
        type: Description of return value
        
    Raises:
        ExceptionType: When this exception is raised
    """
    # Function implementation
```

### Module Documentation

Add module-level docstrings:

```python
"""
Module Name

Description of the module's purpose and functionality.
"""
```

### Updating Documentation

When adding new features or making significant changes:

1. Update the API documentation
2. Update the user guide
3. Update README if necessary

## Performance Optimization

### Database Optimization

1. Use indexing for frequently queried fields
2. Use batch operations for bulk data
3. Minimize database round-trips

### Computation Optimization

1. Use vectorized operations with pandas and numpy
2. Cache results of expensive computations
3. Use async operations for slow I/O operations

### Streamlit-Specific Optimization

1. Use caching with `@st.cache_data` and `@st.cache_resource`
2. Avoid recomputing values when not needed
3. Use placeholders for progressive rendering
4. Consider pagination for large datasets

## Deployment

### Environment Variables

Use environment variables for configuration:

1. Database credentials
2. API keys
3. Feature flags
4. Environment-specific settings

### Docker Deployment

A Dockerfile is provided for containerized deployment:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```
docker build -t sports-performance-assistant .
docker run -p 8501:8501 sports-performance-assistant
```

### Cloud Deployment

Guidelines for deploying to cloud platforms:

1. Set up a PostgreSQL database service
2. Deploy the application to a container service
3. Configure environment variables
4. Set up monitoring and logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write or update tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.