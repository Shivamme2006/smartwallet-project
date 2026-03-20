from __future__ import annotations

import sqlite3
from pathlib import Path

from data_cleaning import clean_heart_data


REPO_ROOT = Path(__file__).resolve().parents[1]
DATABASE_DIR = REPO_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "heart.db"
TABLE_NAME = "patients"


def load_clean_data_to_database(database_path: Path | None = None) -> Path:
    db_path = database_path or DATABASE_PATH
    cleaned_dataframe = clean_heart_data()

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        cleaned_dataframe.to_sql(TABLE_NAME, connection, if_exists="replace", index=False)

    return db_path


if __name__ == "__main__":
    database_file = load_clean_data_to_database()
    print(
        f"Loaded cleaned data into '{database_file.relative_to(REPO_ROOT)}' table '{TABLE_NAME}'."
    )
