from google import genai
from dotenv import load_dotenv
from PIL import Image
import os
import time

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_incident(description):

    prompt = f"""
    You are CrisisLens AI, an advanced disaster intelligence system.

    Analyze the disaster report and return EXACTLY in this format:

    Category: <Flood/Fire/Earthquake/Accident/Medical Emergency/Other>

    Severity: <Low/Medium/High/Critical>

    Fake Report Probability: <0-100%>

    Summary: <Short emergency summary>

    Emergency Recommendation:
    <3-5 short action points for rescue teams>

    Incident:
    {description}
    """

    models = [
        "gemini-2.5-flash",
        "gemini-2.0-flash"
    ]

    for model in models:

        try:
            response = client.models.generate_content(
                model=model,
                contents=prompt
            )

            return response.text

        except Exception:
            time.sleep(2)
            continue


    return """
Category: Unknown

Severity: Unknown

Fake Report Probability: Unknown

Summary: AI analysis unavailable.

Emergency Recommendation:
Unable to generate recommendations.
"""


def analyze_image(image_path):

    try:

        image = Image.open(image_path)

        prompt = """
        You are an AI disaster image analyst.

        Analyze the image and provide:

        - Incident type visible
        - Dangers or damage
        - Risks to people
        - Recommended emergency response

        Keep your answer concise in bullet points.
        """

        models = [
            "gemini-2.5-flash",
            "gemini-2.0-flash"
        ]


        for model in models:

            try:
                response = client.models.generate_content(
                    model=model,
                    contents=[
                        prompt,
                        image
                    ]
                )

                return response.text

            except Exception:
                time.sleep(2)
                continue


        return "Image AI analysis temporarily unavailable."


    except Exception as e:

        return f"Image analysis error: {str(e)}"
