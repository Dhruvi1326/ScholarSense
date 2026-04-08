import os
import json
import time # Added for retry delay
from google import genai 
from google.genai import types
from google.api_core import exceptions # For catching server busy errors
from dotenv import load_dotenv

load_dotenv()

# Initialize the Client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_paper_integrity(pdf_path, clinical_mode=False):
    """
    Forensic Audit using Gemini 2.5 Flash with Retry Logic.
    """
    model_id = "gemini-2.5-flash"
    
    guardrail = ""
    if clinical_mode:
        guardrail = "CRITICAL: Focus on FDA safety and manufacturing scalability."

    prompt = f"""
    Analyze this research paper PDF. {guardrail}
    Return ONLY a JSON object with these keys: 
    "final_score" (int), "verdict" (string), "trust_level" (string), 
    "summary" (string), "red_flags" (list).
    """

    # --- RETRY LOGIC CONFIG ---
    max_retries = 3
    retry_delay = 2 # seconds

    for attempt in range(max_retries):
        try:
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            response = client.models.generate_content(
                model=model_id,
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                    prompt
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            # Success! Return the parsed result
            return response.parsed if response.parsed else json.loads(response.text)
                
        except (exceptions.ServiceUnavailable, exceptions.InternalServerError) as server_err:
            # This handles the 503 error you saw earlier
            if attempt < max_retries - 1:
                print(f"⚠️ Gemini is busy (503). Retrying in {retry_delay}s... (Attempt {attempt + 1})")
                time.sleep(retry_delay)
                retry_delay *= 2 # Wait longer each time (Exponential Backoff)
                continue
            else:
                return {
                    "final_score": 0,
                    "verdict": "Google Servers are currently overloaded. Please try again in 5 minutes.",
                    "trust_level": "Busy",
                    "summary": "The audit could not be completed because the AI server is at capacity.",
                    "red_flags": ["Service Temporarily Unavailable"]
                }

        except Exception as e:
            # This handles DNS (11002) or other major errors
            print(f"AI_ENGINE ERROR: {str(e)}")
            return {
                "final_score": 0,
                "verdict": "Audit Failed",
                "trust_level": "Error",
                "summary": f"Connection error: {str(e)}",
                "red_flags": ["Network connectivity issue. Please check your hotspot."]
            }