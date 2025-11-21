import pandas as pd
import numpy as np
from datetime import datetime

print("="*60)
print("AVIATION TRAINING ANALYTICS - ETL PIPELINE")
print("="*60)

# ============================================
# EXTRACT
# ============================================
print("\n[EXTRACT] Loading raw data...")

df_simulators = pd.read_csv('data/raw/simulators.csv')
df_instructors = pd.read_csv('data/raw/instructors.csv')
df_sessions = pd.read_csv('data/raw/training_sessions.csv')

print(f"  ✓ Loaded {len(df_simulators)} simulators")
print(f"  ✓ Loaded {len(df_instructors)} instructors")
print(f"  ✓ Loaded {len(df_sessions)} sessions")

# ============================================
# TRANSFORM
# ============================================
print("\n[TRANSFORM] Processing and calculating metrics...")

# Convert dates
df_sessions['date'] = pd.to_datetime(df_sessions['date'])
df_simulators['acquisition_date'] = pd.to_datetime(df_simulators['acquisition_date'])

# Add time dimensions
df_sessions['year'] = df_sessions['date'].dt.year
df_sessions['month'] = df_sessions['date'].dt.month
df_sessions['month_name'] = df_sessions['date'].dt.strftime('%B')
df_sessions['quarter'] = df_sessions['date'].dt.quarter
df_sessions['day_of_week'] = df_sessions['date'].dt.day_name()

# Calculate revenue
df_sessions = df_sessions.merge(
    df_simulators[['simulator_id', 'hourly_rate_eur', 'aircraft_type', 'location']], 
    on='simulator_id', 
    how='left'
)
df_sessions['revenue_eur'] = df_sessions['actual_duration_hours'] * df_sessions['hourly_rate_eur']

print("  ✓ Added time dimensions")
print("  ✓ Calculated revenue")

# ============================================
# AGGREGATIONS FOR DASHBOARD
# ============================================
print("\n[TRANSFORM] Creating aggregated tables...")

# 1. Simulator Utilization Metrics
print("  → Calculating simulator utilization...")

# Available hours per month per simulator
days_per_month = 30
available_hours_per_month = 20 * days_per_month  # 20 hours per day

sim_utilization = df_sessions.groupby(['simulator_id', 'year', 'month']).agg({
    'actual_duration_hours': 'sum',
    'session_id': 'count'
}).reset_index()

sim_utilization.columns = ['simulator_id', 'year', 'month', 'total_hours_used', 'total_sessions']
sim_utilization['available_hours'] = available_hours_per_month
sim_utilization['utilization_rate'] = (sim_utilization['total_hours_used'] / sim_utilization['available_hours']) * 100

# Add simulator details
sim_utilization = sim_utilization.merge(
    df_simulators[['simulator_id', 'aircraft_type', 'location']], 
    on='simulator_id'
)

print(f"    ✓ Created utilization table: {len(sim_utilization)} records")

# 2. Training Performance Metrics
print("  → Calculating training performance...")

training_performance = df_sessions.groupby(['training_type', 'year', 'month']).agg({
    'session_id': 'count',
    'actual_duration_hours': 'sum',
    'student_satisfaction_score': 'mean',
    'revenue_eur': 'sum'
}).reset_index()

training_performance.columns = [
    'training_type', 'year', 'month', 
    'total_sessions', 'total_hours', 
    'avg_satisfaction', 'total_revenue'
]

# Calculate pass rates
outcome_stats = df_sessions.groupby(['training_type', 'year', 'month', 'outcome']).size().reset_index(name='count')
passed = outcome_stats[outcome_stats['outcome'] == 'Passed'].copy()
total = outcome_stats.groupby(['training_type', 'year', 'month'])['count'].sum().reset_index(name='total_sessions')

pass_rates = passed.merge(total, on=['training_type', 'year', 'month'])
pass_rates['pass_rate'] = (pass_rates['count'] / pass_rates['total_sessions']) * 100

training_performance = training_performance.merge(
    pass_rates[['training_type', 'year', 'month', 'pass_rate']], 
    on=['training_type', 'year', 'month'],
    how='left'
)

print(f"    ✓ Created performance table: {len(training_performance)} records")

# 3. Instructor Performance Metrics
print("  → Calculating instructor performance...")

instructor_performance = df_sessions.groupby('instructor_id').agg({
    'session_id': 'count',
    'actual_duration_hours': 'sum',
    'student_satisfaction_score': 'mean'
}).reset_index()

