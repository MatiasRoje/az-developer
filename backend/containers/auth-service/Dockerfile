FROM python:3.13-slim

WORKDIR /auth-service

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Keep the app directory structure (don't flatten)
COPY app/ ./app/

# Create non-root user for security (Security best practice)
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /auth-service
USER appuser

EXPOSE 8000

# Run using the module path
CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]