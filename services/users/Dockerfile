FROM python:3.11-slim

LABEL maintainer="etudianteB"
LABEL version="1.0"

WORKDIR /app

RUN useradd -m appuser

RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5001

HEALTHCHECK --interval=10s --timeout=5s --retries=5 CMD curl --fail http://localhost:5001/health || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "app:app"]