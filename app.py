import streamlit as st
import requests
import ai_engine
import document_processor
import os

st.set_page_config(page_title="ScholarSense", layout="wide")

# --- Glassmorphism CSS ---
st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    div[data-testid="stExpander"] { background: rgba(255, 255, 255, 0.05); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar & Toggle ---
with st.sidebar:
    st.title("🧬 ScholarSense")
    clinical_mode = st.toggle("Clinical Translation Mode", value=False)
    st.divider()
    st.info("Mode: " + ("Regulatory Guardrails" if clinical_mode else "Academic Rigor"))

# --- Main Layout ---
st.title("Research Integrity Command Center")
tab1, tab2 = st.tabs(["📄 Forensic PDF Audit", "🔍 Semantic Search"])

with tab1:
    uploaded_file = st.file_uploader("Upload Research Paper", type="pdf")
    if uploaded_file:
        # 1. Save temp file
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.status("Performing Forensic Analysis...", expanded=True) as status:
            st.write("Uploading to Gemini 2.5 Flash...")
            gemini_file = document_processor.upload_to_gemini("temp.pdf")
            
            st.write("Auditing Methodology & Data...")
            report = ai_engine.audit_full_document(gemini_file, clinical_mode)
            status.update(label="Audit Complete!", state="complete")

        # --- RESULTS UI ---
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Integrity Score", f"{report['score']}/100")
            st.subheader(f"Label: {report['trust_label']}")
        
        with col2:
            st.write(f"**Verdict:** {report['verdict']}")
            st.write(f"**Summary:** {report['summary']}")
            with st.expander("🚩 View Scientific Red Flags"):
                for flag in report['red_flags']:
                    st.write(f"- {flag}")

with tab2:
    st.header("🔍 Neural Memory Discovery")
    query = st.text_input("Ask ScholarSense about your indexed papers...", placeholder="e.g., Swelling rates of Gantrez formulations")
    
    if query:
        with st.spinner("Searching Vector Database..."):
            try:
                # call the FastAPI endpoint 
                response = requests.get(f"http://localhost:8000/search/?query={query}")
                results = response.json()
                
                if results:
                    for res in results:
                        with st.container():
                            # Modern 'Card' look for search results
                            st.markdown(f"""
                            <div style="background-color: #161b22; padding: 20px; border-radius: 10px; border-left: 5px solid #2e7af1; margin-bottom: 10px;">
                                <h4 style="margin:0;">{res['title']}</h4>
                                <p style="color: #8b949e; margin: 5px 0;">Relevance: {res['relevance']} | Integrity Score: {res['score']}/100</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.info("No matching research found in local memory.")
            except Exception as e:
                st.error("Connection to Backend failed. Is uvicorn running?")