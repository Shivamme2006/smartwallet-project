from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"
SOURCE_CSV = DATA_DIR / "heart.csv"
CLEANED_CSV = DATA_DIR / "heart_cleaned.csv"

REQUIRED_COLUMNS = [
    "age",
    "sex",
    "cp",
    "trestbps",
    "chol",
    "fbs",
    "restecg",
    "thalach",
    "exang",
    "oldpeak",
    "slope",
    "ca",
    "thal",
    "target",
]
NUMERIC_COLUMNS = REQUIRED_COLUMNS
POSITIVE_COLUMNS = ["age", "trestbps", "chol", "thalach"]
BINARY_COLUMNS = ["sex", "fbs", "exang", "target"]


def _normalize_columns(columns: Iterable[str]) -> list[str]:
    return [str(column).strip().lower() for column in columns]


def _validate_required_columns(dataframe: pd.DataFrame) -> None:
    missing_columns = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing_columns:
        missing = ", ".join(missing_columns)
        raise ValueError(f"Dataset is missing required columns: {missing}")


def clean_heart_data(
    source_path: Path | None = None,
    cleaned_path: Path | None = None,
) -> pd.DataFrame:
    csv_path = source_path or SOURCE_CSV
    output_path = cleaned_path or CLEANED_CSV

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Heart disease dataset not found at '{csv_path}'. Place the CSV at data/heart.csv."
        )

    dataframe = pd.read_csv(csv_path)
    dataframe.columns = _normalize_columns(dataframe.columns)
    _validate_required_columns(dataframe)

    dataframe = dataframe[REQUIRED_COLUMNS].drop_duplicates().copy()

    for column in NUMERIC_COLUMNS:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    dataframe = dataframe.dropna(subset=REQUIRED_COLUMNS)

    for column in POSITIVE_COLUMNS:
        dataframe = dataframe[dataframe[column] > 0]

    dataframe = dataframe[dataframe["oldpeak"] >= 0]

    for column in BINARY_COLUMNS:
        dataframe = dataframe[dataframe[column].isin([0, 1])]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    return dataframe.reset_index(drop=True)


if __name__ == "__main__":
    cleaned = clean_heart_data()
    print(
        f"Cleaned dataset saved to '{CLEANED_CSV.relative_to(REPO_ROOT)}' with {len(cleaned)} rows."
    )
