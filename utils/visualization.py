import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MaxNLocator

def create_performance_radar(data, athlete, figsize=(10, 8)):
    """
    Create a radar chart of the athlete's performance metrics.
    
    Args:
        data (pd.DataFrame): The performance data
        athlete (str): The name of the athlete
        figsize (tuple): Figure size (width, height)
        
    Returns:
        matplotlib.figure.Figure: The radar chart figure
    """
    # Filter data for the selected athlete
    athlete_data = data[data['Athlete'] == athlete].copy()
    
    # Get the most recent values for metrics
    if 'Date' in athlete_data.columns:
        athlete_data['Date'] = pd.to_datetime(athlete_data['Date'], errors='coerce')
        latest_date = athlete_data['Date'].max()
        latest_data = athlete_data[athlete_data['Date'] == latest_date].iloc[0]
    else:
        latest_data = athlete_data.iloc[-1]
    
    # Get the metrics (excluding non-metric columns)
    metrics = [col for col in athlete_data.columns 
              if col not in ['Athlete', 'Date', 'Session', 'Notes']]
    
    # Extract values for the metrics
    values = [latest_data[metric] for metric in metrics]
    
    # Normalize the values between 0 and 1 for the radar chart
    min_vals = athlete_data[metrics].min()
    max_vals = athlete_data[metrics].max()
    
    # Avoid division by zero
    ranges = max_vals - min_vals
    ranges = ranges.replace(0, 1)  # Replace zeros with ones to avoid division by zero
    
    normalized_values = [(latest_data[metric] - min_vals[metric]) / ranges[metric] for metric in metrics]
    
    # Create the radar chart
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, polar=True)
    
    # Set the angle of each metric
    angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
    angles += angles[:1]  # Close the loop
    
    # Add values
    normalized_values += normalized_values[:1]  # Close the loop
    
    # Plot the values
    ax.plot(angles, normalized_values, 'o-', linewidth=2)
    ax.fill(angles, normalized_values, alpha=0.25)
    
    # Set labels and title
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(metrics)
    plt.title(f'Performance Profile: {athlete}', size=15)
    
    return fig

def plot_trend_analysis(data, athlete, metric, figsize=(10, 6)):
    """
    Create a trend analysis plot for a specific metric.
    
    Args:
        data (pd.DataFrame): The performance data
        athlete (str): The name of the athlete
        metric (str): The metric to plot
        figsize (tuple): Figure size (width, height)
        
    Returns:
        matplotlib.figure.Figure: The trend analysis figure
    """
    # Filter data for the selected athlete
    athlete_data = data[data['Athlete'] == athlete].copy()
    
    # Sort by date if available
    if 'Date' in athlete_data.columns:
        athlete_data['Date'] = pd.to_datetime(athlete_data['Date'], errors='coerce')
        athlete_data = athlete_data.sort_values('Date')
        x_values = athlete_data['Date']
        x_label = 'Date'
    else:
        x_values = range(len(athlete_data))
        x_label = 'Session'
    
    # Extract the metric values
    y_values = athlete_data[metric]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the metric values
    ax.plot(x_values, y_values, 'o-', linewidth=2)
    
    # Add a trendline
    if len(y_values) > 1:
        # For date x-axis, convert to numeric for regression
        if 'Date' in athlete_data.columns:
            x_numeric = np.arange(len(x_values))
            z = np.polyfit(x_numeric, y_values, 1)
            p = np.poly1d(z)
            ax.plot(x_values, p(x_numeric), "r--", alpha=0.8, linewidth=1)
        else:
            z = np.polyfit(x_values, y_values, 1)
            p = np.poly1d(z)
            ax.plot(x_values, p(x_values), "r--", alpha=0.8, linewidth=1)
    
    # Set labels and title
    ax.set_xlabel(x_label)
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} Trend for {athlete}')
    
    # Format the plot
    if 'Date' not in athlete_data.columns:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    
    ax.grid(True, linestyle='--', alpha=0.7)
    
    return fig

def plot_comparison(data, athlete1, athlete2, figsize=(12, 8)):
    """
    Create a comparison plot between two athletes.
    
    Args:
        data (pd.DataFrame): The performance data
        athlete1 (str): The name of the first athlete
        athlete2 (str): The name of the second athlete
        figsize (tuple): Figure size (width, height)
        
    Returns:
        matplotlib.figure.Figure: The comparison figure
    """
    # Filter data for both athletes
    athlete1_data = data[data['Athlete'] == athlete1]
    athlete2_data = data[data['Athlete'] == athlete2]
    
    # Get metrics (excluding non-metric columns)
    metrics = [col for col in data.columns 
              if col not in ['Athlete', 'Date', 'Session', 'Notes']]
    
    # Calculate mean values for each metric for both athletes
    athlete1_means = [athlete1_data[metric].mean() for metric in metrics]
    athlete2_means = [athlete2_data[metric].mean() for metric in metrics]
    
    # Create the comparison chart
    fig, ax = plt.subplots(figsize=figsize)
    
    # Set up bar positions
    x = np.arange(len(metrics))
    width = 0.35
    
    # Create the bars
    rects1 = ax.bar(x - width/2, athlete1_means, width, label=athlete1)
    rects2 = ax.bar(x + width/2, athlete2_means, width, label=athlete2)
    
    # Add labels and title
    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    ax.set_title(f'Performance Comparison: {athlete1} vs {athlete2}')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, rotation=45, ha='right')
    ax.legend()
    
    # Adjust layout
    fig.tight_layout()
    
    return fig
