import streamlit as st
import requests
import document_processor
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
    st.caption("Forensic Research Auditor v1.5")
    st.divider()
    clinical_mode = st.toggle("Clinical Translation Mode", value=False)
    st.info("Mode: " + ("Regulatory Guardrails" if clinical_mode else "Academic Rigor"))

# --- Main Layout ---
st.title("Research Integrity Command Center")
tab1, tab2, tab3 = st.tabs(["📄 Forensic PDF Audit", "🔍 Neural Discovery", "📚 Research Library"])

# --- TAB 1: PDF AUDIT (Now saves to Cloud) ---
with tab1:
    uploaded_file = st.file_uploader("Upload Research Paper for Forensic Audit", type="pdf")
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.status("Performing Forensic Analysis...", expanded=True) as status:
            st.write("Extracting Text from PDF...")
            # Using your existing local processor to get text
            text_content = document_processor.extract_text("temp.pdf") 
            
            st.write("Syncing with Google Cloud AI Engine...")
            # Prepare data for the Backend POST request
            payload = {
                "title": uploaded_file.name,
                "abstract": text_content[:4000], # Send first 4000 chars for audit
                "doi": f"REF-{hash(uploaded_file.name)}" # Generate unique ref
            }
            
            try:
                # Trigger the full audit + database save + vector indexing
                response = requests.post(f"{BACKEND_URL}/papers/", json=payload)
                if response.status_code == 200:
                    data = response.json()
                    report = data['audit_report']
                    db_record = data['data']
                    status.update(label="Audit Complete & Indexed!", state="complete")
                    
                    # UI RESULTS
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.metric("Integrity Score", f"{report['final_score']}/100")
                        st.subheader(f"Label: {report['trust_level']}")
                        if report['final_score'] > 85: st.balloons()
                    
                    with col2:
                        st.markdown(f"### **Verdict:** {report['verdict']}")
                        st.write(f"**Registry Status:** {report['registry']}")
                        with st.expander("🚩 View Scientific Red Flags"):
                            for flag in report['red_flags']:
                                st.write(f"- {flag}")
                else:
                    st.error(f"Backend Error: {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# --- TAB 2: NEURAL DISCOVERY (Cloud Vector Search) ---
with tab2:
    st.header("🔍 Neural Memory Discovery")
    query = st.text_input("Ask ScholarSense about your indexed papers...", placeholder="e.g., Gantrez formulations")
    
    if query:
        with st.spinner("Searching Vector Database in Virginia..."):
            try:
                response = requests.get(f"{BACKEND_URL}/search/", params={"query": query, "limit": 3})
                results = response.json()
                
                if isinstance(results, list):
                    for res in results:
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="margin:0;">{res['title']}</h4>
                            <p style="color: #8E8E8E; margin: 5px 0;">
                                <b>Relevance:</b> {res['relevance']} | 
                                <b>Stored Integrity:</b> <span style="color:#D63384;">{res['score']}/100</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No matching research found.")
            except Exception as e:
                st.error("Could not reach Neural Memory.")

# --- TAB 3: RESEARCH LIBRARY (SQL Cloud History) ---
with tab3:
    st.header("📚 Your Audited Collection")
    if st.button("Refresh Library"):
        try:
            # This fetches from the SQLite database running on Google Cloud
            history_response = requests.get(f"{BACKEND_URL}/papers/")
            papers = history_response.json()
            
            if papers:
                for paper in reversed(papers):
                    with st.expander(f"📄 {paper['title']} (Score: {paper['integrity_score']}/100)"):
                        st.write(f"**DOI/Ref:** {paper['doi']}")
                        st.info(f"**AI Audit Log:** {paper['citation_apa']}")
            else:
                st.info("Library is empty.")
        except Exception:
            st.warning("Database offline.")