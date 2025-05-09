import streamlit as st
import pandas as pd

# Simulated data this will be replaced later with real Excel data
data = pd.DataFrame([
    {"From Country": "Germany", "To Country": "Canada", "Requirement": "Abitur, IELTS 6.5+"},
    {"From Country": "Germany", "To Country": "USA", "Requirement": "Abitur, TOEFL 90+"},
    {"From Country": "India", "To Country": "Germany", "Requirement": "12th Pass, APS Certificate"},
])

# Streamlit UI
st.title("Study Abroad Requirement Checker")

from_country = st.selectbox("Where are you from?", data["From Country"].unique())
to_country = st.selectbox("Where do you want to study?", data["To Country"].unique())

# Filter based on selection
result = data[(data["From Country"] == from_country) & (data["To Country"] == to_country)]

# Show the requirement
if not result.empty:
    st.success(f"Requirements: {result.iloc[0]['Requirement']}")
else:
    st.warning("No data found for your selection.")
