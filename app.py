from fastapi import FastAPI
import pandas as pd

app = FastAPI(
    title="India WPIS Backend",
    description="Crime Against Women Analytics API (2001–2021)",
    version="1.0"
)

# Load dataset
df = pd.read_csv("data/crimes_cleaned.csv")

# # Drop unwanted column
# df.drop(columns=["Unnamed: 0"], inplace=True)

# Rename columns
df.rename(columns={
    "K&A": "Kidnapping_Abduction",
    "DD": "Dowry_Deaths",
    "AoW": "Assault_on_Women",
    "AoM": "Assault_on_Modesty",
    "DV": "Domestic_Violence",
    "WT": "Women_Trafficking"
}, inplace=True)

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

# ------------------- APIs -------------------

@app.get("/")
def home():
    return {"message": "India WPIS Backend is Running 🚀"}


@app.get("/states")
def get_states():
    return sorted(df["State"].unique().tolist())


@app.get("/map-data")
def map_data():
    state_totals = df.groupby("State")["Total_Crimes"].sum().reset_index()
    return state_totals.to_dict(orient="records")


@app.get("/state/{state}")
def state_full_data(state: str):
    data = df[df["State"] == state]
    return data.to_dict(orient="records")


@app.get("/state/{state}/yearly")
def yearly_trend(state: str):
    yearly = (
        df[df["State"] == state]
        .groupby("Year")["Total_Crimes"]
        .sum()
        .reset_index()
    )
    return yearly.to_dict(orient="records")


@app.get("/state/{state}/crime-split")
def crime_split(state: str):
    data = df[df["State"] == state]
    totals = data[crime_cols].sum().reset_index()
    totals.columns = ["crime_type", "count"]
    return totals.to_dict(orient="records")


@app.get("/state/{state}/insights")
def insights(state: str):
    data = df[df["State"] == state]

    yearly = data.groupby("Year")["Total_Crimes"].sum()
    worst_year = int(yearly.idxmax())
    worst_year_count = int(yearly.max())

    crime_totals = data[crime_cols].sum()
    top_crime = crime_totals.idxmax()

    return {
        "state": state,
        "total_cases": int(data["Total_Crimes"].sum()),
        "worst_year": worst_year,
        "worst_year_cases": worst_year_count,
        "most_common_crime": top_crime
    }


@app.get("/national/summary")
def national_summary():
    yearly = df.groupby("Year")["Total_Crimes"].sum().reset_index()

    crime_totals = df[crime_cols].sum().reset_index()
    crime_totals.columns = ["crime_type", "count"]

    return {
        "yearly_trend": yearly.to_dict(orient="records"),
        "crime_distribution": crime_totals.to_dict(orient="records")
    }
