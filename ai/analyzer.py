import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))


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

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    return response.text


def analyze_image(image_path):
    prompt = "Analyze this disaster image and describe risks, damage, and response."

    with open(image_path, "rb") as img:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt, img]
        )

    return response.text
