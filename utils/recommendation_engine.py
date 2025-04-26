import pandas as pd
import numpy as np
import logging
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")  # Replace with your actual OpenAI API key

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_recommendations(performance_data=None, athlete=None, form_analysis=None):
    """
    Generate personalized training recommendations based on performance data and form analysis.
    
    Args:
        performance_data (pd.DataFrame, optional): Athlete performance data
        athlete (str, optional): Name of the athlete
        form_analysis (dict, optional): Results from form analysis
        
    Returns:
        dict: Personalized recommendations by category
    """
    recommendations = {
        "Strength Training": [],
        "Endurance Development": [],
        "Recovery Strategies": [],
        "Technique Improvements": [],
        "Nutrition Suggestions": []
    }
    
    try:
        # Generate recommendations based on performance data
        if performance_data is not None and athlete is not None:
            perf_recommendations = _generate_performance_recommendations(performance_data, athlete)
            for category, recs in perf_recommendations.items():
                if category in recommendations:
                    recommendations[category].extend(recs)
        
        # Generate recommendations based on form analysis
        if form_analysis is not None:
            form_recommendations = _generate_form_recommendations(form_analysis)
            for category, recs in form_recommendations.items():
                if category in recommendations:
                    recommendations[category].extend(recs)
        
        # If no data provided, return general recommendations
        if performance_data is None and form_analysis is None:
            recommendations = _generate_general_recommendations()
        
        return recommendations
    
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        # Return general recommendations in case of error
        return _generate_general_recommendations()

def _generate_performance_recommendations(data, athlete):
    """
    Generate recommendations based on performance data.
    
    Args:
        data (pd.DataFrame): Performance data
        athlete (str): Name of the athlete
        
    Returns:
        dict: Recommendations by category
    """
    # Filter data for the selected athlete
    athlete_data = data[data['Athlete'] == athlete].copy()
    
    # Get the metrics (excluding non-metric columns)
    metric_columns = [col for col in athlete_data.columns 
                     if col not in ['Athlete', 'Date', 'Session', 'Notes']]
    
    # Calculate statistics for each metric
    metric_stats = {}
    for metric in metric_columns:
        metric_data = athlete_data[metric].dropna()
        if len(metric_data) > 0:
            metric_stats[metric] = {
                'mean': metric_data.mean(),
                'std': metric_data.std(),
                'min': metric_data.min(),
                'max': metric_data.max(),
                'recent': metric_data.iloc[-1] if len(metric_data) > 0 else None,
                'trend': _calculate_trend(metric_data)
            }
    
    # Identify areas that need improvement
    improvements_needed = []
    for metric, stats in metric_stats.items():
        if stats['trend'] == 'decreasing' and metric not in ['Recovery Time', 'Fatigue Level']:
            improvements_needed.append(metric)
        elif stats['trend'] == 'increasing' and metric in ['Recovery Time', 'Fatigue Level']:
            improvements_needed.append(metric)
    
    # Identify strengths
    strengths = []
    for metric, stats in metric_stats.items():
        if stats['trend'] == 'increasing' and metric not in ['Recovery Time', 'Fatigue Level']:
            strengths.append(metric)
        elif stats['trend'] == 'decreasing' and metric in ['Recovery Time', 'Fatigue Level']:
            strengths.append(metric)
    
    # Generate recommendations based on the analysis
    recommendations = {
        "Strength Training": [],
        "Endurance Development": [],
        "Recovery Strategies": [],
        "Technique Improvements": [],
        "Nutrition Suggestions": []
    }
    
    # Strength training recommendations
    strength_metrics = ['Strength', 'Power', 'Max Lift', 'Squat', 'Bench Press', 'Deadlift']
    for metric in strength_metrics:
        if metric in improvements_needed:
            if metric == 'Strength' or metric == 'Power':
                recommendations["Strength Training"].append(f"Focus on progressive overload to improve {metric.lower()}")
                recommendations["Strength Training"].append(f"Add compound movements like squats and deadlifts to build overall {metric.lower()}")
            else:
                recommendations["Strength Training"].append(f"Implement specialized training program to improve {metric}")
                recommendations["Strength Training"].append(f"Consider periodization to break through {metric} plateau")
    
    # If no specific strength metrics found, add general strength recommendation
    if not recommendations["Strength Training"]:
        recommendations["Strength Training"].append("Maintain balanced strength training program with emphasis on sport-specific movements")
    
    # Endurance recommendations
    endurance_metrics = ['Endurance', 'VO2Max', 'Stamina', 'Distance', 'Time']
    for metric in endurance_metrics:
        if metric in improvements_needed:
            recommendations["Endurance Development"].append(f"Implement interval training to improve {metric.lower()}")
            recommendations["Endurance Development"].append(f"Gradually increase training volume to build {metric.lower()}")
    
    # If no specific endurance metrics found, add general endurance recommendation
    if not recommendations["Endurance Development"]:
        recommendations["Endurance Development"].append("Maintain current endurance training with focus on quality over quantity")
    
    # Recovery recommendations
    recovery_metrics = ['Recovery Time', 'Fatigue Level', 'Sleep Quality', 'Soreness']
    for metric in recovery_metrics:
        if metric in improvements_needed:
            if metric == 'Recovery Time' or metric == 'Fatigue Level':
                recommendations["Recovery Strategies"].append("Implement active recovery sessions to reduce fatigue")
                recommendations["Recovery Strategies"].append("Consider stress management techniques to improve recovery")
            elif metric == 'Sleep Quality':
                recommendations["Recovery Strategies"].append("Focus on sleep hygiene to improve recovery overnight")
                recommendations["Recovery Strategies"].append("Aim for 7-9 hours of quality sleep per night")
            else:
                recommendations["Recovery Strategies"].append("Incorporate foam rolling and stretching to reduce soreness")
    
    # If no specific recovery metrics found, add general recovery recommendation
    if not recommendations["Recovery Strategies"]:
        recommendations["Recovery Strategies"].append("Continue with current recovery protocols but monitor for signs of overtraining")
    
    # Nutrition suggestions (based on any available metrics)
    if 'Weight' in metric_stats or 'Body Fat' in metric_stats:
        recommendations["Nutrition Suggestions"].append("Maintain protein intake at 1.6-2.0g per kg of bodyweight")
        recommendations["Nutrition Suggestions"].append("Focus on nutrient timing: protein and carbs within 30-60 minutes after training")
    else:
        recommendations["Nutrition Suggestions"].append("Ensure adequate hydration before, during, and after training")
        recommendations["Nutrition Suggestions"].append("Consider personalized nutrition plan based on training goals")
    
    return recommendations

