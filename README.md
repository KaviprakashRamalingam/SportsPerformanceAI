# Sports Performance Analysis Assistant

An advanced analytics tool that helps coaches and athletes track performance, analyze form, and generate personalized training recommendations using AI.

![Application Screenshot](assets/app_screenshot.png)

## Features

- **Performance Data Analysis**: Track and visualize key performance metrics over time
- **Form Analysis**: Analyze athletic form from images/videos using computer vision
- **Knowledge Base**: Access sports science information through a RAG-based Q&A system
- **Personalized Recommendations**: Generate tailored training programs based on individual data
- **Database Integration**: Store and retrieve athlete data persistently

## Demo

https://sportsperformance.streamlit.app/

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Internet connection for RAG knowledge retrieval
- OpenAI API key
- Streamlit cloud (for hosting)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/sports-performance-assistant.git
   cd sports-performance-assistant
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure PostgreSQL:
   - Set up a PostgreSQL database
   - Set the following environment variables:
     - `DATABASE_URL`: Complete connection string
     - `PGUSER`: Database username
     - `PGPASSWORD`: Database password
     - `PGHOST`: Database host
     - `PGPORT`: Database port
     - `PGDATABASE`: Database name

4. Start the application:
   ```
   streamlit run app.py
   ```

## Usage Guide

### Data Analysis

Upload CSV files with performance metrics to:
- Visualize performance across different metrics
- Identify strengths and weaknesses
- Track progress over time
- Compare athletes

### Form Analysis

Upload images or videos of athletes to:
- Analyze posture and technique
- Identify form issues
- Get recommendations for improvement
- Track form progress over time

### Knowledge Base

Use the Q&A interface to:
- Ask questions about sports science topics
- Get evidence-based answers
- Learn about training methodologies
- Access injury prevention information

### Recommendations

Generate personalized recommendations:
- Strength training programs
- Speed and endurance development
- Recovery strategies
- Form improvement exercises

## Architecture

The Sports Performance Analysis Assistant uses a modular architecture:

- **Frontend**: Streamlit web interface
- **Backend Services**:
  - Data Processing Module
  - Image Analysis Engine
  - RAG Knowledge System
  - Recommendation Engine
  - FAISS
- **Database**: PostgreSQL for persistent storage

For more details, see the [Architecture Documentation](docs/architecture.md).

## Development

### Project Structure

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

### Running Tests

Execute the test suite:

```
pytest
```

For test coverage:

```
pytest --cov=utils
```

### Documentation

- [User Guide](docs/user_guide.md): Detailed usage instructions
- [API Documentation](docs/api_documentation.md): Technical reference
- [Development Guide](docs/development_guide.md): Guide for contributors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Sports science data sourced from peer-reviewed research
- Built with Streamlit, scikit-learn, OpenCV, and PostgreSQL
- Special thanks to contributors and testers
