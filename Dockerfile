# Builder
FROM python:3.12-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock* ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY ./app ./app
COPY ./migrations ./migrations
COPY alembic.ini .
COPY entrypoint.sh .

RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app && \
    chmod +x /app/entrypoint.sh

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]