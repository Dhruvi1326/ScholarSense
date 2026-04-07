# ScholarSense 🧬 
**The AI-Powered Forensic Auditor for Research Integrity**

ScholarSense is a high-performance, cloud-native platform designed to solve the "Trust Gap" in academic publishing. It doesn't just search—it audits. By combining **Vector Discovery** with **Multimodal AI Forensics**, ScholarSense cross-verifies abstract claims against deep-text data to ensure scientific rigor.

---

## 🚀 Status: 🔵 Phase 4 & 5 Complete (Cloud-Native Infrastructure)
**ScholarSense has successfully migrated from local environments to a scalable, production-grade Google Cloud Architecture.**

### 🔬 Advanced AI Forensics (The Scientific Auditor)
* **Engine:** Integrated **Gemini 2.0 Flash** with native **Multimodal PDF Processing** for full-document vision.
* **Clinical Translation Toggle:** A domain-specific guardrail auditing research against **FDA/EMA** feasibility and skin-safety standards (specialized for Pharmaceutical Sciences & Microneedle technology).
* **Automated Discrepancy Detection:** Cross-references Abstract claims with Results tables to flag "Data Overstatements."

### 🧠 Neural Discovery & Memory
* **Semantic Search:** **Qdrant Vector Database** (Cloud/Managed) for "Conceptual Discovery"—finding papers by meaning, not just keywords.
* **Embeddings:** High-dimensional mapping using `all-MiniLM-L6-v2` for 768-dimension scientific fingerprints.
* **Truth Layer:** Real-time metadata reconciliation via persistent storage and automated SQL indexing.

### 🎨 Modern UX/UI Dashboard
* **Interface:** High-performance **Streamlit** dashboard with **Glassmorphism** design elements.
* **Real-time Metrics:** Animated Integrity Gauges and Forensic Risk labels (Gold Standard, Credible, High Risk).
* **Product Architecture:** Full-stack integration of FastAPI (Backend Brain) and Streamlit (Frontend Command Center).

---

## 🧪 Case Study: The "Prausnitz" Stress Test
To verify the engine's ability to distinguish between academic merit and clinical reality, we audited the foundational review: **'Microneedles for drug and vaccine delivery'** (*Kim, Park, & Prausnitz, 2012*).

| Audit Mode | Integrity Score | Forensic Verdict | Key Clinical Insight |
| :--- | :--- | :--- | :--- |
| **Academic Rigor** | **95/100** | **Excellent** | Verified 350+ citations and robust historical methodology. |
| **Clinical Translation** | **80/100** | **Comprehensive** | Flagged 2012 regulatory gaps and GMP manufacturing hurdles for 2026 standards. |

**Observation:** ScholarSense identified that while the paper is a "Gold Standard," the manufacturing scalability and modern FDA sterilization protocols required for human translation in 2026 were (expectedly) less emphasized in this 2012 text.

---

## 📈 Tech Stack & Infrastructure
* **Cloud Platform:** Google Cloud Platform (GCP)
* **Orchestration:** **Google Cloud Run** (Serverless Auto-scaling)
* **CI/CD:** **Google Cloud Build** (Automated Containerization)
* **Backend:** FastAPI (Python 3.12+) with `python-multipart` high-speed file streaming.
* **Storage:** Hybrid Persistence (SQLite for Metadata + Qdrant for Vectors).
* **AI Engine:** Gemini 2.0 Flash (Multimodal Vision + File API).

---

## 🗺️ Roadmap
* [x] **Phase 4:** Cloud Migration (FastAPI to Google Cloud Run).
* [x] **Phase 5:** CI/CD Integration (Google Cloud Build).
* [ ] **Phase 8:** Frontend Cloud Hosting (Streamlit on Google Cloud).
* [ ] **Phase 9: Secure Scholar Access** — Implementing **OAuth2 (Google Identity)** for private research vaults.

---

## ✅ Deployment Notes
To deploy this architecture to Google Cloud:
```bash
# Bake the Container
gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT_ID/repo/api:latest

# Deploy with AI-Optimized Resources
gcloud run deploy scholarsense-api \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/repo/api:latest \
  --memory 2Gi --cpu 1 --timeout 300
