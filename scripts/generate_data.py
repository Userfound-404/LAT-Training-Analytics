import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2024, 12, 31)
NUM_SIMULATORS = 12
NUM_INSTRUCTORS = 25
NUM_SESSIONS = 2500

print("Generating Aviation Training Analytics Data...")

# ============================================
# 1. SIMULATOR FLEET DATA
# ============================================
print("\n1. Generating simulator fleet data...")

aircraft_types = ['A320', 'A350', 'B737', 'B787', 'A380']
locations = ['Munich', 'Zurich', 'Vienna', 'Brussels', 'Frankfurt', 'Berlin']

simulators = []
for i in range(1, NUM_SIMULATORS + 1):
    simulators.append({
        'simulator_id': f'SIM-{i:03d}',
        'aircraft_type': random.choice(aircraft_types),
        'location': random.choice(locations),
        'acquisition_date': START_DATE - timedelta(days=random.randint(365, 1825)),
        'hourly_rate_eur': random.randint(400, 800),
        'max_hours_per_day': 20,
        'status': random.choices(['Active', 'Maintenance'], weights=[0.95, 0.05])[0]
    })

df_simulators = pd.DataFrame(simulators)
print(f"   ✓ Generated {len(df_simulators)} simulators")

# ============================================
# 2. INSTRUCTOR DATA
# ============================================
print("\n2. Generating instructor data...")

instructors = []
for i in range(1, NUM_INSTRUCTORS + 1):
    instructors.append({
        'instructor_id': f'INST-{i:03d}',
        'certification_level': random.choices(['Senior', 'Standard', 'Junior'], 
                                             weights=[0.2, 0.6, 0.2])[0],
        'aircraft_qualifications': ', '.join(random.sample(aircraft_types, 
                                            k=random.randint(1, 3))),
        'years_experience': random.randint(2, 25),
        'location': random.choice(locations),
        'max_sessions_per_week': random.randint(8, 15)
    })

df_instructors = pd.DataFrame(instructors)
print(f"   ✓ Generated {len(df_instructors)} instructors")

# ============================================
# 3. TRAINING SESSIONS DATA
# ============================================
print("\n3. Generating training sessions data...")

training_types = [
    'Type Rating', 
    'Recurrent Training', 
    'Line Training',
    'Initial Training',
    'Upgrade Training'
]

session_outcomes = ['Completed', 'Passed', 'Failed', 'Cancelled']

sessions = []
current_date = START_DATE

while len(sessions) < NUM_SESSIONS:
    # Select random simulator and instructor
    sim = df_simulators.sample(1).iloc[0]
    instructor = df_instructors[
        df_instructors['aircraft_qualifications'].str.contains(sim['aircraft_type'])
    ].sample(1).iloc[0] if len(df_instructors[
        df_instructors['aircraft_qualifications'].str.contains(sim['aircraft_type'])
    ]) > 0 else df_instructors.sample(1).iloc[0]
    
    # Generate session
    training_type = random.choice(training_types)
    duration_hours = round(random.uniform(2, 6), 1)
    
    # Realistic outcomes based on training type
    if training_type == 'Recurrent Training':
        outcome = random.choices(session_outcomes, weights=[0.05, 0.85, 0.05, 0.05])[0]
    else:
        outcome = random.choices(session_outcomes, weights=[0.1, 0.75, 0.1, 0.05])[0]
    
    sessions.append({
        'session_id': f'SESS-{len(sessions)+1:05d}',
        'date': current_date + timedelta(days=random.randint(0, (END_DATE - current_date).days)),
        'simulator_id': sim['simulator_id'],
        'instructor_id': instructor['instructor_id'],
        'student_id': f'STU-{random.randint(1000, 9999)}',
        'training_type': training_type,
        'scheduled_duration_hours': duration_hours,
        'actual_duration_hours': duration_hours + round(random.uniform(-0.5, 0.5), 1),
        'outcome': outcome,
        'student_satisfaction_score': random.randint(3, 5) if outcome in ['Completed', 'Passed'] else random.randint(2, 4)
    })

df_sessions = pd.DataFrame(sessions)
df_sessions['date'] = pd.to_datetime(df_sessions['date'])
df_sessions = df_sessions.sort_values('date').reset_index(drop=True)
print(f"   ✓ Generated {len(df_sessions)} training sessions")

# ============================================
# 4. SAVE RAW DATA
# ============================================
print("\n4. Saving raw data files...")

df_simulators.to_csv('data/raw/simulators.csv', index=False)
print("   ✓ Saved: data/raw/simulators.csv")

df_instructors.to_csv('data/raw/instructors.csv', index=False)
print("   ✓ Saved: data/raw/instructors.csv")

df_sessions.to_csv('data/raw/training_sessions.csv', index=False)
print("   ✓ Saved: data/raw/training_sessions.csv")

print("\n" + "="*50)
print("DATA GENERATION COMPLETE!")
print("="*50)
print(f"\nDatasets created:")
print(f"  • Simulators: {len(df_simulators)} records")
print(f"  • Instructors: {len(df_instructors)} records")
print(f"  • Training Sessions: {len(df_sessions)} records")
print(f"  • Date Range: {df_sessions['date'].min().date()} to {df_sessions['date'].max().date()}")

