FROM python:3.11-slim

# Security: create non-root user
RUN useradd -m -u 10001 appuser

WORKDIR /app

# Install dependencies first (better layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy project (for container-only runs; we'll also bind-mount in compose)
COPY . /app

USER appuser

# Default (overridden per service in docker-compose)
CMD ["python", "-V"]
