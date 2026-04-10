import os
import uuid
import time
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

load_dotenv()

# Configuration
QDRANT_URL = "https://144a8e84-2a9f-4e27-b417-5953265687a5.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "scholar_papers_v1"
MODEL_PATH = "./model_cache" # Must match Dockerfile

# --- 1. PRO-LEVEL MODEL LOADING ---
# We point to the local folder we "baked" in the Dockerfile
os.environ["SENTENCE_TRANSFORMERS_HOME"] = MODEL_PATH

# Global placeholders to prevent boot-time hang
_model = None
_client = None

def get_model():
    global _model
    if _model is None:
        # Load from local cache folder only
        _model = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=MODEL_PATH)
    return _model

def get_client():
    global _client
    if _client is None:
        _client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
            port=443,
            https=True,
            timeout=60
        )
    return _client

# --- 2. LAZY INITIALIZATION ---
def initialize_vector_db():
    """Checks for collection only when called, not at import."""
    try:
        client = get_client()
        collections = client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("✅ Cloud Collection Ready!")
    except Exception as e:
        print(f"⚠️ Cloud Sync Warning: {e}")

def add_to_vector_store(paper_id, title, abstract, integrity_score):
    """Converts the paper into a vector and saves it to Qdrant Cloud."""
    client = get_client()
    model = get_model()
    
    text_to_embed = f"Title: {title}. Abstract: {abstract}"
    vector = model.encode(text_to_embed).tolist()
    
    if isinstance(paper_id, int):
        point_id = paper_id
    else:
        point_id = int(uuid.uuid5(uuid.NAMESPACE_DNS, str(paper_id)).int >> 96)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "original_id": str(paper_id),
                    "title": title, 
                    "abstract": abstract[:500],
                    "integrity_score": float(integrity_score)
                }
            )
        ]
    )
    print(f"✅ Paper '{title}' indexed in Qdrant Cloud.")