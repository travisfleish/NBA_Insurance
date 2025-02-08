import pandas as pd

# Load dataset
file_path = "data/nba_player_injury_history_final.csv"
df = pd.read_csv(file_path)

# Extract all unique injury descriptions
unique_injuries = df["Injury"].dropna().unique()

# Save unique injury names to review
with open("data/unique_injuries.txt", "w") as f:
    for injury in unique_injuries:
        f.write(injury + "\n")

print(f"✅ Extracted {len(unique_injuries)} unique injuries. Check 'data/unique_injuries.txt'")
