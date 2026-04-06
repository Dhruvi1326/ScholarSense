# ScholarSense 🧬
**The AI-Powered Forensic Auditor for Research Integrity**

ScholarSense is a high-performance, full-stack platform designed to solve the "Trust Gap" in academic publishing. It doesn't just search—it audits. By combining **Vector Discovery** with **Multimodal AI Forensics**, ScholarSense cross-verifies abstract claims against deep-text data to ensure scientific rigor.

---

## 🚀 Status: 🟢 Production Ready (Phase 1 & 2 Complete)

### 🔬 Advanced AI Forensics (The Scientific Auditor)
- **Engine:** Integrated **Gemini 2.5 Flash** with native **Multimodal PDF Processing** for full-document vision.
- **Clinical Translation Toggle:** A domain-specific guardrail that audits research against **FDA/EMA** human feasibility and skin-safety standards (specialized for Pharmaceutical Sciences).
- **Automated Discrepancy Detection:** Cross-references Abstract claims with Results tables to flag "Data Overstatements."

### 🧠 Neural Discovery & Memory
- **Semantic Search:** **Qdrant Vector Database** running in Docker for "Conceptual Discovery" (finding papers by meaning, not just keywords).
- **Embeddings:** High-dimensional mapping using `all-mpnet-base-v2` for 768-dimension scientific fingerprints.
- **Truth Layer:** Real-time **Crossref DOI** verification and metadata reconciliation.

### 🎨 Modern UX/UI Dashboard
- **Interface:** High-performance **Streamlit** dashboard with **Glassmorphism** design.
- **Real-time Metrics:** Animated Integrity Gauges and Forensic Risk labels (Gold Standard, Credible, High Risk).
- **Product Architecture:** Full-stack integration of FastAPI (Backend Brain) and Streamlit (Frontend Command Center).

---

## 🧪 Case Study: The "Prausnitz" Stress Test
To verify the engine's ability to distinguish between academic merit and clinical reality, we audited the foundational review: **'Microneedles for drug and vaccine delivery'** (*Kim, Park, & Prausnitz, 2012*).

| Audit Mode | Integrity Score | Forensic Verdict | Key Clinical Insight |
| :--- | :--- | :--- | :--- |
| **Academic Rigor** | **95/100** | **Excellent** | Verified 350+ citations and robust historical methodology. |
| **Clinical Translation** | **80/100** | **Comprehensive** | Flagged 2012 regulatory gaps and GMP manufacturing hurdles for 2026 standards. |

**Observation:** ScholarSense successfully identified that while the paper is a "Gold Standard" for researchers, the specific manufacturing scalability and modern FDA sterilization protocols required for human translation were (expectedly) less emphasized in this 2012 text.

---

## 📚 Features: Research Vault & History
The platform now includes a persistent **Research Library** allowing users to:
- **Recall Audits:** Instant access to past scores and "Red Flags" without re-uploading PDFs.
- **Neural Memory:** Automated indexing into **Qdrant** for conceptual retrieval.
- **Hybrid Storage:** Uses SQLite for structured metadata and Vector Embeddings for semantic discovery.

---

## 📈 Tech Stack & Alignment
- **Language:** Python 3.14 (Optimized for latest library concurrency).
- **AI Engine:** Gemini 2.5 Flash (Multimodal Vision + File API).
- **Backend:** FastAPI with Async I/O.
- **Vector DB:** Qdrant (HNSW Indexing) via Docker.
- **UI:** Streamlit (Custom Zen-Pastel Glassmorphism).
- **Academic Alignment:** Developed during PhD candidacy to address real-world gaps in pharmaceutical document verification.

---

## ✅ Milestones
- [x] Database Schema & Neural Memory Indexing
- [x] Gemini 2.5 Multimodal Audit Engine
- [x] **Forensic PDF Analysis:** Full-text vision vs. simple text scraping.
- [x] **Clinical Regulatory Toggle:** Domain-specific AI guardrails.
- [x] **Live Web Deployment:** Accessible via Streamlit Community Cloud.
- [x] **Research Library & History:** Persistent local audit storage.
