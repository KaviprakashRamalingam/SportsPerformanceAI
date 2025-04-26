# Sports Performance Analysis Assistant - API Documentation

## Overview

This document provides detailed technical information about the internal modules and functions of the Sports Performance Analysis Assistant. It's intended for developers who want to understand, extend, or modify the application's functionality.

## Module: `utils.data_processor`

### Functions

#### `process_performance_data(data, athlete)`

Processes performance data for a specific athlete.

**Parameters:**
- `data` (pd.DataFrame): Performance data
- `athlete` (str): Name of the athlete to analyze

**Returns:**
- `dict`: Analysis results containing strengths, weaknesses, trends, and average metrics

**Example:**
```python
results = process_performance_data(performance_df, "John Doe")
print(results["strengths"])  # List of strengths
```

#### `calculate_trend(data_series)`

Calculates the trend direction for a series of values.

**Parameters:**
- `data_series` (pd.Series): The data to analyze

**Returns:**
- `str`: 'increasing', 'decreasing', or 'stable'

#### `identify_strengths_weaknesses(data, metrics)`

Identifies the athlete's strengths and weaknesses based on their metrics.

**Parameters:**
- `data` (pd.DataFrame): The athlete's performance data
- `metrics` (list): List of metric columns

**Returns:**
- `tuple`: Lists of strengths and weaknesses

#### `extract_key_metrics(data, athlete)`

Extracts key performance metrics for display.

**Parameters:**
- `data` (pd.DataFrame): The performance data
- `athlete` (str): The name of the athlete

**Returns:**
- `dict`: Key metrics and their values

## Module: `utils.database`

### Classes

#### `Athlete`

Model for storing basic athlete information.

**Attributes:**
- `id` (Integer): Primary key
- `name` (String): Athlete's name (unique)
- `sport` (String): Athlete's sport
- `team` (String): Athlete's team
- `age` (Integer): Athlete's age
- `created_at` (DateTime): Creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `performance_data` (Relationship): Related performance data
- `form_analyses` (Relationship): Related form analyses

#### `PerformanceData`

Model for storing athlete performance metrics.

**Attributes:**
- `id` (Integer): Primary key
- `athlete_id` (Integer): Foreign key to Athlete
- `date` (DateTime): Date of the measurement
- `metric_name` (String): Name of the metric
- `metric_value` (Float): Value of the metric
- `notes` (Text): Additional notes

#### `FormAnalysis`

Model for storing form analysis results.

**Attributes:**
- `id` (Integer): Primary key
- `athlete_id` (Integer): Foreign key to Athlete
- `date` (DateTime): Date of the analysis
- `exercise_type` (String): Type of exercise analyzed
- `analysis_data` (Text): Analysis results as JSON
- `recommendations` (Text): Recommendations as JSON

### Functions

#### `init_db()`

Initializes the database by creating all tables.

#### `get_or_create_athlete(name, sport=None, team=None, age=None)`

Gets an existing athlete or creates a new one.

**Parameters:**
- `name` (str): Athlete's name
- `sport` (str, optional): Athlete's sport
- `team` (str, optional): Athlete's team
- `age` (int, optional): Athlete's age

**Returns:**
- `Athlete`: The athlete object

#### `save_performance_data(athlete_name, metric_name, metric_value, notes=None, date=None)`

Saves a performance metric for an athlete.

**Parameters:**
- `athlete_name` (str): The name of the athlete
- `metric_name` (str): Name of the metric
- `metric_value` (float): Value of the metric
- `notes` (str, optional): Additional notes
- `date` (datetime, optional): Date of the measurement

**Returns:**
- `PerformanceData`: The saved performance data object

#### `save_form_analysis(athlete_name, exercise_type, analysis_data, recommendations=None)`

Saves form analysis results for an athlete.

**Parameters:**
- `athlete_name` (str): The name of the athlete
- `exercise_type` (str): Type of exercise analyzed
- `analysis_data` (dict): Analysis results
- `recommendations` (dict, optional): Recommendations

**Returns:**
- `FormAnalysis`: The saved form analysis object

#### `get_athlete_performance_data(athlete_name)`

Gets all performance data for an athlete.

**Parameters:**
- `athlete_name` (str): The name of the athlete

**Returns:**
- `pd.DataFrame`: DataFrame with performance data

#### `get_athlete_form_analyses(athlete_name)`

Gets all form analyses for an athlete.

**Parameters:**
- `athlete_name` (str): The name of the athlete

**Returns:**
- `list`: List of form analysis dictionaries

#### `get_all_athletes()`

Gets a list of all athletes in the database.

**Returns:**
- `list`: List of athlete dictionaries

#### `delete_athlete(athlete_name)`

Deletes an athlete and all associated data.

**Parameters:**
- `athlete_name` (str): The name of the athlete

**Returns:**
- `bool`: True if successful

#### `store_dataframe(athlete_name, df, data_type="performance")`

Stores a pandas DataFrame in the database.

**Parameters:**
- `athlete_name` (str): The name of the athlete
- `df` (pd.DataFrame): The DataFrame to store
- `data_type` (str): "performance" or "form_analysis"

**Returns:**
- `bool`: True if successful

#### `load_dataframe(athlete_name, data_type="performance")`

Loads data for an athlete from the database.

**Parameters:**
- `athlete_name` (str): The name of the athlete
- `data_type` (str): "performance" or "form_analysis"

**Returns:**
- `pd.DataFrame`: The loaded DataFrame

## Module: `utils.image_analyzer`

### Functions

#### `analyze_form(image)`

Analyzes athlete form from an image.

**Parameters:**
- `image` (numpy.ndarray): The image to analyze

**Returns:**
- `tuple`: (form_analysis_results, annotated_image)

#### `analyze_keypoints(keypoints, image_shape)`

