# ScholarSense 🧬
**AI-Powered Research Integrity & Semantic Discovery Engine**

ScholarSense is a high-performance platform designed to address the "Trust Gap" in academic publishing. It audits scientific methodology, verifies registries, and enables conceptual discovery using cutting-edge Vector Search and Generative AI.

---

## 🚀 Phase 1: Foundations & The "Neural Brain" (Complete)

### System Architecture & Data Bedrock
- **Backend:** FastAPI (Python) with Async I/O for high-concurrency research queries.
- **Relational DB:** SQLite with SQLAlchemy ORM (Architected for Google Cloud SQL migration).
- **Vector Memory:** **Qdrant (Vector Database)** running in Docker for high-dimensional semantic similarity.
- **Embeddings:** Utilizing `all-mpnet-base-v2` via `sentence-transformers` for 768-dimension scientific mapping.

### Advanced AI Integration (The Scientific Auditor)
- **Model:** Integrated **Gemini 2.5 Flash** for automated, skeptical peer review.
- **Robust Scoring Logic:** A "Fairness-First" hybrid system that balances AI content analysis with **Crossref DOI** registry verification.
- **Expert Signature Detection:** Engineered prompts to distinguish between "keyword-stuffed" abstracts and high-impact methodology.

### Containerization & DevOps
- **Dockerized Environment:** Multi-container orchestration (FastAPI + Qdrant).
- **Security:** Strict `.env` management and secure environment mapping for API keys.
- **Tooling:** Development via Cursor AI; API testing & documentation via Bruno.

---

## 📈 Current Status: 🟢 Intelligence Layer Active
- [x] Database Schema & Migrations
- [x] Gemini 2.5 AI Audit Engine (Methodology & Logic)
- [x] Crossref DOI Verification 
- [x] **Semantic Discovery:** Vector-based search by concept, not just keywords.
- [x] Docker Containerization (App + Vector DB)
- [ ] Phase 2: PDF Full-Text Forensic Analysis (Upcoming)
- [ ] Phase 3: Frontend Dashboard & Visualization (Upcoming)
