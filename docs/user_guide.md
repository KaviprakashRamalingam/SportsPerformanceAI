# Sports Performance Analysis Assistant - User Guide

## Introduction

The Sports Performance Analysis Assistant is a comprehensive tool designed to help coaches and athletes track performance, analyze athletic form, and generate personalized training recommendations. This guide will walk you through all the features and functionality of the application.

## Getting Started

### Installation and Setup

1. Ensure you have Python 3.8 or higher installed
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Configure your PostgreSQL database settings in environment variables
4. Start the application:
   ```
   streamlit run app.py
   ```

### Interface Overview

The application has a sidebar navigation menu with the following pages:
- **Home**: Overview of the application
- **Data Analysis**: Upload and analyze performance data
- **Form Analysis**: Upload images/videos for form assessment
- **Knowledge Base**: Ask sports science questions
- **Recommendations**: View personalized training recommendations
- **Database**: Manage athlete profiles and data

The global athlete selector in the sidebar allows you to set the active athlete that will be used across all tabs.

## Feature Guides

### Data Analysis

The Data Analysis tab allows you to upload, visualize, and analyze athlete performance data.

#### Uploading Data

1. Click on the "Upload Data" tab
2. Click "Browse files" to select a CSV file containing performance data
3. Your file should include the following columns:
   - Athlete: Name of the athlete
   - Date: Date of the performance recording
   - Various performance metrics (Strength, Speed, Endurance, etc.)

#### Analyzing Performance

Once data is uploaded:
1. Select an athlete from the dropdown
2. View key performance metrics at the top of the page
3. Explore visualizations in the tabs below:
   - **Radar Chart**: Shows overall performance across all metrics
   - **Trend Analysis**: Shows progress for a specific metric over time
   - **Comparison**: Compare metrics between two athletes

#### Saving to Database

To save the uploaded data to the database:
1. Click "Save Data to Database" after selecting an athlete
2. The data will be stored persistently and available in future sessions

### Form Analysis

The Form Analysis tab allows you to analyze an athlete's form from images or videos.

#### Uploading Media

1. Click "Browse files" to select an image or video file
2. Select the exercise type from the dropdown (Squat, Deadlift, etc.)
3. Click "Analyze Form" to process the media

#### Understanding Form Analysis

The form analysis results include:
1. **Posture Assessment**: Overall body alignment evaluation
2. **Joint Angles**: Measurements of key joints during the movement
3. **Symmetry Analysis**: Comparison of left and right side movement patterns
4. **Form Score**: Overall rating of technique quality

#### Using Form Recommendations

Based on the analysis, you'll receive:
1. **Form Correction Tips**: Specific adjustments to improve technique
2. **Exercise Recommendations**: Supplementary exercises to address weaknesses
3. **Visual Feedback**: Annotated image highlighting areas for improvement

### Knowledge Base

The Knowledge Base tab provides access to sports science information through a question-answering system.

#### Asking Questions

1. Type a sports-related question in the text box
2. Click "Ask Question" to submit
3. View the answer with supporting sources

#### Sample Questions

The interface provides sample questions in categories:
- Common Questions (recovery, sleep, training, etc.)
- Sports Injuries & Treatment (muscle cramps, sprains, etc.)

#### Follow-up Questions

After receiving an answer:
1. Click on any of the follow-up question buttons to explore related topics
2. Your conversation history is maintained throughout the session

### Recommendations

The Recommendations tab generates personalized training programs based on performance data and form analysis.

#### Viewing Recommendations

1. Select an athlete from the dropdown
2. View personalized recommendations in categories:
   - Strength Training
   - Speed Development
   - Endurance Training
   - Recovery Strategies
   - Form Improvement

#### Weekly Training Plan

Below the recommendations, you'll find:
1. A suggested weekly training schedule
2. Day-by-day workout focus areas
3. Training intensity guidelines

#### Exporting Recommendations

To save the recommendations:
1. Select your preferred export format (PDF, CSV, Text)
2. Click "Download Recommendations"
3. Save the file to your device

### Database Management

The Database tab allows you to manage athlete profiles and their data.

#### Adding Athletes

1. Enter the athlete's details in the form:
   - Name
   - Sport
   - Team
   - Age
2. Click "Add Athlete" to save to the database

#### Viewing Athletes

1. All athletes in the database are listed in a table
2. Click on an athlete to view their details and associated data

#### Editing and Deleting

1. To edit an athlete, select them and click "Edit"
2. To delete an athlete and all their data, click "Delete"

#### Data Export

To export all data for an athlete:
1. Select the athlete from the list
2. Click "Export Data"
3. Choose your preferred format

## Customization Options

### UI Customization

In the sidebar, under "UI Customization", you can:
1. Change the primary color theme
2. Adjust text size for better readability

### Database Settings

To toggle database functionality:
1. The database connection status is shown in the sidebar
2. When connected, all data is saved persistently
3. Without a database, data is stored in the session only

## Troubleshooting

### Common Issues

1. **Data Upload Error**: Ensure your CSV has the required columns (Athlete, Date, and metrics)
2. **Form Analysis Failure**: Check that the image is clear and the subject is fully visible
3. **Database Connection Issues**: Verify your environment variables are set correctly

### Getting Help

If you encounter issues not covered in this guide:
1. Check the console logs for specific error messages
2. Refer to the API documentation for detailed information
3. Contact support with details of the problem and steps to reproduce

## Best Practices

1. **Data Organization**: Use consistent naming and metrics in your CSV files
2. **Regular Updates**: Track performance data at consistent intervals for better trend analysis
3. **Image Quality**: For best form analysis results, use clear images with good lighting
4. **Database Backup**: Regularly export your data for backup purposes

## Conclusion

The Sports Performance Analysis Assistant provides a comprehensive set of tools for performance tracking, form analysis, and training optimization. By integrating data analysis with sports science knowledge, it helps coaches and athletes make informed decisions to improve performance and reduce injury risk.

For technical details about the application's functionality, please refer to the API Documentation.