# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (REQUIRED for psycopg2 and building extensions)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- STEP 1: BAKE MODELS ---
# Pre-download the model into the 'model_cache' directory (Matches your vector_service.py)
RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('./model_cache')"

# Copy all project files
COPY . .

# --- STEP 2: RUN THE SERVER ---
# We use 0.0.0.0 and the dynamic $PORT to satisfy Google Cloud Run's health check
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]