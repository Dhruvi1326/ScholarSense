import streamlit as st
import requests
import ai_engine
import document_processor
import os

st.set_page_config(page_title="ScholarSense", layout="wide", page_icon="🧬")

# --- CUSTOM CSS (Enhanced Pastel Zen Theme) ---
st.markdown("""
    <style>
    /* Main Background and Text */
    .stApp {
        background-color: #F7F3F0; /* Soft Beige */
        color: #4A4A4A; /* Charcoal Gray */
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #EDE7E3;
        border-right: 1px solid #D8D2D0;
    }

    /* Buttons */
    .stButton>button {
        border-radius: 12px;
        background-color: #F8D7DA; /* Soft Pastel Pink */
        color: #4A4A4A;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #F1C0C4;
        transform: translateY(-1px);
    }

    /* Cards and Expanders */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border-radius: 15px;
        border: 1px solid #EAEAEA !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* History & Search Cards */
    .result-card {
        background-color: #FFFFFF;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #F1C0C4;
        margin-bottom: 15px;
        border-top: 1px solid #EAEAEA;
        border-right: 1px solid #EAEAEA;
        border-bottom: 1px solid #EAEAEA;
    }

    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #D63384;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        color: #8E8E8E;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #D63384 !important;
        border-bottom-color: #D63384 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar & Toggle ---
with st.sidebar:
    st.title("🧬 ScholarSense")
    st.caption("Forensic Research Auditor v1.5")
    st.divider()
    
    clinical_mode = st.toggle("Clinical Translation Mode", value=False)
    st.info("Mode: " + ("Regulatory Guardrails" if clinical_mode else "Academic Rigor"))
    


# --- Main Layout ---
st.title("Research Integrity Command Center")
tab1, tab2, tab3 = st.tabs(["📄 Forensic PDF Audit", "🔍 Neural Discovery", "📚 Research Library"])

with tab1:
    uploaded_file = st.file_uploader("Upload Research Paper for Forensic Audit", type="pdf")
    if uploaded_file:
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
            if report['score'] > 85:
                st.balloons()
        
        with col2:
            st.markdown(f"### **Verdict:** {report['verdict']}")
            st.write(f"**Summary:** {report['summary']}")
            with st.expander("🚩 View Scientific Red Flags & Gaps"):
                for flag in report['red_flags']:
                    st.write(f"- {flag}")

with tab2:
    st.header("🔍 Neural Memory Discovery")
    query = st.text_input("Ask ScholarSense about your indexed papers...", placeholder="e.g., Swelling rates of Gantrez formulations")
    
    if query:
        with st.spinner("Searching Vector Database..."):
            try:
                # Call the FastAPI endpoint 
                response = requests.get(f"http://localhost:8000/search/?query={query}")
                results = response.json()
                
                if results:
                    for res in results:
                        st.markdown(f"""
                        <div class="result-card">
                            <h4 style="margin:0; color: #4A4A4A;">{res['title']}</h4>
                            <p style="color: #8E8E8E; margin: 5px 0;">
                                <b>Relevance:</b> {res['relevance']} | 
                                <b>Integrity Score:</b> <span style="color:#D63384;">{res['score']}/100</span>
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("No matching research found in neural memory.")
            except Exception as e:
                st.error("Connection to Backend failed. Is uvicorn running?")

with tab3:
    st.header("📚 Your Audited Collection")
    st.markdown("Revisit your past audits and clinical feasibility reports.")
    
    try:
        # Fetch paper history from your SQLite database via FastAPI
        history_response = requests.get("http://localhost:8000/papers/")
        papers = history_response.json()
        
        if papers:
            # Show newest first
            for paper in reversed(papers):
                with st.expander(f"📄 {paper['title']} (Score: {paper['score']}/100)"):
                    hcol1, hcol2 = st.columns([1, 2])
                    with hcol1:
                        st.metric("Trust Label", paper['trust_label'])
                        st.write(f"**Status:** {'🚀 Clinical Ready' if paper['score'] > 80 else '⚠️ Research Only'}")
                    with hcol2:
                        st.write(f"**Forensic Verdict:** {paper['verdict']}")
                        st.info(f"**Summary:** {paper['summary']}")
                        st.write("**Identified Flags:**")
                        for flag in paper['red_flags']:
                            st.write(f"• {flag}")
        else:
            st.info("Your library is empty. Audited papers will appear here automatically.")
    except Exception:
        st.warning("Database connection unavailable. Library history is currently offline.")