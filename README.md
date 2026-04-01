# ScholarSense 🧬
**AI-Powered Research Integrity & Citation Management**

ScholarSense is a high-performance platform designed to solve the "Trust Gap" in academic publishing. It audits scientific methodology and automates citation workflows using cutting-edge Generative AI.

---

## 🚀 Phase 1: Foundations & The "Brain" (Complete)

### System Architecture & Data Bedrock
- **Backend:** FastAPI (Python) with Async I/O for high-concurrency research queries.
- **Database:** Relational SQLite with SQLAlchemy ORM (Architected for seamless migration to Google Cloud SQL).
- **Environment:** Isolated workspace using `venv` and Secret Management via `.env` (Security First).
- **Tooling:** Development via Cursor AI and API testing via Bruno.

### Advanced AI Integration (The Nature Auditor)
- **Model:** Integrated **Gemini 2.5 Flash** (Bleeding-edge LLM) for automated peer review.
- **Dynamic Discovery:** Implemented runtime model discovery to ensure the system always utilizes the most advanced available Google AI model.
- **Audit Protocol:** Engineered a custom weighted prompt system to score research based on:
    - **Methodology (40%)**
    - **Data Transparency (30%)**
    - **Logical Coherence (20%)**
    - **Novelty (10%)**
- **Robustness:** Built-in JSON sanitization and fallback logic to handle stochastic AI outputs without system failure.

---

## 🛠️ Academic & Tech Alignment
- **Harvard CS50:** Implementing Data Abstraction, RESTful design patterns, and SQL integrity.
- **Google Cloud:** Architected for horizontal scalability, secure IAM management, and FinOps optimization (maximizing the $300 GCP credit lifecycle).

---

## 📈 Current Status: 🟢 Backend API Live
- [x] Database Schema Design & Migrations
- [x] CRUD Operations for Research Papers
- [x] Gemini 2.5 AI Audit Engine
- [ ] Crossref DOI Verification (Upcoming)
- [ ] Docker Containerization (Upcoming)
