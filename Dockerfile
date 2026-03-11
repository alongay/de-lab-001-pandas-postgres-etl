FROM python:3.11-slim-bookworm

# Security: create non-root user
RUN useradd -m -u 10001 appuser

WORKDIR /app

# Install dependencies first (better layer caching)
RUN apt-get update && \
    apt-get install -y --no-install-recommends default-jre-headless && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy project (for container-only runs; we'll also bind-mount in compose)
COPY . /app

USER appuser

# Default (overridden per service in docker-compose)
CMD ["python", "-V"]
