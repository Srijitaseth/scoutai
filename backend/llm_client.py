import os
import json
from google import genai


def get_client():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise Exception(
            "GEMINI_API_KEY is missing. Set it in the backend terminal."
        )

    return genai.Client(api_key=api_key)


def clean_json_text(text):
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return text


def call_llm_json(prompt):
    """
    Sends a prompt to Gemini and expects valid JSON back.
    Used for JD parsing, resume parsing, and interest scoring.
    """

    client = get_client()

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt
    )

    text = clean_json_text(response.text)

    return json.loads(text)


def call_llm_text(prompt):
    """
    Sends a prompt to Gemini and expects normal text back.
    Used for real agent conversation replies.
    """

    client = get_client()

    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=prompt
    )

    return response.text.strip()
