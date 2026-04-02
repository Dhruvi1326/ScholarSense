import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_paper_integrity(title, abstract):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    You are a Senior Peer Reviewer for a high-impact pharmaceutical journal. 
    Analyze this abstract for "Sound Science" vs "Scientific Fluff."

    SCORING RULES:
    1. INTERNAL LOGIC: Do the concentrations (mg/mL, % w/w) and flux rates (J) make physical sense?
    2. DATA TRANSPARENCY: Are there specific results (n=, p-values, Cmax) or just vague claims?
    3. EXPERT SIGNATURE: High-quality research is concise and precise. Reward clarity over wordiness.
    
    Title: {title}
    Abstract: {abstract}

    Return ONLY a JSON object with:
    - score (0-100)
    - verdict (High Integrity, Credible, or Low Rigor)
    - summary (2-sentence 'Bottom Line' for a researcher)
    - red_flags (List specific gaps found in the methodology)
    """
    
    try:
        response = model.generate_content(prompt)
        # Clean the response to ensure it is valid JSON
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"AI Audit Error: {e}")
        return {
            "score": 50, 
            "verdict": "Error", 
            "summary": "AI Audit failed to process.",
            "red_flags": ["System connectivity issue"]
        }