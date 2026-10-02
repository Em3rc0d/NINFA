FROM python:3.11-slim

ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cu124

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_PREFER_BINARY=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg git libsndfile1 build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN pip install --upgrade "pip>=25" "setuptools<81" wheel && \
    pip install --index-url "${TORCH_INDEX_URL}" \
      torch==2.6.0 torchaudio==2.6.0 && \
    pip install \
      "chatterbox-tts==0.1.7" \
      "gradio==6.8.0" \
      "numpy>=1.24,<2" \
      soundfile && \
    pip check

COPY app /workspace/app

EXPOSE 7860

CMD ["python", "/workspace/app/app.py"]
