# Data Dictionary

## 1. simulators.csv

| Column | Type | Description |
|--------|------|-------------|
| simulator_id | String | Unique identifier (e.g., SIM-001) |
| aircraft_type | String | Aircraft model (A320, A350, B737, B787, A380) |
| location | String | Training center location |
| acquisition_date | Date | Date simulator was acquired |
| hourly_rate_eur | Integer | Revenue rate in EUR per flight hour |
| max_hours_per_day | Integer | Maximum operational hours per day (typically 20) |
| status | String | Current status (Active, Maintenance) |

## 2. instructors.csv

| Column | Type | Description |
|--------|------|-------------|
| instructor_id | String | Unique identifier (e.g., INST-001) |
| certification_level | String | Seniority (Senior, Standard, Junior) |
| aircraft_qualifications | String | Comma-separated aircraft types certified for |
| years_experience | Integer | Years of instruction experience |
| location | String | Primary location |
| max_sessions_per_week | Integer | Maximum sessions instructor can teach |

## 3. training_sessions.csv

| Column | Type | Description |
|--------|------|-------------|
| session_id | String | Unique identifier (e.g., SESS-00001) |
| date | Date | Session date |
| simulator_id | String | Foreign key to simulators table |
| instructor_id | String | Foreign key to instructors table |
| student_id | String | Anonymized student identifier |
| training_type | String | Type of training (Type Rating, Recurrent, etc.) |
| scheduled_duration_hours | Float | Planned session duration |
| actual_duration_hours | Float | Actual session duration |
| outcome | String | Session result (Completed, Passed, Failed, Cancelled) |
| student_satisfaction_score | Integer | Rating 1-5 |

## Processed Tables

### simulator_utilization.csv
Monthly aggregation of simulator usage with utilization rate calculation.

### training_performance.csv
Training type performance metrics including pass rates and satisfaction.

### instructor_performance.csv
Instructor-level metrics with pass rates and session counts.

### location_performance.csv
Location-level revenue and operational metrics.

