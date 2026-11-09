"""
Explore every CSV file in the MusicOSet dataset folders.

Put this file in your src folder and run from the project folder:
    python src/explore_all.py

It prints a report for each file and saves a one-row-per-file summary
to outputs/data_overview.csv.
"""

from pathlib import Path

import pandas as pd

# Project folder = the folder above src/, so the script works
# no matter which folder you run it from
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FOLDERS = ["musicoset_metadata", "musicoset_popularity", "musicoset_songfeatures"]
OUTPUT_FOLDER = PROJECT_FOLDER / "outputs"

# Show all columns when printing wide tables
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def load_csv(file_path):
    """Load a CSV, trying tab-separated first (MusicOSet's usual format),
    then falling back to comma-separated if that gives a single column."""
    table = pd.read_csv(file_path, sep="\t")
    if table.shape[1] == 1:
        table = pd.read_csv(file_path)
    return table


def describe_table(name, table):
    """Print a short report on one table."""
    print("=" * 70)
    print(f"FILE: {name}")
    print(f"Rows: {table.shape[0]:,}   Columns: {table.shape[1]}")

    print("\nColumns, types and missing values:")
    column_info = pd.DataFrame({
        "type": table.dtypes.astype(str),
        "missing": table.isna().sum(),
        "missing_%": (table.isna().mean() * 100).round(1),
        "unique_values": table.nunique(),
    })
    print(column_info)

    print(f"\nExact duplicate rows: {table.duplicated().sum():,}")

    print("\nFirst 3 rows:")
    print(table.head(3))

    numeric_columns = table.select_dtypes("number")
    if not numeric_columns.empty:
        print("\nNumeric summary:")
        print(numeric_columns.describe().T.round(3))
    print()


summary_rows = []

for folder_name in DATA_FOLDERS:
    folder = PROJECT_FOLDER / folder_name
    if not folder.exists():
        print(f"Folder not found, skipping: {folder}")
        continue

    for csv_path in sorted(folder.glob("*.csv")):
        file_label = f"{folder_name}/{csv_path.name}"
        try:
            table = load_csv(csv_path)
        except Exception as error:
            print(f"Could not read {file_label}: {error}")
            continue

        describe_table(file_label, table)

        summary_rows.append({
            "file": file_label,
            "rows": table.shape[0],
            "columns": table.shape[1],
            "column_names": ", ".join(table.columns),
            "total_missing_cells": int(table.isna().sum().sum()),
            "duplicate_rows": int(table.duplicated().sum()),
        })

# Save the one-row-per-file overview
OUTPUT_FOLDER.mkdir(exist_ok=True)
overview = pd.DataFrame(summary_rows)
overview.to_csv(OUTPUT_FOLDER / "data_overview.csv", index=False)

print("=" * 70)
print("OVERVIEW OF ALL FILES")
print(overview[["file", "rows", "columns", "total_missing_cells", "duplicate_rows"]])
print(f"\nSaved to {OUTPUT_FOLDER / 'data_overview.csv'}")