# OmegaInfinity Codex Dockerfile
FROM python:3.11-slim

LABEL maintainer="Ricardo Jorge do Vale"
WORKDIR /codex

COPY ricardo_codex.py .
COPY requirements.txt .
COPY pyproject.toml .
COPY README.md .

RUN pip install --no-cache-dir .

ENTRYPOINT ["python3", "ricardo_codex.py"]