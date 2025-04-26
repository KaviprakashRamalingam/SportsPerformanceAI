"""
Database module for the Sports Performance Analysis Assistant.

This module handles the database connection and operations for storing 
and retrieving athlete data, metrics, and analysis results.
"""

import os
import json
import pickle
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Initialize SQLAlchemy components
Base = declarative_base()
DATABASE_URL = os.environ.get('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Athlete(Base):
    """Athlete model for storing basic athlete information."""
    __tablename__ = 'athletes'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sport = Column(String(255))
    team = Column(String(255))
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    # Relationships
    performance_data = relationship("PerformanceData", back_populates="athlete", cascade="all, delete-orphan")
    form_analyses = relationship("FormAnalysis", back_populates="athlete", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Athlete(name='{self.name}', sport='{self.sport}')>"


class PerformanceData(Base):
    """Model for storing athlete performance metrics."""
    __tablename__ = 'performance_data'
    
    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    metric_name = Column(String(255), nullable=False)
    metric_value = Column(Float, nullable=False)
    notes = Column(Text)
    
    # Relationship
    athlete = relationship("Athlete", back_populates="performance_data")
    
    def __repr__(self):
        return f"<PerformanceData(athlete_id={self.athlete_id}, metric='{self.metric_name}', value={self.metric_value})>"


class FormAnalysis(Base):
    """Model for storing form analysis results from image or video processing."""
    __tablename__ = 'form_analyses'
    
    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer, ForeignKey('athletes.id'), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    exercise_type = Column(String(255))
    analysis_data = Column(Text)  # Stored as JSON string
    recommendations = Column(Text)  # Stored as JSON string
    
    # Relationship
    athlete = relationship("Athlete", back_populates="form_analyses")
    
    def __repr__(self):
        return f"<FormAnalysis(athlete_id={self.athlete_id}, exercise='{self.exercise_type}')>"


# Database functions

def init_db():
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(engine)
    print("Database initialized successfully.")


def get_or_create_athlete(name, sport=None, team=None, age=None):
    """
    Get an existing athlete or create a new one if they don't exist.
    
    Args:
        name (str): Athlete's name
        sport (str, optional): Athlete's sport
        team (str, optional): Athlete's team
        age (int, optional): Athlete's age
        
    Returns:
        Athlete: The athlete object
    """
    session = Session()
    athlete = session.query(Athlete).filter_by(name=name).first()
    
    if not athlete:
        athlete = Athlete(name=name, sport=sport, team=team, age=age)
        session.add(athlete)
        session.commit()
    
    session.close()
    return athlete


def save_performance_data(athlete_name, metric_name, metric_value, notes=None, date=None):
    """
    Save a performance metric for an athlete.
    
    Args:
        athlete_name (str): The name of the athlete
        metric_name (str): Name of the metric (e.g., "Sprint Speed", "Vertical Jump")
        metric_value (float): Value of the metric
        notes (str, optional): Additional notes about the metric
        date (datetime, optional): Date of the measurement, defaults to current time
        
    Returns:
        PerformanceData: The saved performance data object
    """
    session = Session()
    
    athlete = get_or_create_athlete(athlete_name)
    
    if not date:
        date = datetime.datetime.utcnow()
    
    perf_data = PerformanceData(
        athlete_id=athlete.id,
        date=date,
        metric_name=metric_name,
        metric_value=metric_value,
        notes=notes
    )
    
    session.add(perf_data)
    session.commit()
    session.close()
    
    return perf_data


def save_form_analysis(athlete_name, exercise_type, analysis_data, recommendations=None):
    """
    Save form analysis results for an athlete.
    
    Args:
        athlete_name (str): The name of the athlete
        exercise_type (str): Type of exercise analyzed (e.g., "Squat", "Deadlift")
        analysis_data (dict): Analysis results as a dictionary
        recommendations (dict, optional): Recommendations based on the analysis
        
    Returns:
        FormAnalysis: The saved form analysis object
    """
    session = Session()
    
    athlete = get_or_create_athlete(athlete_name)
    
    form_analysis = FormAnalysis(
        athlete_id=athlete.id,
        exercise_type=exercise_type,
        analysis_data=json.dumps(analysis_data),
        recommendations=json.dumps(recommendations) if recommendations else None
    )
    
    session.add(form_analysis)
    session.commit()
    session.close()
    
    return form_analysis


def get_athlete_performance_data(athlete_name):
    """
    Get all performance data for an athlete.
    
    Args:
        athlete_name (str): The name of the athlete
        
    Returns:
        pd.DataFrame: DataFrame containing all performance data for the athlete
    """
    session = Session()
    
    athlete = session.query(Athlete).filter_by(name=athlete_name).first()
    
    if not athlete:
        session.close()
        return pd.DataFrame()
    
    performance_data = session.query(PerformanceData).filter_by(athlete_id=athlete.id).all()
    
    data = []
    for perf_data in performance_data:
        data.append({
            'date': perf_data.date,
            'metric_name': perf_data.metric_name,
            'metric_value': perf_data.metric_value,
            'notes': perf_data.notes
        })
    
    session.close()
    
    if not data:
        return pd.DataFrame()
    
    df = pd.DataFrame(data)
    
    # Pivot the data to get metrics as columns
    if not df.empty:
        pivot_df = df.pivot_table(index='date', columns='metric_name', values='metric_value')
        pivot_df = pivot_df.reset_index()
        return pivot_df
    
    return df


def get_athlete_form_analyses(athlete_name):
    """
    Get all form analyses for an athlete.
    
    Args:
        athlete_name (str): The name of the athlete
        
    Returns:
        list: List of form analysis dictionaries
    """
    session = Session()
    
    athlete = session.query(Athlete).filter_by(name=athlete_name).first()
    
    if not athlete:
        session.close()
        return []
    
    form_analyses = session.query(FormAnalysis).filter_by(athlete_id=athlete.id).all()
    
    result = []
    for form_analysis in form_analyses:
        result.append({
            'id': form_analysis.id,
            'date': form_analysis.date,
            'exercise_type': form_analysis.exercise_type,
            'analysis_data': json.loads(form_analysis.analysis_data),
            'recommendations': json.loads(form_analysis.recommendations) if form_analysis.recommendations else None
        })
    
    session.close()
    return result


def get_all_athletes():
    """
    Get a list of all athletes in the database.
    
    Returns:
        list: List of athlete dictionaries with basic info
    """
    session = Session()
    
    athletes = session.query(Athlete).all()
    
    result = []
    for athlete in athletes:
        result.append({
            'id': athlete.id,
            'name': athlete.name,
            'sport': athlete.sport,
            'team': athlete.team,
            'age': athlete.age
        })
    
    session.close()
    return result


def delete_athlete(athlete_name):
    """
    Delete an athlete and all associated data.
    
    Args:
        athlete_name (str): The name of the athlete
        
    Returns:
        bool: True if successful, False otherwise
    """
    session = Session()
    
    athlete = session.query(Athlete).filter_by(name=athlete_name).first()
    
    if not athlete:
        session.close()
        return False
    
    session.delete(athlete)
    session.commit()
    session.close()
    
    return True


def store_dataframe(athlete_name, df, data_type="performance"):
    """
    Store a pandas DataFrame in the database for a specific athlete.
    
    Args:
        athlete_name (str): The name of the athlete
        df (pd.DataFrame): The DataFrame to store
        data_type (str): Type of data ("performance" or "form_analysis")
        
    Returns:
        bool: True if successful, False otherwise
    """
    if data_type == "performance":
        # Assumes DataFrame has columns for metrics and rows for dates/observations
        athlete = get_or_create_athlete(athlete_name)
        
        # Reset the index if 'date' is the index
        if df.index.name == 'date':
            df = df.reset_index()
        
        # Get all column names except non-metric columns
        non_metric_columns = ['Athlete', 'Date', 'Session', 'date']
        metric_columns = [col for col in df.columns if col not in non_metric_columns]
        
        # Process each row
        for _, row in df.iterrows():
            for metric in metric_columns:
                if pd.notna(row[metric]):  # Skip NaN values
                    try:
                        # Try to convert to float, skip if not possible
                        metric_value = float(row[metric])
                        
                        # Use Date column if available, otherwise current time
                        date_val = None
                        if 'Date' in row:
                            try:
                                # Try to parse the date
                                date_val = pd.to_datetime(row['Date'])
                            except:
                                date_val = datetime.datetime.utcnow()
                        else:
                            date_val = row.get('date', datetime.datetime.utcnow())
                        
                        save_performance_data(
                            athlete_name=athlete_name,
                            metric_name=metric,
                            metric_value=metric_value,
                            date=date_val
                        )
                    except (ValueError, TypeError):
                        # Skip non-numeric values
                        continue
        
        return True
    
    elif data_type == "form_analysis":
        # For form analysis, we expect a different structure
        # This would need to be implemented based on the specific format of form analysis data
        pass
    
    return False


def load_dataframe(athlete_name, data_type="performance"):
    """
    Load data for an athlete from the database into a DataFrame.
    
    Args:
        athlete_name (str): The name of the athlete
        data_type (str): Type of data ("performance" or "form_analysis")
        
    Returns:
        pd.DataFrame: The loaded DataFrame
    """
    if data_type == "performance":
        return get_athlete_performance_data(athlete_name)
    
    elif data_type == "form_analysis":
        # Convert form analysis data to DataFrame format
        form_analyses = get_athlete_form_analyses(athlete_name)
        if not form_analyses:
            return pd.DataFrame()
        
        # This will depend on how you want to structure form analysis data in a DataFrame
        df_data = []
        for analysis in form_analyses:
            row = {
                'date': analysis['date'],
                'exercise_type': analysis['exercise_type']
            }
            # Flatten analysis_data dictionary
            for key, value in analysis['analysis_data'].items():
                row[f'analysis_{key}'] = value
            
            # Add recommendations if available
            if analysis['recommendations']:
                for key, value in analysis['recommendations'].items():
                    row[f'rec_{key}'] = value
            
            df_data.append(row)
        
        return pd.DataFrame(df_data)
    
    return pd.DataFrame()


# Initialize database tables if they don't exist
init_db()