def _generate_form_recommendations(form_analysis):
    """
    Generate recommendations based on form analysis.
    
    Args:
        form_analysis (dict): Results from form analysis
        
    Returns:
        dict: Recommendations by category
    """
    recommendations = {
        "Technique Improvements": [],
        "Strength Training": [],
        "Recovery Strategies": []
    }
    
    # Check posture issues
    if "Posture" in form_analysis:
        posture_issues = []
        for insight in form_analysis["Posture"]:
            if "good" not in insight.lower() and "proper" not in insight.lower():
                posture_issues.append(insight)
        
        if posture_issues:
            recommendations["Technique Improvements"].append("Focus on maintaining neutral spine throughout exercise")
            recommendations["Technique Improvements"].append("Practice proper posture with lighter weights to build muscle memory")
            recommendations["Strength Training"].append("Strengthen core muscles to improve postural stability")
    
    # Check alignment issues
    if "Alignment" in form_analysis:
        alignment_issues = []
        for insight in form_analysis["Alignment"]:
            if "good" not in insight.lower() and "proper" not in insight.lower():
                alignment_issues.append(insight)
        
        if alignment_issues:
            recommendations["Technique Improvements"].append("Work on body alignment awareness with mirror feedback")
            recommendations["Strength Training"].append("Address muscle imbalances with unilateral exercises")
            recommendations["Recovery Strategies"].append("Use mobility work to improve range of motion and alignment")
    
    # Check balance issues
    if "Balance" in form_analysis:
        balance_issues = []
        for insight in form_analysis["Balance"]:
            if "good" not in insight.lower() and "proper" not in insight.lower():
                balance_issues.append(insight)
        
        if balance_issues:
            recommendations["Technique Improvements"].append("Practice stability exercises on unstable surfaces")
            recommendations["Strength Training"].append("Strengthen stabilizer muscles around problematic joints")
    
    # Check joint angle issues
    if "Joint Angles" in form_analysis:
        joint_issues = []
        for insight in form_analysis["Joint Angles"]:
            # Look for specific angle problems
            if "improve" in insight.lower() or "incorrect" in insight.lower():
                joint_issues.append(insight)
        
        if joint_issues:
            recommendations["Technique Improvements"].append("Focus on achieving proper joint angles through full range of motion")
            recommendations["Technique Improvements"].append("Consider video analysis to track joint angles during exercises")
            recommendations["Recovery Strategies"].append("Use targeted stretching to improve mobility in restricted joints")
    
    return recommendations

