import google.generativeai as genai
import json
import re
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_paper_integrity(gemini_file, clinical_mode=False):
    """
    Renamed to evaluate_paper_integrity to match the FastAPI main.py call.
    """
    model = genai.GenerativeModel('gemini-1.5-flash') # Using stable flash model
    
    guardrail = ""
    if clinical_mode:
        guardrail = """
        CRITICAL: Audit for Clinical Translation. 
        Focus on FDA/EMA human safety, skin irritation profiles, 
        and manufacturing scalability (GMP). 
        """

    prompt = f"""
    Analyze this research paper PDF. 
    {guardrail}
    1. Cross-verify the Abstract's claims against the Results tables and data.
    2. Check for unit consistency and statistical significance (P-values).
    3. Identify any logical gaps between the Conclusion and the actual Data.
    
    Return the report ONLY as a JSON object with these EXACT keys: 
    "final_score" (int 0-100), "verdict" (string), "trust_level" (string), "summary" (string), "red_flags" (list), "registry" (string).
    """
    
    try:
        response = model.generate_content([gemini_file, prompt])
        raw_text = response.text
        
        # Cleaning logic to find JSON block
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            clean_json = json_match.group(0)
            data = json.loads(clean_json)
            
            # Ensure the keys match what the UI and DB expect
            return {
                "final_score": data.get("final_score", data.get("score", 0)),
                "verdict": data.get("verdict", "N/A"),
                "trust_level": data.get("trust_level", data.get("trust_label", "Unknown")),
                "summary": data.get("summary", "No summary provided."),
                "red_flags": data.get("red_flags", []),
                "registry": data.get("registry", "Academic")
            }
        else:
            raise ValueError("AI response did not contain a valid JSON block.")
            
    except Exception as e:
        return {
            "final_score": 0,
            "verdict": "Audit Failed",
            "trust_level": "Error",
            "summary": f"Forensic Engine error: {str(e)}",
            "red_flags": ["System connectivity or parsing error"],
            "registry": "N/A"
        }