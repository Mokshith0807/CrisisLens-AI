import streamlit as st
from database.db import get_incidents
import pandas as pd
import plotly.express as px
import os
import folium
from streamlit_folium import st_folium
from ai.geocoder import get_coordinates


st.set_page_config(
    page_title="Crisis Command Center",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 CrisisLens AI Command Center")

st.markdown(
    "Real-time disaster monitoring powered by AI intelligence."
)


# Get incidents
incidents = get_incidents()


def count_severity(level):
    return sum(
        1 for item in incidents
        if item[6]
        and item[6].lower() == level.lower()
    )


# ==============================
# Top Metrics
# ==============================

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "📋 Total Incidents",
        len(incidents)
    )

with col2:
    st.metric(
        "🔴 Critical",
        count_severity("Critical")
    )

with col3:
    st.metric(
        "🟠 High",
        count_severity("High")
    )

with col4:
    st.metric(
        "🟡 Medium",
        count_severity("Medium")
    )

with col5:
    st.metric(
        "🟢 Low",
        count_severity("Low")
    )


st.divider()


# ==============================
# Severity Chart
# ==============================

if incidents:

    severity_data = [
        item[6]
        for item in incidents
        if item[6]
    ]

    if severity_data:

        df = pd.DataFrame(
            severity_data,
            columns=["Severity"]
        )

        fig = px.pie(
            df,
            names="Severity",
            title="📊 Disaster Severity Distribution"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


st.divider()


# ==============================
# Critical Alerts
# ==============================

critical_incidents = [
    item for item in incidents
    if item[6]
    and item[6].lower() == "critical"
]


if critical_incidents:

    st.error(
        f"🚨 {len(critical_incidents)} Critical incidents need immediate action!"
    )

    for item in critical_incidents:

        st.warning(
            f"""
📍 Location: {item[2]}

🌊 Disaster Type: {item[5]}

🧠 AI Summary:
{item[7]}
"""
        )


st.divider()


# ==============================
# Live Crisis Map
# ==============================

st.subheader("🗺️ Live Crisis Map")

crisis_map = None


for item in incidents:

    location = item[2]

    coordinates = get_coordinates(location)

    if coordinates:

        lat, lon = coordinates

        if crisis_map is None:

            crisis_map = folium.Map(
                location=[lat, lon],
                zoom_start=10
            )

        severity = item[6].lower() if item[6] else "unknown"

        colors = {
            "critical": "red",
            "high": "orange",
            "medium": "beige",
            "low": "green"
        }

        folium.Marker(
            location=[lat, lon],
            popup=f"""
🚨 {item[5]}

📍 {location}

Severity: {item[6]}
""",
            icon=folium.Icon(
                color=colors.get(severity, "blue")
            )
        ).add_to(crisis_map)


if crisis_map:

    st_folium(
        crisis_map,
        width=1200,
        height=500
    )

else:

    st.info(
        "No locations available for map display."
    )


st.divider()


# ==============================
# Incident Intelligence Feed
# ==============================

st.subheader(
    "🛰️ Incident Intelligence Feed"
)

if incidents:

    for item in incidents:

        (
            incident_id,
            name,
            location,
            description,
            image_path,
            category,
            severity,
            ai_summary,
            fake_probability,
            image_ai_analysis,
            emergency_recommendation,
            created_at
        ) = item


        with st.expander(
            f"🚨 {severity} | {category} | {location}"
        ):

            col1, col2 = st.columns([2, 1])


            with col1:

                st.markdown(
                    f"""
### 👤 Reporter

{name if name else "Anonymous"}

---

### 📍 Location

{location}

---

### 📝 Citizen Report

{description}

---

### 🤖 AI Text Intelligence

**Category:** {category}

**Severity:** {severity}

**Fake Report Probability:** {fake_probability}

**AI Summary:**

{ai_summary}

---

### 🖼️ AI Image Intelligence

{image_ai_analysis}

---

### 🏆 AI Emergency Recommendations

{emergency_recommendation}

---

### 🕒 Reported At

{created_at}
"""
                )


            with col2:

                if (
                    image_path
                    and os.path.exists(image_path)
                ):

                    st.image(
                        image_path,
                        caption="📸 Incident Evidence",
                        use_container_width=True
                    )


else:

    st.info(
        "No incidents have been reported yet."
    )
