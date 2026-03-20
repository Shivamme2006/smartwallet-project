from __future__ import annotations

from html import escape
from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request

from scripts.queries import get_patients_data


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = REPO_ROOT / "flask_app" / "templates"
STATIC_DIR = REPO_ROOT / "flask_app" / "static"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR), static_folder=str(STATIC_DIR))

SEX_LABELS = {0: "Female", 1: "Male"}
TARGET_LABELS = {0: "No disease", 1: "Heart disease"}
TARGET_COLORS = {0: "#5b7c99", 1: "#c45a38"}


def parse_int(value: str | None) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError:
        return None


def chart_card(title: str, subtitle: str, svg: str) -> dict[str, str]:
    return {"title": title, "subtitle": subtitle, "svg": svg}


def empty_chart(message: str) -> str:
    return f"""
    <svg viewBox="0 0 640 280" role="img" aria-label="{escape(message)}">
        <rect x="0" y="0" width="640" height="280" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        <text x="320" y="145" text-anchor="middle" fill="#6b6a67" font-size="18">{escape(message)}</text>
    </svg>
    """


def build_age_target_chart(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return empty_chart("No age data available for the selected filters.")

    grouped = (
        dataframe.groupby(["age", "target"])
        .size()
        .unstack(fill_value=0)
        .reindex(columns=[0, 1], fill_value=0)
        .sort_index()
    )
    width = 760
    height = 320
    left = 56
    bottom = 36
    top = 24
    chart_height = height - top - bottom
    chart_width = width - left - 18
    max_total = int(grouped.sum(axis=1).max()) or 1
    step = chart_width / max(len(grouped), 1)
    bar_width = max(step * 0.72, 8)
    bars = []
    labels = []

    for index, (age, row) in enumerate(grouped.iterrows()):
        x = left + index * step + (step - bar_width) / 2
        running_y = top + chart_height
        for target in [0, 1]:
            value = int(row[target])
            bar_height = (value / max_total) * chart_height
            y = running_y - bar_height
            bars.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" '
                f'fill="{TARGET_COLORS[target]}" rx="4" />'
            )
            running_y = y
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{height - 12}" text-anchor="middle" '
            f'font-size="11" fill="#475467">{int(age)}</text>'
        )

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Age by heart disease status">
        <rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" stroke="#b7ab95" />
        <line x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" y2="{top + chart_height}" stroke="#b7ab95" />
        {''.join(bars)}
        {''.join(labels)}
    </svg>
    """


def build_histogram(dataframe: pd.DataFrame, column: str, bins: int = 6) -> str:
    if dataframe.empty:
        return empty_chart("No cholesterol data available for the selected filters.")

    series = dataframe[column]
    minimum = float(series.min())
    maximum = float(series.max())
    if minimum == maximum:
        minimum -= 1
        maximum += 1

    edges = pd.interval_range(start=minimum, end=maximum, periods=bins)
    counts = pd.cut(series, bins=edges).value_counts(sort=False)

    width = 760
    height = 320
    left = 56
    bottom = 42
    top = 24
    chart_height = height - top - bottom
    chart_width = width - left - 18
    step = chart_width / max(len(counts), 1)
    bar_width = max(step * 0.74, 10)
    max_count = int(counts.max()) or 1
    bars = []
    labels = []

    for index, (interval, count) in enumerate(counts.items()):
        x = left + index * step + (step - bar_width) / 2
        bar_height = (int(count) / max_count) * chart_height
        y = top + chart_height - bar_height
        bars.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_height:.1f}" fill="#d28d54" rx="4" />'
        )
        label = f"{int(interval.left)}-{int(interval.right)}"
        labels.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{height - 12}" text-anchor="middle" font-size="10" fill="#475467">{escape(label)}</text>'
        )

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Cholesterol distribution">
        <rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top + chart_height}" stroke="#b7ab95" />
        <line x1="{left}" y1="{top + chart_height}" x2="{left + chart_width}" y2="{top + chart_height}" stroke="#b7ab95" />
        {''.join(bars)}
        {''.join(labels)}
    </svg>
    """