Analyzes keypoints to determine form quality.

**Parameters:**
- `keypoints` (dict): Dictionary of keypoints
- `image_shape` (tuple): Shape of the image

**Returns:**
- `dict`: Form analysis results

#### `calculate_angle(point1, point2, point3=None, vertical=False)`

Calculates the angle between three points or between a line and the vertical.

**Parameters:**
- `point1` (tuple): First point (x, y)
- `point2` (tuple): Second point (x, y)
- `point3` (tuple, optional): Third point (x, y)
- `vertical` (bool): Whether to calculate angle with vertical line

**Returns:**
- `float`: Angle in degrees

#### `detect_pose(frame)`

Detects human pose in a video frame.

**Parameters:**
- `frame` (numpy.ndarray): The video frame

**Returns:**
- `dict`: Detected pose keypoints

## Module: `utils.rag_system`

### Functions

#### `initialize_kb()`

Initializes the knowledge base by loading data and creating vector embeddings.

#### `query_knowledge_base(query, num_results=5)`

Queries the knowledge base for relevant information.

**Parameters:**
- `query` (str): The query string
- `num_results` (int): Number of results to return

**Returns:**
- `dict`: Query response with answer and sources

#### `generate_answer(query, relevant_docs)`

Generates an answer based on the query and relevant documents.

**Parameters:**
- `query` (str): The query string
- `relevant_docs` (pd.DataFrame): Relevant documents

**Returns:**
- `str`: Generated answer

## Module: `utils.recommendation_engine`

### Functions

#### `generate_recommendations(performance_data=None, athlete=None, form_analysis=None)`

Generates personalized training recommendations.

**Parameters:**
- `performance_data` (pd.DataFrame, optional): Athlete performance data
- `athlete` (str, optional): Name of the athlete
- `form_analysis` (dict, optional): Results from form analysis

**Returns:**
- `dict`: Personalized recommendations by category

#### `_generate_performance_recommendations(data, athlete)`

Generates recommendations based on performance data.

**Parameters:**
- `data` (pd.DataFrame): Performance data
- `athlete` (str): Name of the athlete

**Returns:**
- `dict`: Recommendations by category

#### `_generate_form_recommendations(form_analysis)`

Generates recommendations based on form analysis.

**Parameters:**
- `form_analysis` (dict): Results from form analysis

**Returns:**
- `dict`: Recommendations by category

#### `_generate_general_recommendations()`

Generates general training recommendations.

**Returns:**
- `dict`: General recommendations by category

#### `_calculate_trend(data_series)`

Calculates the trend direction for a series of values.

**Parameters:**
- `data_series` (pd.Series): The data to analyze

**Returns:**
- `str`: 'increasing', 'decreasing', or 'stable'

## Module: `utils.visualization`

### Functions

#### `create_performance_radar(data, athlete, figsize=(10, 8))`

Creates a radar chart of the athlete's performance metrics.

**Parameters:**
- `data` (pd.DataFrame): The performance data
- `athlete` (str): The name of the athlete
- `figsize` (tuple): Figure size (width, height)

**Returns:**
- `matplotlib.figure.Figure`: The radar chart figure

#### `plot_trend_analysis(data, athlete, metric, figsize=(10, 6))`

Creates a trend analysis plot for a specific metric.

**Parameters:**
- `data` (pd.DataFrame): The performance data
- `athlete` (str): The name of the athlete
- `metric` (str): The metric to plot
- `figsize` (tuple): Figure size (width, height)

**Returns:**
- `matplotlib.figure.Figure`: The trend analysis figure

#### `plot_comparison(data, athlete1, athlete2, figsize=(12, 8))`

Creates a comparison plot between two athletes.

**Parameters:**
- `data` (pd.DataFrame): The performance data
- `athlete1` (str): The name of the first athlete
- `athlete2` (str): The name of the second athlete
- `figsize` (tuple): Figure size (width, height)

**Returns:**
- `matplotlib.figure.Figure`: The comparison figure

## Application Flow

### Data Loading and Processing

1. User uploads CSV data or loads from database
2. `process_performance_data()` analyzes the metrics
3. `extract_key_metrics()` identifies key values for display
4. Visualization functions generate plots

### Form Analysis

1. User uploads image or video
2. `detect_pose()` identifies key body points
3. `analyze_keypoints()` evaluates form quality
4. `analyze_form()` generates overall assessment

### Knowledge Base Queries

1. User submits a question
2. Query is processed to find relevant documents
3. `generate_answer()` creates a response using retrieved information

### Recommendation Generation

1. Performance data and form analysis are combined
2. `generate_recommendations()` creates personalized training advice
3. Recommendations are categorized by training focus

## Database Schema

The database schema includes three main tables:

1. **athletes**
   - Primary key: id
   - Unique constraint: name

2. **performance_data**
   - Primary key: id
   - Foreign key: athlete_id references athletes(id)
   - Indexes: athlete_id, date

3. **form_analyses**
   - Primary key: id
   - Foreign key: athlete_id references athletes(id)
   - Indexes: athlete_id, date

## Error Handling

All database operations include error handling to prevent crashes:
- Data validation before saving
- Try/except blocks for database operations
- Graceful fallbacks when data is unavailable

## Extending the Application

### Adding New Metrics

To add new performance metrics:
1. Include the new metrics in your CSV data
2. They will automatically be included in data processing
3. Update visualization functions if needed

### Adding New Analysis Features

To add new form analysis features:
1. Extend the `analyze_keypoints()` function
2. Add new analysis logic
3. Update the recommendation generation to use the new features

### Customizing the Knowledge Base

To update the knowledge base:
1. Add new entries to the kb_sports_science.csv file
2. Run the embedding generation script
3. Reinitialize the knowledge base with `initialize_kb()`