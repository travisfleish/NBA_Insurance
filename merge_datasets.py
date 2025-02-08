import pandas as pd

# Correct file paths (assuming they are inside the `data/` directory)
file_kaggle = "data/injury_data/NBA Player Injury Stats(1951 - 2023).csv"
file_scraped = "data/injury_data/nba_injuries_2023_present.csv"

# Load both datasets
df_kaggle = pd.read_csv(file_kaggle)
df_scraped = pd.read_csv(file_scraped)

# Standardize column names for merging
df_kaggle.columns = df_kaggle.columns.str.strip()
df_scraped.columns = df_scraped.columns.str.strip()

# Convert 'Date' column to datetime for filtering
df_kaggle['Date'] = pd.to_datetime(df_kaggle['Date'], errors='coerce')
df_scraped['Date'] = pd.to_datetime(df_scraped['Date'], errors='coerce')

# Define the date range (past 10 years)
cutoff_date = pd.Timestamp("2014-01-01")

# Filter both datasets for the last 10 years
df_kaggle_filtered = df_kaggle[df_kaggle['Date'] >= cutoff_date]
df_scraped_filtered = df_scraped[df_scraped['Date'] >= cutoff_date]

# Merge both datasets
df_merged = pd.concat([df_kaggle_filtered, df_scraped_filtered], ignore_index=True)

# Save merged dataset in the data directory
merged_file_path = "data/injury_data/nba_injuries_2014_2025.csv"
df_merged.to_csv(merged_file_path, index=False)

print(f"✅ Merged dataset saved at {merged_file_path}")
