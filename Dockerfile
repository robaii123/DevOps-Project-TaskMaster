FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN adduser -D appuser && chown -R appuser /app

USER appuser

# Vérifie toutes les 30 secondes que l'application est en vie sur /health
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD [ "python", "app.py" ]

