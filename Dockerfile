# 1. Use a slim but capable Python image
FROM python:3.12-slim

# 2. Install essential system build tools for AI/DB libraries
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory
WORKDIR /app

# 4. Copy and install dependencies first (for faster caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your ScholarSense code
COPY . .

# 6. Inform Docker about the port
EXPOSE 8080

# 7. Start the API using the Cloud Run dynamic PORT variable
# Replace the old CMD with this exactly:
  CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]