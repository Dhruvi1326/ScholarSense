import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def audit_full_document(gemini_file, clinical_mode):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # The Toggle Logic 
    guardrail = ""
    if clinical_mode:
        guardrail = "CRITICAL: Audit for Clinical Translation. Check for FDA safety and human skin compatibility."

    prompt = f"""
    Analyze this research paper PDF. 
    {guardrail}
    1. Cross-verify the Abstract's data against the Results tables.
    2. Check for unit consistency and statistical significance.
    3. Return JSON: score, verdict, trust_label, summary, red_flags.
    """
    
    response = model.generate_content([gemini_file, prompt])
    # Standard JSON cleaning logic
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    return json.loads(clean_json)