import os
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()

def extract_text(file_path):
    """
    Extracts raw text for our Qdrant Search.
    Gemini now handles the PDF directly, so we only use this for 'Neural Discovery'.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"Extraction Error: {e}")
        return ""

# WE REMOVED upload_to_gemini because the new 2026 SDK 
# in ai_engine.py handles this automatically!