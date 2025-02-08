import pandas as pd

# Load the merged dataset
df_merged = pd.read_csv("data/injury_data/nba_injuries_2014_2025.csv")

# Remove the "Unnamed: 0" column if it exists
if "Unnamed: 0" in df_merged.columns:
    df_merged = df_merged.drop(columns=["Unnamed: 0"])

# Save the cleaned dataset
df_merged.to_csv("data/nba_injuries_2014_2025_cleaned.csv", index=False)

print("✅ Cleaned dataset saved as data/nba_injuries_2014_2025_cleaned.csv")
