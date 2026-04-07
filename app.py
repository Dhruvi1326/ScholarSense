import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="ScholarSense", layout="wide", page_icon="🧬")

# --- CLOUD CONFIGURATION ---
# Your Live Google Cloud Backend
BACKEND_URL = "https://scholarsense-api-326425862435.us-central1.run.app"

# --- CUSTOM CSS (Enhanced Pastel Zen Theme) ---
st.markdown("""
    <style>
    .stApp { background-color: #F7F3F0; color: #4A4A4A; }
    section[data-testid="stSidebar"] { background-color: #EDE7E3; border-right: 1px solid #D8D2D0; }
    .stButton>button { border-radius: 12px; background-color: #F8D7DA; color: #4A4A4A; border: none; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #F1C0C4; transform: translateY(-1px); }
    div[data-testid="stExpander"] { background-color: #FFFFFF; border-radius: 15px; border: 1px solid #EAEAEA !important; }
    .result-card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; border-left: 5px solid #F1C0C4; margin-bottom: 15px; border: 1px solid #EAEAEA; }
    div[data-testid="stMetricValue"] { color: #D63384; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🧬 ScholarSense")
    st.caption("Forensic Research Auditor v2.0 (Cloud)")
    st.divider()
    clinical_mode = st.toggle("Clinical Translation Mode", value=False)
    st.info("Mode: " + ("Regulatory Guardrails" if clinical_mode else "Academic Rigor"))

# --- Main Layout ---
st.title("Research Integrity Command Center")
tab1, tab2, tab3 = st.tabs(["📄 Forensic PDF Audit", "🔍 Neural Discovery", "📚 Research Library"])

# --- TAB 1: PDF AUDIT (Synced with FastAPI main.py) ---
with tab1:
    uploaded_file = st.file_uploader("Upload Research Paper for Forensic Audit", type="pdf")
    if uploaded_file:
        with st.status("Performing Forensic Analysis...", expanded=True) as status:
            st.write("Preparing Document for Cloud AI Engine...")
            
            # --- PRO-TIP IMPLEMENTATION: MULTIPART FORM DATA ---
            # We send the raw file bytes + form data strings
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            data = {"clinical_mode": "true" if clinical_mode else "false"}
            
            try:
                # Door Fix: Switched from /papers/ to /audit/ to match main.py
                response = requests.post(f"{BACKEND_URL}/audit/", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    # Mapping the response from your FastAPI 'audit_paper' logic
                    report = result.get('audit_report', {})
                    
                    status.update(label="Audit Complete & Indexed!", state="complete")
                    
                    # UI RESULTS
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric("Integrity Score", f"{report.get('final_score', 'N/A')}/100")
                        st.subheader(f"Label: {report.get('trust_level', 'Unknown')}")
                        if report.get('final_score', 0) > 85: st.balloons()
                    
                    with col2:
                        st.markdown(f"### **Verdict:** {report.get('verdict', 'No verdict generated.')}")
                        st.write(f"**Registry Status:** {report.get('registry', 'Unverified')}")
                        with st.expander("🚩 View Scientific Red Flags"):
                            flags = report.get('red_flags', [])
                            if flags:
                                for flag in flags:
                                    st.write(f"- {flag}")
                            else:
                                st.write("No major red flags detected.")
                else:
                    st.error(f"Backend Error ({response.status_code}): {response.text}")
                    status.update(label="Audit Failed", state="error")
                    
            except Exception as e:
                st.error(f"Connection Failed: Ensure your Cloud Run Service is Active. Error: {e}")
                status.update(label="Connection Error", state="error")

# --- TAB 2: NEURAL DISCOVERY (Placeholder for Search Endpoint) ---
with tab2:
    st.header("🔍 Neural Memory Discovery")
    query = st.text_input("Ask ScholarSense about your indexed papers...", placeholder="e.g., Gantrez formulations")
    
    if query:
        st.info("Neural Search endpoint (/search) is currently being initialized on Cloud Run.")

# --- TAB 3: RESEARCH LIBRARY (Placeholder for Library Endpoint) ---
with tab3:
    st.header("📚 Your Audited Collection")
    if st.button("Refresh Library"):
        st.warning("History endpoint (/papers) is currently being migrated to the Cloud DB.")