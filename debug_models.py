import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# Initialize the 2026 Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("--- Checking Available Gemini Models (April 2026) ---")
try:
    # This is the correct 2026 SDK method to list models
    for m in client.models.list():
        print(f"ID: {m.name:30} | Display: {m.display_name}")
except Exception as e:
    print(f"❌ Error connecting to Gemini API: {e}")