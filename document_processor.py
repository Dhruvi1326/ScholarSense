import google.generativeai as genai
import os
from dotenv import load_dotenv
from pypdf import PdfReader

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def upload_to_gemini(file_path):
    """
    Uploads the PDF to Gemini's temporary storage (48h free).
    This allows the AI to 'see' the document structure.
    """
    file = genai.upload_file(path=file_path, mime_type="application/pdf")
    return file

def extract_text(file_path):
    """
    Extracts text for our Qdrant Search. 
    Renamed from 'get_text_for_indexing' to match app.py calls.
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
        print(f"Error extracting PDF text: {e}")
        return ""