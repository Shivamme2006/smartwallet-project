from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATABASE_PATH = REPO_ROOT / "database" / "heart.db"


def run_query(query: str, database_path: Path | None = None) -> pd.DataFrame:
    db_path = database_path or DATABASE_PATH
    if not db_path.exists():
        raise FileNotFoundError(
            f"Database not found at '{db_path}'. Run 'python scripts/load_data.py' first."
        )

    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)


def get_patients_data(database_path: Path | None = None) -> pd.DataFrame:
    query = """
        SELECT
            age,
            sex,
            cp,
            trestbps,
            chol,
            fbs,
            restecg,
            thalach,
            exang,
            oldpeak,
            slope,
            ca,
            thal,
            target
        FROM patients
    """
    return run_query(query, database_path)


def get_age_distribution(database_path: Path | None = None) -> pd.DataFrame:
    query = """
        SELECT age, COUNT(*) AS total_patients
        FROM patients
        GROUP BY age
        ORDER BY age
    """
    return run_query(query, database_path)


def get_heart_disease_by_gender(database_path: Path | None = None) -> pd.DataFrame:
    query = """
        SELECT sex, COUNT(*) AS cases
        FROM patients
        WHERE target = 1
        GROUP BY sex
        ORDER BY sex
    """
    return run_query(query, database_path)


def get_average_cholesterol_by_age(database_path: Path | None = None) -> pd.DataFrame:
    query = """
        SELECT age, AVG(chol) AS avg_cholesterol
        FROM patients
        GROUP BY age
        ORDER BY age
    """
    return run_query(query, database_path)


if __name__ == "__main__":
    print("Age distribution")
    print(get_age_distribution().head())
    print("\nHeart disease by gender")
    print(get_heart_disease_by_gender().head())
    print("\nAverage cholesterol by age")
    print(get_average_cholesterol_by_age().head())
