# syntax=docker/dockerfile:1
# Release: docker build --target production -t app:prod .
# Default last stage is development (docker-compose.dev.yml uses target: development).

FROM python:3.12-slim AS production

ENV PYTHONUNBUFFERED=1 PYTHONPATH=/app TZ=Europe/Prague

RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Keep requirements separate so dependency layer stays cached when only app code changes.
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM production AS development

RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache \
    pip install --no-cache-dir -r requirements-dev.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
