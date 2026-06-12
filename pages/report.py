import streamlit as st
from database.db import save_incident
from ai.analyzer import analyze_incident, analyze_image
import os
import re


st.set_page_config(
    page_title="Report Incident",
    page_icon="🚨",
    layout="wide"
)


st.title("🚨 Report Disaster Incident")

st.markdown("""
Submit an incident report. CrisisLens AI will analyze the incident,
image evidence, and provide emergency response recommendations.
""")


name = st.text_input("👤 Your Name (Optional)")

location = st.text_input(
    "📍 Incident Location",
    placeholder="Example: Rushikonda Beach, Visakhapatnam, Andhra Pradesh, India"
)

description = st.text_area(
    "📝 Describe the incident",
    placeholder="Example: Heavy flooding has trapped several families."
)


image = st.file_uploader(
    "🖼 Upload Evidence Image",
    type=["jpg", "jpeg", "png"]
)


def extract_field(text, field):

    pattern = rf"{field}:\s*(.*?)(?:\n\n|\Z)"
    match = re.search(pattern, text, re.DOTALL)

    if match:
        return match.group(1).strip()

    return "Unknown"


if st.button("🚨 Analyze & Submit Report"):

    if not location or not description:
        st.error("Please enter location and incident description.")

    else:

        with st.spinner("🧠 CrisisLens AI analyzing the emergency..."):

            # Text AI Analysis
            ai_result = analyze_incident(description)

            category = extract_field(
                ai_result,
                "Category"
            )

            severity = extract_field(
                ai_result,
                "Severity"
            )

            fake_probability = extract_field(
                ai_result,
                "Fake Report Probability"
            )

            summary = extract_field(
                ai_result,
                "Summary"
            )

            recommendation = extract_field(
                ai_result,
                "Emergency Recommendation"
            )


            # Image AI Analysis
            image_path = ""
            image_analysis = "No image provided."

            if image:

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                image_path = os.path.join(
                    "uploads",
                    image.name
                )

                with open(image_path, "wb") as file:
                    file.write(image.getbuffer())

                image_analysis = analyze_image(
                    image_path
                )


            # Save everything
            save_incident(
                name,
                location,
                description,
                image_path,
                category,
                severity,
                summary,
                fake_probability,
                image_analysis,
                recommendation
            )


        st.success(
            "✅ Crisis report analyzed and saved successfully!"
        )

        st.divider()

        st.subheader("🧠 AI Disaster Intelligence Report")


        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "🌊 Category",
                category
            )

        with col2:
            st.metric(
                "🔥 Severity",
                severity
            )


        st.write("### 🚫 Fake Report Probability")
        st.info(fake_probability)


        st.write("### 📝 AI Emergency Summary")
        st.success(summary)


        st.write("### 🖼 AI Image Intelligence")
        st.warning(image_analysis)


        st.write("### 🏆 AI Emergency Recommendations")
        st.error(recommendation)


        if image:
            st.image(
                image,
                caption="Uploaded Evidence",
                use_container_width=True
            )
