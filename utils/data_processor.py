import pandas as pd
import numpy as np
from datetime import datetime

def process_performance_data(data, athlete):
    """
    Process performance data for a specific athlete.
    
    Args:
        data (pd.DataFrame): The performance data
        athlete (str): The name of the athlete to analyze
        
    Returns:
        dict: Processed analysis results
    """
    # Filter data for the selected athlete
    athlete_data = data[data['Athlete'] == athlete].copy()
    
    # Ensure date is in datetime format if it exists
    if 'Date' in athlete_data.columns:
        athlete_data['Date'] = pd.to_datetime(athlete_data['Date'], errors='coerce')
        athlete_data = athlete_data.sort_values('Date')
    
    # Calculate basic statistics for each metric
    metric_columns = [col for col in athlete_data.columns 
                     if col not in ['Athlete', 'Date', 'Session', 'Notes']]
    
    stats = {}
    for metric in metric_columns:
        metric_data = athlete_data[metric].dropna()
        if len(metric_data) > 0:
            stats[metric] = {
                'mean': metric_data.mean(),
                'median': metric_data.median(),
                'min': metric_data.min(),
                'max': metric_data.max(),
                'std': metric_data.std(),
                'recent': metric_data.iloc[-1] if len(metric_data) > 0 else None,
                'trend': calculate_trend(metric_data)
            }
    
    # Identify strengths and weaknesses
    strengths, weaknesses = identify_strengths_weaknesses(athlete_data, metric_columns)
    
    # Prepare the analysis results
    analysis_results = {
        'athlete': athlete,
        'metrics': stats,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'data_points': len(athlete_data),
        'date_range': (athlete_data['Date'].min(), athlete_data['Date'].max()) if 'Date' in athlete_data.columns else None
    }
    
    return analysis_results

def calculate_trend(data_series):
    """
    Calculate the trend direction for a series of values.
    
    Args:
        data_series (pd.Series): The data to analyze
        
    Returns:
        str: 'increasing', 'decreasing', or 'stable'
    """
    if len(data_series) < 2:
        return 'insufficient_data'
    
    # Simple linear regression to find the slope
    x = np.arange(len(data_series))
    y = data_series.values
    slope = np.polyfit(x, y, 1)[0]
    
    # Determine trend direction
    if abs(slope) < 0.01 * data_series.mean():  # Less than 1% change on average
        return 'stable'
    elif slope > 0:
        return 'increasing'
    else:
        return 'decreasing'

def identify_strengths_weaknesses(data, metrics):
    """
    Identify the athlete's strengths and weaknesses based on their metrics.
    
    Args:
        data (pd.DataFrame): The athlete's performance data
        metrics (list): List of metric columns
        
    Returns:
        tuple: Lists of strengths and weaknesses
    """
    strengths = []
    weaknesses = []
    
    # Calculate the mean for each metric
    means = {metric: data[metric].mean() for metric in metrics}
    
    # Calculate the standard deviation across all metrics
    all_values = np.concatenate([data[metric].values for metric in metrics])
    overall_std = np.std(all_values)
    
    # Normalize the metrics and identify outliers
    for metric in metrics:
        metric_mean = means[metric]
        metric_data = data[metric].dropna()
        
        if len(metric_data) > 0:
            recent_value = metric_data.iloc[-1]
            normalized_value = (recent_value - np.mean(all_values)) / overall_std
            
            if normalized_value > 0.75:  # More than 0.75 std above mean
                strengths.append(metric)
            elif normalized_value < -0.75:  # More than 0.75 std below mean
                weaknesses.append(metric)
    
    return strengths, weaknesses

def extract_key_metrics(data, athlete):
    """
    Extract key performance metrics for display.
    
    Args:
        data (pd.DataFrame): The performance data
        athlete (str): The name of the athlete
        
    Returns:
        dict: Key metrics and their values
    """
    # Filter data for the selected athlete
    athlete_data = data[data['Athlete'] == athlete].copy()
    
    # Get the metrics (excluding non-metric columns)
    metric_columns = [col for col in athlete_data.columns 
                     if col not in ['Athlete', 'Date', 'Session', 'Notes']]
    
    # Get the most recent values for each metric
    if 'Date' in athlete_data.columns:
        athlete_data['Date'] = pd.to_datetime(athlete_data['Date'], errors='coerce')
        most_recent = athlete_data.loc[athlete_data['Date'].idxmax()]
    else:
        most_recent = athlete_data.iloc[-1]
    
    # Extract the key metrics
    key_metrics = {}
    for metric in metric_columns:
        if metric in most_recent and not pd.isna(most_recent[metric]):
            key_metrics[metric] = most_recent[metric]
    
    return key_metrics
