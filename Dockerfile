# Dockerfile for FastAPI + Streamlit in separate images (use one at a time for dev)

FROM python:3.12-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 9090
ENV PYTHONPATH=/app
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "9090"]
