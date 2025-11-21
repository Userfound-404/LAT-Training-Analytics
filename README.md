# Aviation Training Performance Analytics

**Project for:** Lufthansa Aviation Training - Data & Analytics Role  
**Author:** Sneha  
**Date:** November 2025  
**Tech Stack:** Python, Pandas, Power BI

## 📋 Project Overview

This project demonstrates end-to-end data analytics for flight simulator training operations, including:
- Synthetic data generation for realistic aviation training scenarios
- ETL pipeline with data transformations and KPI calculations
- Interactive Power BI dashboard for performance monitoring

**Business Context:** Flight simulator utilization and training efficiency are critical KPIs for aviation training organizations. This analysis tracks simulator performance, instructor effectiveness, and training outcomes across multiple locations.

## 🎯 Key Performance Indicators (KPIs)

1. **Simulator Utilization Rate:** (Used Hours / Available Hours) × 100  
   *Target: 75-80%*

2. **Training Pass Rate:** (Passed Sessions / Total Sessions) × 100  
   *Target: >90%*

3. **Revenue Per Flight Hour (RPFH):** Total Revenue / Total Hours

4. **Student Satisfaction Score:** Average rating (1-5 scale)

5. **Instructor Efficiency:** Sessions per instructor, pass rates

## 📁 Project Structure

LAT_Training_Analytics/
├── data/
│   ├── raw/
│   │   ├── simulators.csv
│   │   ├── instructors.csv
│   │   └── training_sessions.csv
│   └── processed/
│       ├── sessions_enriched.csv
│       ├── simulator_utilization.csv
│       ├── training_performance.csv
│       ├── instructor_performance.csv
│       └── location_performance.csv
├── scripts/
│   ├── generate_data.py
│   └── etl_pipeline.py
├── docs/
│   └── data_dictionary.md
└── README.md

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- Power BI Desktop (for Mac: use Windows VM or Power BI Service)

### Step 1: Generate Data
python scripts/generate_data.py

### Step 2: Run ETL Pipeline
python scripts/etl_pipeline.py


### Step 3: Import to Power BI
1. Open Power BI Desktop
2. Get Data → Text/CSV
3. Import all files from `data/processed/`
4. Create relationships between tables
5. Build visualizations

## 📊 Dashboard Components

### Page 1: Executive Overview
- Total sessions, hours, revenue (KPI cards)
- Utilization rate gauge
- Monthly trend line charts
- Location comparison bar chart

### Page 2: Simulator Performance
- Utilization heatmap by simulator and month
- Aircraft type performance comparison
- Peak usage time analysis

### Page 3: Training Quality
- Pass rate by training type
- Student satisfaction trends
- Instructor performance leaderboard

## 🔍 Key Insights

- Average simulator utilization: 67% (below 75% target)
- Recurrent training has highest pass rate: 94%
- Munich location generates 35% of total revenue

## 🛠️ Technical Implementation

### ETL Pipeline
- **Extract:** Load CSV files from raw data folder
- **Transform:** 
  - Add time dimensions (year, month, quarter)
  - Calculate KPIs and aggregations
  - Join tables for enriched datasets
- **Load:** Save processed data for BI consumption

### Data Quality
- Date range: January 1 - December 31, 2024
- 12 simulators across 6 locations
- 25 instructors with varied qualifications
- 2,500 training sessions

## 📈 Future Enhancements

- Integrate with Databricks for real-time processing
- Add predictive maintenance models
- Implement demand forecasting
- Create automated alerting for KPI thresholds

## 📧 Contact

Sneha Pulikonda    
https://www.linkedin.com/in/sneha-pulikonda/
---

**Note:** This is a demonstration project with synthetic data created for portfolio purposes.


