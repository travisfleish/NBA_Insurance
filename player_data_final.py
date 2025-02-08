import pandas as pd

# Load the cleaned dataset
file_path = "data/injury_data/nba_injuries_2014_2025_cleaned.csv"  # Update path if needed
df = pd.read_csv(file_path)

# Ensure 'Date' column is in datetime format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Dictionary to track multiple injuries per player
injury_records = {}

# Iterate through dataset to capture injury placements (Relinquished) and activations (Acquired)
for _, row in df.iterrows():
    date = row["Date"]
    acquired_player = row["Acquired"].strip().lstrip("•") if pd.notna(row["Acquired"]) else None
    relinquished_player = row["Relinquished"].strip().lstrip("•") if pd.notna(row["Relinquished"]) else None
    notes = row["Notes"].strip() if pd.notna(row["Notes"]) else None

    # If the player is "Relinquished", store the injury start date & notes
    if relinquished_player:
        if relinquished_player not in injury_records:
            injury_records[relinquished_player] = []
        injury_records[relinquished_player].append({"Injury": notes, "Start Date": date})

    # If the player is "Acquired", find their start date & calculate days missed
    if acquired_player and acquired_player in injury_records:
        if injury_records[acquired_player]:  # Ensure there is a record to update
            injury_records[acquired_player][-1]["Return Date"] = date

# Convert injury records to DataFrame
player_injury_data = []
for player, injuries in injury_records.items():
    for injury in injuries:
        if "Return Date" in injury:  # Ensure only completed injuries are saved
            start_date = injury["Start Date"]
            return_date = injury["Return Date"]
            days_missed = (return_date - start_date).days
            player_injury_data.append([player, injury["Injury"], start_date, return_date, days_missed])

# Create final DataFrame
df_player_injuries = pd.DataFrame(player_injury_data, columns=["Player", "Injury", "Start Date", "Return Date", "Days Missed"])

# ✅ Sort alphabetically by player name
df_player_injuries = df_player_injuries.sort_values(by="Player")

# Save the dataset
player_injury_dataset_path = "data/nba_player_injury_history_final.csv"
df_player_injuries.to_csv(player_injury_dataset_path, index=False)

print(f"✅ Player injury history saved as {player_injury_dataset_path}")
