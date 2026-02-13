import pandas as pd

# Load raw dataset
input_path = "data/CrimesOnWomenData.csv"
output_path = "data/crimes_cleaned.csv"

df = pd.read_csv(input_path)

# Drop unwanted index column
if "Unnamed: 0" in df.columns:
    df.drop(columns=["Unnamed: 0"], inplace=True)

# Rename columns for readability
df.rename(columns={
    "K&A": "Kidnapping_Abduction",
    "DD": "Dowry_Deaths",
    "AoW": "Assault_on_Women",
    "AoM": "Assault_on_Modesty",
    "DV": "Domestic_Violence",
    "WT": "Women_Trafficking"
}, inplace=True)

# Standard state naming
STANDARD_STATES = {
    "andaman and nicobar islands": "Andaman and Nicobar Islands",
    "andhra pradesh": "Andhra Pradesh",
    "arunachal pradesh": "Arunachal Pradesh",
    "assam": "Assam",
    "bihar": "Bihar",
    "chandigarh": "Chandigarh",
    "chhattisgarh": "Chhattisgarh",
    "dadra and nagar haveli": "Dadra and Nagar Haveli",
    "daman and diu": "Daman and Diu",
    "delhi": "Delhi",
    "goa": "Goa",
    "gujarat": "Gujarat",
    "haryana": "Haryana",
    "himachal pradesh": "Himachal Pradesh",
    "jammu and kashmir": "Jammu and Kashmir",
    "jharkhand": "Jharkhand",
    "karnataka": "Karnataka",
    "kerala": "Kerala",
    "lakshadweep": "Lakshadweep",
    "madhya pradesh": "Madhya Pradesh",
    "maharashtra": "Maharashtra",
    "manipur": "Manipur",
    "meghalaya": "Meghalaya",
    "mizoram": "Mizoram",
    "nagaland": "Nagaland",
    "odisha": "Odisha",
    "puducherry": "Puducherry",
    "punjab": "Punjab",
    "rajasthan": "Rajasthan",
    "sikkim": "Sikkim",
    "tamil nadu": "Tamil Nadu",
    "telangana": "Telangana",
    "tripura": "Tripura",
    "uttar pradesh": "Uttar Pradesh",
    "uttarakhand": "Uttarakhand",
    "west bengal": "West Bengal"
}

def normalize_state(name: str):
    if not isinstance(name, str):
        return name

    name = name.lower().strip()
    name = name.replace("&", "and")

    # remove UT prefix ONLY if it starts with it
    if name.startswith("ut "):
        name = name[3:]

    name = " ".join(name.split())

    return STANDARD_STATES.get(name, name.title())

# Apply normalization
df["State"] = df["State"].apply(normalize_state)

# Crime columns
crime_cols = [
    "Rape",
    "Kidnapping_Abduction",
    "Dowry_Deaths",
    "Assault_on_Women",
    "Assault_on_Modesty",
    "Domestic_Violence",
    "Women_Trafficking"
]

# Create total crimes column
df["Total_Crimes"] = df[crime_cols].sum(axis=1)

# Save cleaned dataset
df.to_csv(output_path, index=False)

print("✅ Preprocessing complete.")
print(f"Cleaned dataset saved to → {output_path}")
print(f"Unique States → {len(df['State'].unique())}")
print(sorted(df["State"].unique()))
