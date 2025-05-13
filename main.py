from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Create FastAPI app
app = FastAPI()

# Allow all origins (for dev; restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Excel file ('requirements.xlsx' should exist in same folder)
try:
    data = pd.read_excel("requirements.xlsx")
    data.columns = data.columns.str.strip()  # Clean column names
except FileNotFoundError:
    data = pd.DataFrame(columns=["From Country", "To Country", "Requirement"])
    print("⚠️ Excel file not found. Make sure 'requirements.xlsx' is placed correctly.")

# Test route
@app.get("/")
def root():
    return {"message": "Study Abroad API is running!"}

# Main route to fetch requirements
@app.get("/requirements")
def get_requirements(from_country: str = Query(...), to_country: str = Query(...)):
    result = data[
        (data["From Country"] == from_country) &
        (data["To Country"] == to_country)
    ]
    if not result.empty:
        return {"status": "success", "requirement": result.iloc[0]["Requirement"]}
    else:
        return {"status": "not_found", "requirement": "No data found for your selection."}
