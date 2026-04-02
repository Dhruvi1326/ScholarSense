from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

# 1. Connect to Docker
client = QdrantClient("http://localhost:6333")
COLLECTION_NAME = "audited_papers"

# 2. Load the 'Brain' (The model that creates fingerprints)
# This will download a small (~400MB) file the first time you run it
model = SentenceTransformer('all-mpnet-base-v2')

def initialize_vector_db():
    """Sets up the collection for our academic vectors."""
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=768, # MPNet uses 768 dimensions for higher accuracy
                distance=Distance.COSINE
            ),
        )
        print(f"✅ Stable Collection '{COLLECTION_NAME}' is ready!")

def add_to_vector_store(paper_id, title, abstract, integrity_score):
    """Converts the paper into a vector and saves it."""
    text_to_embed = f"Title: {title}. Abstract: {abstract}"
    
    # Generate the fingerprint
    vector = model.encode(text_to_embed).tolist()
    
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=paper_id,
                vector=vector,
                payload={
                    "title": title,
                    "integrity_score": float(integrity_score)
                }
            )
        ]
    )
    print(f"🚀 Paper {paper_id} indexed in Semantic Memory.")