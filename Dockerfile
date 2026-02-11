FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update \
  && apt-get install -y \
      gcc \
      git \
      postgresql-client \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r ./requirements.txt

FROM python:3.13-slim

WORKDIR /app

RUN useradd -m -u 1000 appuser

COPY --from=builder /usr/local /usr/local/

COPY . .

RUN chown -R appuser:appuser /app

USER appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

CMD ['gunicorn', 'config.wsgi:application', '-b', '0.0.0.0:8000', '-w', '4']
