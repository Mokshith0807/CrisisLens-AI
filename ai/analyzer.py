import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GOOGLE_API_KEY")
)


def analyze_incident(text):
    prompt = f"""
You are an emergency response AI.

Analyze this incident:
{text}

Return:
- Category
- Severity (Low/Medium/High/Critical)
- Fake probability (0-100%)
- Summary
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"AI Analysis Error: {str(e)}"


def analyze_image(image_path):
    """
    Safe image analysis for Streamlit Cloud
    """

    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "mime_type": "image/jpeg",
                    "data": image_bytes
                },
                "Analyze this disaster image. Describe damage, risks, severity, and emergency response recommendations."
            ]
        )

        return response.text

    except Exception as e:
        return f"Image Analysis Error: {str(e)}"
