# Heart Disease Analytics Dashboard

This project builds a local analytics pipeline for heart disease data and serves a self-contained Flask dashboard with charts rendered directly from SQLite data.

## Project structure

```text
heart-disease-analytics
|
+-- data
|   +-- heart.csv
|   +-- heart_cleaned.csv
|
+-- database
|   +-- heart.db
|
+-- scripts
|   +-- data_cleaning.py
|   +-- load_data.py
|   +-- queries.py
|
+-- flask_app
|   +-- app.py
|   +-- templates
|   |   +-- dashboard.html
|   +-- static
|
+-- requirements.txt
+-- README.md
```

## Dataset requirements

Place the raw dataset at `data/heart.csv`.
The repository currently includes a starter sample file there so the pipeline can run immediately; replace it with your real dataset when ready.

Expected columns:

- `age`
- `sex`
- `cp`
- `trestbps`
- `chol`
- `fbs`
- `restecg`
- `thalach`
- `exang`
- `oldpeak`
- `slope`
- `ca`
- `thal`
- `target`

The cleaning script:

- removes duplicate rows
- coerces required columns to numeric values
- drops rows with missing or invalid required values
- filters out invalid ranges for age, blood pressure, cholesterol, heart rate, and oldpeak
- enforces binary flags for `sex`, `fbs`, `exang`, and `target`

## Installation

```bash
pip install -r requirements.txt
```

## Load the dataset into SQLite

```bash
python scripts/load_data.py
```

This command cleans `data/heart.csv`, saves the result to `data/heart_cleaned.csv`, and replaces the `patients` table in `database/heart.db`.

## Run analytics queries

The reusable query helpers live in `scripts/queries.py` and return pandas DataFrames:

- `get_patients_data()`
- `get_age_distribution()`
- `get_heart_disease_by_gender()`
- `get_average_cholesterol_by_age()`

## Local dashboard

The Flask dashboard now renders local charts directly from the SQLite database. It includes:

- age vs heart disease
- cholesterol distribution
- gender vs heart disease
- blood pressure vs age
- heart rate vs age

Available filters on the page:

- minimum age
- maximum age
- gender
- maximum cholesterol

## Run the Flask app

```bash
python -m flask --app flask_app.app run --no-debugger --no-reload
```

Then open `http://127.0.0.1:5000`.
