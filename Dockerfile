FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Pre-bake the model
RUN python3 -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2'); model.save('./model_cache')"
COPY . .
# Explicitly bind to 0.0.0.0 and Port 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]