import streamlit as st
import pandas as pd
from database.db import get_incidents

st.set_page_config(page_title="Dashboard", page_icon="📊")

st.title("📊 CrisisLens Dashboard")

incidents = get_incidents()

if not incidents:
    st.warning("No incidents found. Submit a report first.")
    st.stop()

columns = [
    "id",
    "name",
    "location",
    "description",
    "image_path",
    "category",
    "severity",
    "ai_summary",
    "fake_probability",
    "image_ai_analysis",
    "emergency_recommendation",
    "created_at"
]

df = pd.DataFrame(incidents, columns=columns)

st.subheader("Total Incidents")
st.metric("Reports", len(df))

st.subheader("Recent Reports")
st.dataframe(df)

if "severity" in df.columns:
    st.subheader("Severity Distribution")
    severity_counts = df["severity"].value_counts()
    st.bar_chart(severity_counts)

if "category" in df.columns:
    st.subheader("Category Distribution")
    category_counts = df["category"].value_counts()
    st.bar_chart(category_counts)
