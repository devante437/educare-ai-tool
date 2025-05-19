from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pandas as pd
import os

app = FastAPI()

# Enable CORS for all origins (good for development, restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Flutter web build files from the 'web' folder
web_dir = os.path.join(os.path.dirname(__file__), "web")
app.mount("/", StaticFiles(directory=web_dir, html=True), name="web")

# Load Excel file with requirements
try:
    data = pd.read_excel("requirements.xlsx")
    data.columns = data.columns.str.strip()  # Clean column names

    # Strip whitespace and convert to lowercase
    data["From Country"] = data["From Country"].astype(str).str.strip().str.lower()
    data["To Country"] = data["To Country"].astype(str).str.strip().str.lower()
    data["Requirement"] = data["Requirement"].astype(str).str.strip()

    print("✅ requirements.xlsx loaded successfully with shape:", data.shape)
    print("📄 Sample data:")
    print(data.head())

except FileNotFoundError:
    data = pd.DataFrame(columns=["From Country", "To Country", "Requirement"])
    print("⚠️ Excel file 'requirements.xlsx' not found. Place it in the backend folder.")

# API endpoint to get requirements based on from_country and to_country
@app.get("/api/requirements")
def get_requirements(from_country: str = Query(...), to_country: str = Query(...)):
    from_country = from_country.strip().lower()
    to_country = to_country.strip().lower()

    result = data[
        (data["From Country"] == from_country) &
        (data["To Country"] == to_country)
    ]

    if not result.empty:
        return {"status": "success", "requirement": result.iloc[0]["Requirement"]}
    else:
        return {
            "status": "not_found",
            "requirement": "No data found for your selection."
        }



