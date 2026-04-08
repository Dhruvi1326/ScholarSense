from sentence_transformers import SentenceTransformer
import os
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


load_dotenv()

# Let's use a more robust connection setup
QDRANT_URL = "https://144a8e84-2a9f-4e27-b417-5953265687a5.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Create the client with an increased timeout and explicit port
client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    port=443,     # Standard HTTPS port to bypass firewalls
    https=True,   # Secure connection
    timeout=60    # Prevents the 'Timed out' error
)

os.environ["SENTENCE_TRANSFORMERS_HOME"] = "./model_cache"
model = SentenceTransformer('all-MiniLM-L6-v2') # Produces 384 dims
COLLECTION_NAME = "scholar_papers_v1"

def initialize_vector_db():
    try:
        collections = client.get_collections().collections
        if not any(c.name == COLLECTION_NAME for c in collections):
            client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE)
            )
            print("✅ Cloud Collection Ready!")
    except Exception as e:
        print(f"⚠️ Cloud Sync Warning: {e}")

initialize_vector_db()

def add_to_vector_store(paper_id, title, abstract, integrity_score):
    """
    Converts the paper into a vector and saves it to Qdrant Cloud.
    """
    # Use global COLLECTION_NAME
    
    # 1. Prepare the data
    text_to_embed = f"Title: {title}. Abstract: {abstract}"
    vector = model.encode(text_to_embed).tolist()
    
    # 2. Ensure paper_id is a valid Qdrant ID (UUID or Int)
    # We use uuid to create a unique mapping for string IDs
    if isinstance(paper_id, int):
        point_id = paper_id
    else:
        # Converts string ID to a valid UUID-based integer for Qdrant
        point_id = int(uuid.uuid5(uuid.NAMESPACE_DNS, str(paper_id)).int >> 96)

    # 3. Upsert to Cloud
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "original_id": str(paper_id),
                    "title": title, 
                    "abstract": abstract[:500], # Snippet for the UI
                    "integrity_score": float(integrity_score)
                }
            )
        ]
    )
    print(f"✅ Paper '{title}' (ID: {paper_id}) indexed in Qdrant Cloud.")

# Call this once at the end of the script to ensure the cloud is ready
initialize_vector_db()