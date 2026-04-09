import streamlit as st
import requests
import os
import json

st.set_page_config(page_title="ScholarSense", layout="wide", page_icon="🧬")

# --- CLOUD CONFIGURATION ---
BACKEND_URL = "https://scholarsense-api-326425862435.us-central1.run.app"

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #F7F3F0; color: #4A4A4A; }
    section[data-testid="stSidebar"] { background-color: #EDE7E3; border-right: 1px solid #D8D2D0; }
    .stButton>button { border-radius: 12px; background-color: #F8D7DA; color: #4A4A4A; border: none; transition: all 0.3s ease; }
    div[data-testid="stMetricValue"] { color: #D63384; }
    .result-card { background-color: #FFFFFF; padding: 20px; border-radius: 15px; border: 1px solid #EAEAEA; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("🧬 ScholarSense")
    st.caption("Forensic Research Auditor v2.0 (Cloud)")
    st.divider()
    clinical_mode = st.toggle("Clinical Translation Mode", value=False)
    st.info("Mode: " + ("Regulatory Guardrails" if clinical_mode else "Academic Rigor"))

st.title("Research Integrity Command Center")
tab1, tab2, tab3 = st.tabs(["📄 Forensic PDF Audit", "🔍 Neural Discovery", "📚 Research Library"])

# --- TAB 1: PDF AUDIT (Fixed Mapping) ---
with tab1:
    uploaded_file = st.file_uploader("Upload Research Paper for Forensic Audit", type="pdf")
    if uploaded_file:
        with st.status("Performing Forensic Analysis...", expanded=True) as status:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            data = {"clinical_mode": "true" if clinical_mode else "false"}
            
            try:
                response = requests.post(f"{BACKEND_URL}/audit/", files=files, data=data)
                
                if response.status_code == 200:
                    # FIX: Your main.py returns the audit dict directly, NOT nested in 'audit_report'
                    audit_result = response.json()
                    
                    status.update(label="Audit Complete & Indexed!", state="complete")
                    
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        # Updated keys to match your main.py / ai_engine.py output
                        st.metric("Integrity Score", f"{audit_result.get('final_score', 'N/A')}/100")
                        st.subheader(f"Trust: {audit_result.get('trust_level', 'Unknown')}")
                    
                    with col2:
                        st.markdown(f"### **Verdict:** {audit_result.get('verdict', 'No verdict generated.')}")
                        # Display Red Flags if they exist
                        with st.expander("🚩 View Scientific Red Flags"):
                            flags = audit_result.get('red_flags', [])
                            if flags:
                                for flag in flags: st.write(f"- {flag}")
                            else: st.write("No major red flags detected.")
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- TAB 2: NEURAL DISCOVERY (Now Functional) ---
with tab2:
    st.header("🔍 Neural Memory Discovery")
    query = st.text_input("Ask ScholarSense about your indexed papers...", placeholder="e.g., Gantrez formulations")
    
    if query:
        with st.spinner("Searching Vector Memory..."):
            res = requests.get(f"{BACKEND_URL}/search", params={"q": query})
            if res.status_code == 200:
                results = res.json()
                for r in results:
                    with st.container():
                        st.markdown(f"### {r['title']}")
                        st.write(f"**Relevance:** {round(r['score']*100, 2)}% | **Integrity:** {r['integrity_score']}/100")
                        st.write(r['abstract'])
                        st.divider()

# --- TAB 3: RESEARCH LIBRARY (Now Functional) ---
with tab3:
    st.header("📚 Your Audited Collection")
    if st.button("Refresh Library"):
        res = requests.get(f"{BACKEND_URL}/papers")
        if res.status_code == 200:
            papers = res.json()
            for p in papers:
                st.markdown(f"""
                <div class='result-card'>
                    <h4>{p['title']}</h4>
                    <p><b>Score:</b> {p['integrity_score']}/100 | <b>Trust:</b> {p['trust_level']}</p>
                    <p><i>{p['verdict']}</i></p>
                </div>
                """, unsafe_allow_html=True)