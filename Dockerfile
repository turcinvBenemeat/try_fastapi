FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends tzdata
ENV TZ=Europe/Prague

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

COPY app app
COPY src src
COPY main.py .
