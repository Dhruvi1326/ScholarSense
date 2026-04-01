import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# 1. DEBUG: This will print every model your key can actually use
print("Checking available models...")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"AVAILABLE MODEL: {m.name}")

# 2. Set the model to the standard Flash identifier
model = genai.GenerativeModel('models/gemini-2.5-flash')

def evaluate_paper_integrity(title: str, abstract: str):
    prompt = f"""
    SYSTEM ROLE: You are the Lead Auditor for a High-Impact Nature Portfolio Journal. 
    Your objective is to identify 'Paper Mill' characteristics, methodology gaps, and data inconsistencies. 
    You are cynical, evidence-based, and unimpressed by broad claims.

    INPUT DATA:
    - Title: {title}
    - Abstract: {abstract}
    
    AUDIT PROTOCOL (Strict Deductive Scoring):
    1. SPECIFICITY (40%): Is there a named model/chemical/protocol? If it only uses vague terms like "AI techniques" or "optimization," score < 10.
    2. REPRODUCIBILITY (30%): Does the abstract provide enough parameters (n, concentration, duration, epochs) for a peer to replicate?
    3. LOGICAL COHERENCE (20%): Do the results flow directly from the described methods?
    4. CITATION READINESS (10%): Is the DOI-worthy discovery clearly stated?

    OUTPUT RULES:
    - Return ONLY a JSON object.
    - If the abstract is a 'placeholder' or 'vague summary', the verdict must be 'Low Integrity' or 'Predatory'.
    
    STRUCTURE:
    {{
        "score": (int),
        "summary": "Focus on the critical methodological absence.",
        "verdict": "High/Medium/Low/Predatory"
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        
        # Clean markdown if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].strip()
            
        return json.loads(text)
    except Exception as e:
        print(f"AI Error: {e}")
        return {"score": 50, "summary": "AI connection pending.", "verdict": "Medium"}