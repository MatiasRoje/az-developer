FROM python:3.13-slim

WORKDIR /image-service

RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

RUN mkdir -p /tmp/image-processing

# Create non-root user for security (Security best practice)
RUN adduser --disabled-password --gecos "" appuser && \
    chown -R appuser:appuser /image-service
USER appuser

EXPOSE 8001

CMD ["sh", "-c", "uvicorn app.main:app --host ${HOST:-0.0.0.0} --port ${PORT:-8000}"]