def build_gender_target_chart(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return empty_chart("No gender data available for the selected filters.")

    grouped = (
        dataframe.groupby(["sex", "target"])
        .size()
        .unstack(fill_value=0)
        .reindex(index=[0, 1], columns=[0, 1], fill_value=0)
    )
    width = 540
    height = 300
    left = 72
    right = 28
    bar_height = 48
    gap = 56
    start_y = 68
    usable = width - left - right
    max_total = int(grouped.sum(axis=1).max()) or 1
    bars = []
    labels = []

    for idx, sex in enumerate(grouped.index):
        y = start_y + idx * (bar_height + gap)
        x = left
        labels.append(
            f'<text x="18" y="{y + 30}" font-size="14" fill="#344054">{SEX_LABELS.get(sex, str(sex))}</text>'
        )
        for target in [0, 1]:
            value = int(grouped.loc[sex, target])
            segment_width = (value / max_total) * usable
            bars.append(
                f'<rect x="{x:.1f}" y="{y:.1f}" width="{segment_width:.1f}" height="{bar_height}" fill="{TARGET_COLORS[target]}" rx="8" />'
            )
            if value:
                bars.append(
                    f'<text x="{x + segment_width / 2:.1f}" y="{y + 29}" text-anchor="middle" font-size="13" fill="#ffffff">{value}</text>'
                )
            x += segment_width

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Gender by heart disease status">
        <rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        {''.join(labels)}
        {''.join(bars)}
    </svg>
    """


def build_scatter_chart(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return empty_chart("No blood pressure data available for the selected filters.")

    width = 760
    height = 340
    left = 54
    right = 18
    top = 24
    bottom = 38
    plot_width = width - left - right
    plot_height = height - top - bottom
    age_min = float(dataframe["age"].min())
    age_max = float(dataframe["age"].max())
    bp_min = float(dataframe["trestbps"].min())
    bp_max = float(dataframe["trestbps"].max())
    age_span = age_max - age_min or 1
    bp_span = bp_max - bp_min or 1
    points = []

    for _, row in dataframe.iterrows():
        x = left + ((float(row["age"]) - age_min) / age_span) * plot_width
        y = top + plot_height - ((float(row["trestbps"]) - bp_min) / bp_span) * plot_height
        points.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{TARGET_COLORS[int(row["target"])]}" opacity="0.85" />'
        )

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Blood pressure versus age">
        <rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#b7ab95" />
        <line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#b7ab95" />
        {''.join(points)}
    </svg>
    """


def build_line_chart(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return empty_chart("No heart rate data available for the selected filters.")

    series = dataframe.groupby("age")["thalach"].mean().sort_index()
    width = 760
    height = 320
    left = 54
    right = 18
    top = 24
    bottom = 38
    plot_width = width - left - right
    plot_height = height - top - bottom
    age_min = float(series.index.min())
    age_max = float(series.index.max())
    rate_min = float(series.min())
    rate_max = float(series.max())
    age_span = age_max - age_min or 1
    rate_span = rate_max - rate_min or 1
    points = []

    for age, value in series.items():
        x = left + ((float(age) - age_min) / age_span) * plot_width
        y = top + plot_height - ((float(value) - rate_min) / rate_span) * plot_height
        points.append((x, y))

    path = " ".join(
        [f"M {points[0][0]:.1f} {points[0][1]:.1f}"]
        + [f"L {x:.1f} {y:.1f}" for x, y in points[1:]]
    )
    markers = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#2f6f5f" />' for x, y in points
    )

    return f"""
    <svg viewBox="0 0 {width} {height}" role="img" aria-label="Average heart rate by age">
        <rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="#fffdf8" stroke="#dccfb8" />
        <line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_height}" stroke="#b7ab95" />
        <line x1="{left}" y1="{top + plot_height}" x2="{left + plot_width}" y2="{top + plot_height}" stroke="#b7ab95" />
        <path d="{path}" fill="none" stroke="#2f6f5f" stroke-width="3" />
        {markers}
    </svg>
    """


@app.route("/")
def dashboard() -> str:
    error_message = ""
    filters = {
        "age_min": parse_int(request.args.get("age_min")),
        "age_max": parse_int(request.args.get("age_max")),
        "sex": request.args.get("sex", ""),
        "chol_max": parse_int(request.args.get("chol_max")),
    }

    try:
        dataframe = get_patients_data()
    except FileNotFoundError as exc:
        error_message = str(exc)
        dataframe = pd.DataFrame(
            columns=["age", "sex", "chol", "trestbps", "thalach", "target"]
        )

    if filters["age_min"] is not None:
        dataframe = dataframe[dataframe["age"] >= filters["age_min"]]
    if filters["age_max"] is not None:
        dataframe = dataframe[dataframe["age"] <= filters["age_max"]]
    if filters["sex"] in {"0", "1"}:
        dataframe = dataframe[dataframe["sex"] == int(filters["sex"])]
    if filters["chol_max"] is not None:
        dataframe = dataframe[dataframe["chol"] <= filters["chol_max"]]

    summary = {
        "patients": int(len(dataframe)),
        "heart_disease_cases": int(dataframe["target"].sum()) if not dataframe.empty else 0,
        "average_age": round(float(dataframe["age"].mean()), 1) if not dataframe.empty else 0,
        "average_cholesterol": round(float(dataframe["chol"].mean()), 1) if not dataframe.empty else 0,
    }

    charts = [
        chart_card(
            "Age vs Heart Disease",
            "Stacked bars show how disease presence changes across patient ages.",
            build_age_target_chart(dataframe),
        ),
        chart_card(
            "Cholesterol Distribution",
            "Histogram of cholesterol values for the active filter set.",
            build_histogram(dataframe, "chol"),
        ),
        chart_card(
            "Gender vs Heart Disease",
            "Comparison of cases by sex and disease outcome.",
            build_gender_target_chart(dataframe),
        ),
        chart_card(
            "Blood Pressure vs Age",
            "Scatter plot of resting blood pressure against age.",
            build_scatter_chart(dataframe),
        ),
        chart_card(
            "Heart Rate vs Age",
            "Average maximum heart rate by age.",
            build_line_chart(dataframe),
        ),
    ]

    return render_template(
        "dashboard.html",
        charts=charts,
        summary=summary,
        filters=filters,
        error_message=error_message,
        sex_labels=SEX_LABELS,
        target_labels=TARGET_LABELS,
        target_colors=TARGET_COLORS,
    )


if __name__ == "__main__":
    app.run(debug=True)
