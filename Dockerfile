# Stage 1: Builder
FROM python:3.11-slim AS builder

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Install only necessary build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install dependencies into a specific folder for easy copying
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Create a non-privileged user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copy only the installed site-packages from builder
COPY --from=builder /install /usr/local

# Copy application files
COPY src/ ./src/
COPY data/ ./data/

# Create output dir and set ownership
RUN mkdir output && chown appuser:appuser output

# Switch to non-root user
USER appuser

ENV PYTHONPATH=/app
ENV PATH="/usr/local/bin:$PATH"

CMD ["python", "src/main.py"]