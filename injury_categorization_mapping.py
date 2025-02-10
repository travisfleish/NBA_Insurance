import pandas as pd

# Define injury categories and associated keywords
injury_categories = {
    "Head": ["concussion", "skull", "head"],
    "Face/Nose": ["nasal", "face", "cheek", "jaw", "eye", "tooth", "fracture"],
    "Neck": ["cervical", "neck"],
    "Back/Spine": ["lumbar", "spine", "back", "vertebrae", "disc", "tailbone"],
    "Shoulder": ["shoulder", "rotator cuff", "ac joint", "labrum"],
    "Arm/Elbow": ["elbow", "biceps", "triceps", "humerus"],
    "Wrist/Hand/Finger": ["wrist", "hand", "finger", "thumb"],
    "Hip/Groin": ["hip", "groin", "pelvis"],
    "Thigh": ["quadriceps", "hamstring", "thigh"],
    "Knee": ["knee", "acl", "mcl", "meniscus", "patella"],
    "Calf/Shin": ["calf", "shin", "tibia", "fibula"],
    "Ankle": ["ankle", "achilles"],
    "Foot/Toe": ["foot", "toe", "plantar", "heel"],
    "Abdomen/Core": ["abdominal", "oblique", "rib", "ribs", "muscle"],
    "Soft Tissue": ["bruised", "sore", "contusion"],
    "General Illness": ["illness", "flu", "virus", "infection", "respiratory", "gastroenteritis"],
    "General Injury": ["injury", "various", "ailment"],
    "Medical/Conditioning": ["conditioning", "surgery", "ineligible"],
    "Other/Unspecified": ["unknown", "miscellaneous", "undisclosed"]
}

# Function to categorize an injury
def categorize_injury(injury):
    if pd.isna(injury):  # Handle missing values
        return "Other/Unspecified"
    injury_lower = str(injury).strip().lower()  # Normalize text: lowercase & strip spaces
    for category, keywords in injury_categories.items():
        if any(keyword in injury_lower for keyword in keywords):
            return category
    return "Other/Unspecified"  # Default if no match is found

# Example usage with a DataFrame
if __name__ == "__main__":
    df = pd.read_csv("nba_injuries.csv")  # Load your dataset
    df["Injury"] = df["Injury"].str.replace("placed on IL", "Unknown", case=False, regex=True)  # Clean "placed on IL"
    df["Injury Category"] = df["Injury"].apply(categorize_injury)  # Apply categorization
    df.to_csv("nba_injuries_categorized.csv", index=False)  # Save output
