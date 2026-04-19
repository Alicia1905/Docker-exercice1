FROM python:3.11-alpine

LABEL maintainer="you"
LABEL version="1.0"

RUN adduser -D appuser
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER appuser

EXPOSE 5002

HEALTHCHECK CMD wget --spider -q http://localhost:5000/health || exit 1

CMD ["python", "app.py"]