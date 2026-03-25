FROM python:3.11-slim

WORKDIR /app
ENV HF_HOME=/models/huggingface
ENV TRANSFORMERS_CACHE=/models/huggingface/transformers
ENV HF_HUB_DISABLE_SYMLINKS_WARNING=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . /app

# Pre-download heavy models at image build time to avoid first-request cold starts.
RUN python -m app.preload_models

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
