import pandas as pd
from rapidfuzz import process, fuzz  # Faster alternative to fuzzywuzzy

# Load dataset
file_path = "data/nba_player_injury_history_final.csv"
df = pd.read_csv(file_path)

# Extract unique injury names
unique_injuries = df["Injury"].dropna().unique().tolist()

# Step 1: Automatically Cluster Similar Injury Names
standardized_injuries = {}
processed = set()

for injury in unique_injuries:
    if injury in processed:
        continue  # Skip already processed injuries

    # Find similar injury names
    matches = process.extract(injury, unique_injuries, scorer=fuzz.token_sort_ratio, limit=10)

    # Select the most common phrasing as the standard name
    base_name = matches[0][0]

    for match_tuple in matches:
        match, score, _ = match_tuple  # ✅ Correct tuple unpacking
        if score >= 85:  # Only group names with high similarity
            standardized_injuries[match] = base_name
            processed.add(match)

# Step 2: Apply the Standardization to the Dataset
df["Standardized Injury"] = df["Injury"].map(lambda x: standardized_injuries.get(x, x))

# Save the cleaned dataset
cleaned_file_path = "data/nba_player_injury_history_cleaned.csv"
df.to_csv(cleaned_file_path, index=False)

print(f"✅ Standardized injury dataset saved as {cleaned_file_path}")
