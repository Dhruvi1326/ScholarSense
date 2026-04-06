import google.generativeai as genai
import json
import re  # New import for robust parsing
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def audit_full_document(gemini_file, clinical_mode):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Enhanced Guardrail for Clinical Mode
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
    
    Return the report ONLY as a JSON object with these keys: 
    "score" (int 0-100), "verdict" (string), "trust_label" (string), "summary" (string), "red_flags" (list).
    """
    
    try:
        response = model.generate_content([gemini_file, prompt])
        raw_text = response.text
        
        # 1. CLEANING LOGIC: Use regex to find the JSON block { ... }
        # This ignores any "Here is your JSON:" chatter from the AI
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        
        if json_match:
            clean_json = json_match.group(0)
            return json.loads(clean_json)
        else:
            # Fallback if the AI completely fails to send JSON
            raise ValueError("AI response did not contain a valid JSON block.")
            
    except Exception as e:
        # Returns a safe error report to the UI instead of crashing
        return {
            "score": 0,
            "verdict": "Parsing Error",
            "trust_label": "Technical Issue",
            "summary": f"The Forensic Engine encountered an error: {str(e)}",
            "red_flags": ["Could not parse AI response", "Check API or JSON format"]
        }