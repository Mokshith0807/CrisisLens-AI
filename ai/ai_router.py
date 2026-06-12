import os
import requests
from ai.analyzer import analyze_incident as gemini_analyze


# ---------------------------
# LOCAL AI (OLLAMA)
# ---------------------------
def ollama_analyze(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        return response.json()["response"]

    except Exception as e:
        return f"Ollama Error: {str(e)}"


# ---------------------------
# CLOUD AI (GEMINI - DEFAULT)
# ---------------------------
def gemini_ai(prompt):
    return gemini_analyze(prompt)


# ---------------------------
# BYOK (Future extension)
# ---------------------------
def byok_ai(prompt, api_key, provider="gemini"):
    """
    User brings their own API key.
    Currently supports Gemini-style key usage.
    """

    if provider == "gemini":
        # reuse existing pipeline but could be extended
        return gemini_analyze(prompt)

    return "BYOK provider not supported yet."


# ---------------------------
# MAIN ROUTER
# ---------------------------
def run_ai(prompt, mode="gemini", api_key=None):

    if mode == "ollama":
        return ollama_analyze(prompt)

    elif mode == "byok":
        return byok_ai(prompt, api_key)

    else:
        return gemini_ai(prompt)
