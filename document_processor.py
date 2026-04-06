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

def get_text_for_indexing(file_path):
    """
    Quickly extracts text for our Qdrant Search (Day 4 logic).
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text