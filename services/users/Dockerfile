FROM python:3.11-slim

LABEL maintainer="etudianteB"
LABEL version="1.0"

WORKDIR /app

RUN useradd -m appuser

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5001

HEALTHCHECK CMD curl --fail http://localhost:5001/health || exit 1

CMD ["gunicorn","--bind","0.0.0.0:5001","app:app"]