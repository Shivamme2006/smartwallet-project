# Heart Disease Analytics Dashboard — Implementation Guide

## Objective

Build a full data analytics pipeline that analyzes heart disease data and displays interactive insights through a web interface.

The system must:

- Load a heart disease dataset
- Clean and validate the data
- Store the dataset in an SQLite database
- Perform SQL analytics queries
- Connect Tableau to the database
- Create visualizations in Tableau
- Publish a Tableau dashboard
- Embed the Tableau dashboard in a Flask web application

The goal is to transform raw medical data into interactive visual insights.

---

# Technology Stack

Python  
Pandas  
SQLite  
Tableau  
Flask  
HTML  

---

# System Workflow

CSV Dataset  
↓  
Python Data Cleaning  
↓  
SQLite Database  
↓  
SQL Queries  
↓  
Tableau Visualization  
↓  
Tableau Dashboard  
↓  
Flask Web Application  

---

# Project Directory Structure

The project must follow this structure.

```
heart-disease-analytics
│
├── data
│   └── heart.csv
│
├── database
│   └── heart.db
│
├── scripts
│   ├── data_cleaning.py
│   ├── load_data.py
│   └── queries.py
│
├── flask_app
│   ├── app.py
│   ├── templates
│   │   └── dashboard.html
│   └── static
│
├── requirements.txt
│
└── README.md
```

All paths should use **relative paths**.

---

# Dataset Specification

Place the dataset in:

```
data/heart.csv
```

Expected columns:

age – age of patient  
sex – gender  
cp – chest pain type  
trestbps – resting blood pressure  
chol – cholesterol level  
fbs – fasting blood sugar  
restecg – ECG results  
thalach – maximum heart rate achieved  
exang – exercise induced angina  
oldpeak – ST depression  
slope – slope of ST segment  
ca – number of vessels  
thal – thalassemia  
target – heart disease presence

Target values:

0 = No heart disease  
1 = Heart disease present

---

# Script: Data Cleaning

File location:

```
scripts/data_cleaning.py
```

Responsibilities:

- Load dataset using pandas
- Remove duplicate rows
- Handle missing values
- Ensure numeric data types are correct
- Validate numeric ranges
- Save cleaned dataset

Steps:

1. Read CSV dataset
2. Perform cleaning operations
3. Save cleaned dataset
4. Return cleaned dataframe

Libraries:

```
pandas
```

---

# Script: Load Data Into Database

File location:

```
scripts/load_data.py
```

Responsibilities:

- Load cleaned dataset
- Connect to SQLite database
- Create database if it does not exist
- Insert dataset into SQL table

Database location:

```
database/heart.db
```

Table name:

```
patients
```

Libraries:

```
pandas
sqlite3
```

Behavior:

- If table already exists, replace it.

---

# Script: SQL Queries

File location:

```
scripts/queries.py
```

Purpose:

Provide reusable SQL queries for analytics.

Example queries.

### Age Distribution

```sql
SELECT age, COUNT(*) AS total_patients
FROM patients
GROUP BY age;
```

### Heart Disease by Gender

```sql
SELECT sex, COUNT(*) AS cases
FROM patients
WHERE target = 1
GROUP BY sex;
```

### Average Cholesterol by Age

```sql
SELECT age, AVG(chol) AS avg_cholesterol
FROM patients
GROUP BY age;
```

Query results should be returned as **Pandas DataFrames**.

---

# Tableau Data Connection

Tableau must connect to the SQLite database.

Database type:

SQLite

Database file:

```
database/heart.db
```

Table:

```
patients
```

---

# Required Tableau Visualizations

## Visualization 1 — Age vs Heart Disease

Chart type: Bar chart

Fields:

age  
count(target)

Color by target.

---

## Visualization 2 — Cholesterol Distribution

Chart type: Histogram

Field:

chol

---

## Visualization 3 — Gender vs Heart Disease

Chart type: Stacked bar chart

Fields:

sex  
count(target)

---

## Visualization 4 — Blood Pressure vs Age

Chart type: Scatter plot

Fields:

age  
trestbps  

Color by target.

---

## Visualization 5 — Heart Rate vs Age

Chart type: Line chart

Fields:

age  
thalach

---

# Dashboard Requirements

Create a Tableau dashboard titled:

**Heart Disease Risk Analysis Dashboard**

Dashboard must contain:

- Age distribution chart
- Cholesterol histogram
- Gender comparison chart
- Blood pressure correlation
- Heart rate trend

Interactive filters:

Age  
Gender  
Cholesterol

---

# Publish Tableau Dashboard

Publish dashboard using Tableau Public.

Example URL:

```
https://public.tableau.com/views/heart-dashboard
```

This link will be embedded in the Flask application.

---

# Flask Web Application

File:

```
flask_app/app.py
```

Responsibilities:

- Start Flask server
- Create route for "/"
- Render HTML page
- Display Tableau dashboard

Use Flask and Jinja templates.

---

# HTML Dashboard Page

File location:

```
flask_app/templates/dashboard.html
```

The page must include:

- Project title
- Short description
- Embedded Tableau dashboard

Embed using iframe.

Example:

```html
<iframe
width="1000"
height="800"
src="TABLEAU_PUBLIC_URL">
</iframe>
```

Replace `TABLEAU_PUBLIC_URL` with your dashboard link.

---

# Running the Project

Install dependencies

```
pip install -r requirements.txt
```

Load dataset into database

```
python scripts/load_data.py
```

Start Flask server

```
python flask_app/app.py
```

Open browser

```
http://127.0.0.1:5000
```

The Tableau dashboard should appear inside the web page.

---

# Requirements File

Create:

```
requirements.txt
```

Contents:

```
pandas
flask
```

---

# Expected Output

The final system must provide:

- Structured SQLite database with heart disease data
- Tableau dashboard with interactive visualizations
- Flask web application embedding the dashboard
- Interactive filtering of heart disease risk factors

---

# Code Quality Requirements

Generated code must:

- Use modular Python scripts
- Follow Python best practices
- Use relative file paths
- Include comments
- Avoid hardcoded values
- Be easy to extend