instructor_performance.columns = [
    'instructor_id', 'total_sessions', 
    'total_hours', 'avg_satisfaction'
]

# Add instructor details
instructor_performance = instructor_performance.merge(
    df_instructors[['instructor_id', 'certification_level', 'years_experience', 'location']], 
    on='instructor_id'
)

# Calculate pass rate per instructor
instructor_outcomes = df_sessions.groupby(['instructor_id', 'outcome']).size().reset_index(name='count')
instructor_passed = instructor_outcomes[instructor_outcomes['outcome'] == 'Passed'].copy()
instructor_total = instructor_outcomes.groupby('instructor_id')['count'].sum().reset_index(name='total')

instructor_pass_rates = instructor_passed.merge(instructor_total, on='instructor_id')
instructor_pass_rates['pass_rate'] = (instructor_pass_rates['count'] / instructor_pass_rates['total']) * 100

instructor_performance = instructor_performance.merge(
    instructor_pass_rates[['instructor_id', 'pass_rate']], 
    on='instructor_id',
    how='left'
)

print(f"    ✓ Created instructor table: {len(instructor_performance)} records")

# 4. Location Performance Summary
print("  → Calculating location performance...")

location_performance = df_sessions.groupby(['location', 'year', 'month']).agg({
    'session_id': 'count',
    'actual_duration_hours': 'sum',
    'revenue_eur': 'sum',
    'student_satisfaction_score': 'mean'
}).reset_index()

location_performance.columns = [
    'location', 'year', 'month',
    'total_sessions', 'total_hours', 
    'total_revenue', 'avg_satisfaction'
]

print(f"    ✓ Created location table: {len(location_performance)} records")

# ============================================
# LOAD
# ============================================
print("\n[LOAD] Saving processed data...")

# Save processed data
df_sessions.to_csv('data/processed/sessions_enriched.csv', index=False)
print("  ✓ Saved: sessions_enriched.csv")

sim_utilization.to_csv('data/processed/simulator_utilization.csv', index=False)
print("  ✓ Saved: simulator_utilization.csv")

training_performance.to_csv('data/processed/training_performance.csv', index=False)
print("  ✓ Saved: training_performance.csv")

instructor_performance.to_csv('data/processed/instructor_performance.csv', index=False)
print("  ✓ Saved: instructor_performance.csv")

location_performance.to_csv('data/processed/location_performance.csv', index=False)
print("  ✓ Saved: location_performance.csv")

# ============================================
# SUMMARY STATISTICS
# ============================================
print("\n" + "="*60)
print("ETL PIPELINE COMPLETE - KEY METRICS")
print("="*60)

print(f"\n📊 Overall Statistics (2024):")
print(f"  • Total Training Sessions: {len(df_sessions):,}")
print(f"  • Total Training Hours: {df_sessions['actual_duration_hours'].sum():,.1f}")
print(f"  • Total Revenue: €{df_sessions['revenue_eur'].sum():,.0f}")
print(f"  • Average Satisfaction Score: {df_sessions['student_satisfaction_score'].mean():.2f}/5")

print(f"\n🎯 Simulator Fleet Utilization:")
avg_utilization = sim_utilization['utilization_rate'].mean()
print(f"  • Average Utilization Rate: {avg_utilization:.1f}%")
print(f"  • Target Benchmark: 75-80%")
print(f"  • Status: {'✓ Above target' if avg_utilization >= 75 else '⚠ Below target'}")

print(f"\n📈 Training Success Rates:")
overall_passed = len(df_sessions[df_sessions['outcome'] == 'Passed'])
overall_total = len(df_sessions[df_sessions['outcome'].isin(['Passed', 'Failed'])])
overall_pass_rate = (overall_passed / overall_total * 100) if overall_total > 0 else 0
print(f"  • Overall Pass Rate: {overall_pass_rate:.1f}%")
print(f"  • Target Benchmark: >90%")
print(f"  • Status: {'✓ Above target' if overall_pass_rate >= 90 else '⚠ Below target'}")

print(f"\n👨‍🏫 Instructor Performance:")
print(f"  • Total Active Instructors: {len(instructor_performance)}")
print(f"  • Avg Sessions per Instructor: {instructor_performance['total_sessions'].mean():.1f}")
print(f"  • Top Performer: {instructor_performance.nlargest(1, 'pass_rate')['instructor_id'].values[0]} " +
      f"({instructor_performance.nlargest(1, 'pass_rate')['pass_rate'].values[0]:.1f}% pass rate)")

print("\n✅ All processed files ready for Power BI import!")
print("="*60)

