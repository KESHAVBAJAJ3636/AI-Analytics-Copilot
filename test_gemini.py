
import os
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: Gemini API key not found in .env")
else:
    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Say hello. I am building an AI Analytics Copilot."
        )

        print("SUCCESS: Gemini API connected!")
        print("Gemini Response:")
        print(response.text)

    except Exception as error:
        print("API Connection Failed:")
        print(error)
