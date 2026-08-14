import os

from dotenv import load_dotenv
from google import genai


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# GET GEMINI API KEY
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    raise ValueError(
        "GEMINI_API_KEY environment variable is not set."
    )


# =========================================================
# CREATE GEMINI CLIENT
# =========================================================

client = genai.Client(
    api_key=api_key
)


# =========================================================
# GENERATE AI RESPONSE
# =========================================================

def generate_ai_response(prompt):
    """
    Send a prompt to Gemini and return the generated response.
    """

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text