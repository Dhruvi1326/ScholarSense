import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# --- CLOUD CONFIGURATION ---
# These will be filled by the 'gcloud run deploy' command automatically
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY
)

COLLECTION_NAME = "audited_papers"

# Load the model (Wait time expected here during first run)
model = SentenceTransformer('all-mpnet-base-v2')

def initialize_vector_db():
    """Sets up the collection for our academic vectors."""
    try:
        collections = client.get_collections().collections
        exists = any(c.name == COLLECTION_NAME for c in collections)
        
        if not exists:
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=768, distance=Distance.COSINE),
            )
            print(f"✅ Collection '{COLLECTION_NAME}' created.")
    except Exception as e:
        print(f"⚠️ Vector DB Check failed: {e}. (This is normal if URL is not yet set)")

def add_to_vector_store(paper_id, title, abstract, integrity_score):
    """Converts the paper into a vector and saves it."""
    text_to_embed = f"Title: {title}. Abstract: {abstract}"
    vector = model.encode(text_to_embed).tolist()
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=paper_id,
                vector=vector,
                payload={"title": title, "integrity_score": float(integrity_score)}
            )
        ]
    )
    print(f"🚀 Paper {paper_id} indexed.")