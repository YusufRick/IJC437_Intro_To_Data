"""
First look at the Billboard Hot-100 (2000-2023) dataset.
Run this in the same folder as the CSV you downloaded from Kaggle.
"""

import pandas as pd
import matplotlib.pyplot as plt


file = input("Enter the path to the CSV file (e.g. musicoset_metadata/songs.csv): ")
songs = pd.read_csv(file, sep="\t")

# 2. Basic shape: how many rows (songs/chart entries) and columns?
print("Rows, columns:", songs.shape)

# 3. Column names and data types - note which are numbers vs text
print("\nColumns and types:")
print(songs.dtypes)

# 4. Peek at the first few rows
print("\nFirst 5 rows:")
print(songs.head())

# 5. Missing values per column (sorted, biggest gaps first)
print("\nMissing values per column:")
print(songs.isna().sum().sort_values(ascending=False))

# 6. Duplicate rows - the same song may appear in several years/weeks
print("\nExact duplicate rows:", songs.duplicated().sum())

# 7. Summary statistics for the numeric columns (e.g. danceability, energy)
print("\nNumeric summary:")
print(songs.describe().T)

# 8. Quick look: one audio feature averaged by year
#    Edit these two names to match your dataset's columns
YEAR_COLUMN = "year"
FEATURE_COLUMN = "danceability"

if YEAR_COLUMN in songs.columns and FEATURE_COLUMN in songs.columns:
    yearly_average = songs.groupby(YEAR_COLUMN)[FEATURE_COLUMN].mean()
    yearly_average.plot(marker="o")
    plt.title(f"Average {FEATURE_COLUMN} of Billboard songs by year")
    plt.xlabel("Year")
    plt.ylabel(f"Mean {FEATURE_COLUMN}")
    plt.tight_layout()
    plt.show()
else:
    print(f"\nEdit YEAR_COLUMN / FEATURE_COLUMN: check the column list above.")