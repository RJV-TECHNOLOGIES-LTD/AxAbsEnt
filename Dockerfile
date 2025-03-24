# --------------------------------------
# AxAbsEnt: Multi-Stage Dockerfile
# --------------------------------------

# === Stage 1: Build Base ===
FROM python:3.11-slim as builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy source and install dependencies
COPY pyproject.toml requirements.txt setup.py ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# === Stage 2: Runtime ===
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY . .

# Default CMD: Uvicorn WSGI
CMD ["uvicorn", "api.wsgi:app", "--host", "0.0.0.0", "--port", "8000"]