def _generate_general_recommendations():
    """
    Generate general training recommendations.
    
    Returns:
        dict: General recommendations by category
    """
    return {
        "Strength Training": [
            "Implement periodized training program with varied intensity and volume",
            "Focus on compound movements for overall strength development",
            "Include unilateral exercises to address muscle imbalances",
            "Add progressive overload by increasing weight 5-10% when current weight becomes manageable"
        ],
        "Endurance Development": [
            "Incorporate interval training 1-2 times per week",
            "Build aerobic base with zone 2 training (60-70% max heart rate)",
            "Implement tempo sessions at 75-85% max heart rate",
            "Gradually increase training volume no more than 10% per week"
        ],
        "Recovery Strategies": [
            "Ensure 7-9 hours of quality sleep per night",
            "Implement active recovery sessions between intense training days",
            "Use contrast therapy (alternating hot and cold) for enhanced recovery",
            "Schedule regular deload weeks every 4-6 weeks to prevent overtraining"
        ],
        "Technique Improvements": [
            "Regularly record and review exercise technique",
            "Focus on quality movement patterns rather than weight/reps",
            "Practice technique drills with light loads",
            "Consider working with a technique coach for specialized feedback"
        ],
        "Nutrition Suggestions": [
            "Maintain protein intake at 1.6-2.0g per kg of bodyweight",
            "Time carbohydrate intake around training sessions",
            "Stay hydrated with 30-40ml of water per kg of bodyweight daily",
            "Consider periodized nutrition approach aligned with training phases"
        ]
    }

def _calculate_trend(data_series):
    """
    Calculate the trend direction for a series of values.
    
    Args:
        data_series (pd.Series): The data to analyze
        
    Returns:
        str: 'increasing', 'decreasing', or 'stable'
    """
    if len(data_series) < 3:
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


def generate_recommendations_ai(performance_data=None, athlete=None, form_analysis=None):
    if performance_data is not None and athlete is not None:
        try:
            athlete_df = performance_data[performance_data['Athlete'] == athlete]
            
            if athlete_df.empty:
                return ["No performance data available for this athlete."]
            
            avg_scores = athlete_df[["Speed", "Agility", "Strength", "Endurance", "Flexibility"]].mean().to_dict()
            
            prompt = f"""
You are a professional sports coach.

Analyze the following performance metrics for an athlete:

- Speed: {avg_scores.get('Speed', 'N/A')}
- Agility: {avg_scores.get('Agility', 'N/A')}
- Strength: {avg_scores.get('Strength', 'N/A')}
- Endurance: {avg_scores.get('Endurance', 'N/A')}
- Flexibility: {avg_scores.get('Flexibility', 'N/A')}

Based on these scores:
- Identify weak areas.
- Suggest personalized training plans to improve.
- Focus on realistic, practical exercises.
- Keep it concise (4–5 action points).

If all scores are high, recommend maintenance tips.
"""

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )

            reply = response['choices'][0]['message']['content']
            return reply.strip().split('\n')
        
        except Exception as e:
            print(f"Error generating AI recommendations: {e}")
            return ["Could not generate personalized recommendations."]
    
    return ["No athlete selected or insufficient data."]
