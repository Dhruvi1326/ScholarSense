# ScholarSense 🧬  
**Autonomous Forensic Auditor for Research Integrity & Clinical Translation** *Engineered by a PhD Researcher to bridge the gap between Academic Rigor and Production-Grade AI.*

ScholarSense is a high-performance, cloud-native platform designed to solve the "Trust Gap" in academic publishing. It moves beyond simple search, acting as an automated auditor that cross-verifies abstract claims against deep-text data and modern regulatory standards (FDA/EMA).

## 🚀 [LIVE DEMO: Access ScholarSense Here](https://scholarsense.streamlit.app)
*(Note: Use the Live Demo to experience real-time forensic auditing and neural discovery.)*

---

## 🏗️ Technical Architecture & Cloud Infrastructure
ScholarSense is architected as a decoupled, scalable microservices ecosystem hosted on **Google Cloud Platform (GCP)**.

* **Brain (Backend API):** FastAPI (Python 3.12+) deployed via **Google Cloud Run**.
* **Face (Frontend):** Streamlit Cloud, delivering a "Glassmorphism" Command Center for researchers.
* **Memory (Persistence):** * **Relational:** Google Cloud SQL (PostgreSQL) for transactional research history.
    * **Vector:** Qdrant Cloud for high-dimensional semantic fingerprints ($d=768$).
* **AI Engine:** Gemini 2.0 Flash via Multimodal File API for full-document forensic vision.
* **DevOps:** Automated CI/CD pipeline via **Google Cloud Build**, implementing a "Container-First" strategy.

---

## 🔬 Senior Engineering Highlights
* **Scale-to-Zero Architecture:** Optimized Cloud Run configurations to ensure 99% cost efficiency while maintaining high-speed file streaming via `python-multipart`.
* **Hybrid Persistence Layer:** Engineered a dynamic environment-aware database switch (SQLite for local development / PostgreSQL for production).
* **Domain-Specific Guardrails:** Developed a "Clinical Translation Toggle" that audits research feasibility against 2026 FDA/EMA sterilization and GMP standards—critical for Pharmaceutical & Microneedle technology.
* **Zero-Trust Security:** Fully integrated **GCP Secret Manager** to eliminate hardcoded credentials, ensuring enterprise-grade security for API keys and database strings.

---

## 🧪 Benchmark Case Study: The "Prausnitz" Stress Test
We audited the foundational review: **'Microneedles for drug and vaccine delivery'** (*Kim, Park, & Prausnitz, 2012*).

| Audit Mode | Integrity Score | Forensic Verdict | Key Clinical Insight |
| :--- | :--- | :--- | :--- |
| **Academic Rigor** | **95/100** | **Excellent** | Verified 350+ citations and robust historical methodology. |
| **Clinical Translation** | **80/100** | **Comprehensive** | Flagged 2012 regulatory gaps vs. 2026 GMP manufacturing standards. |

---

## 🛠️ Installation & Local Development

1. Clone the Repository:
   ```bash
   git clone [https://github.com/your-username/ScholarSense.git](https://github.com/dhruvi1326/ScholarSense.git)
   cd ScholarSense
2. Set Up Environment Variables:
   Create a .env file in the root directory and add:
   GEMINI_API_KEY=your_key_here
   DATABASE_URL=your_sql_url_here
   QDRANT_URL=your_qdrant_url_here
3. Install Dependencies:
   pip install -r requirements.txt
5. Launch the Engine:
   uvicorn main:app --reload

## 👨‍🔬 About the Developer
Currently a **PhD Scholar** and *, I have transitioned into **Full-Stack Cloud Engineering** to build high-performance tools for academic and professional use. ScholarSense represents the culmination of this journey—applying modern software architecture and AI to solve real-world challenges in research integrity.

---
🗺️ Roadmap
[x] Phase 4: Cloud Migration (FastAPI to Google Cloud Run).

[x] Phase 5: CI/CD Integration (Google Cloud Build).

[x] Phase 6: Persistent Cloud Storage (Google Cloud SQL).

[ ] Phase 9: Secure Scholar Access — Implementing OAuth2 (Google Identity) for private research vaults.
