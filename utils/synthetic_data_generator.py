import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker()

def generate_synthetic_athlete_data(num_athletes=10, sessions_per_athlete=5):
    athletes = []
    
    sports_list = [
        "Soccer", "Basketball", "Tennis", "Running", "Swimming", "Cycling", "Gymnastics", "Rowing"
    ]
    
    performance_metrics = [
        "Speed", "Agility", "Strength", "Endurance", "Flexibility"
    ]
    
    data = []

    for _ in range(num_athletes):
        athlete_name = fake.name()
        sport = random.choice(sports_list)
        
        for session in range(sessions_per_athlete):
            session_date = fake.date_between(start_date='-1y', end_date='today')
            session_data = {
                "Athlete": athlete_name,
                "Sport": sport,
                "Date": session_date,
                "Session": f"Session {session+1}"
            }
            for metric in performance_metrics:
                session_data[metric] = round(np.random.uniform(50, 100), 2)  # Random realistic scores
            
            data.append(session_data)

    df = pd.DataFrame(data)
    return df

def save_synthetic_data(filepath="data/synthetic_performance_data.csv"):
    df = generate_synthetic_athlete_data()
    df.to_csv(filepath, index=False)
    print(f"Synthetic data saved to {filepath}")

if __name__ == "__main__":
    save_synthetic_data()
