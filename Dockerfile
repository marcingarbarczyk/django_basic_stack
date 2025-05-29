FROM python:3.13-slim AS builder

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


COPY requirements/ /requirements

RUN pip install --upgrade pip && pip install  --no-cache-dir -r /requirements/requirements.txt


FROM python:3.13-slim

COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

COPY prod /prod
COPY dev /develop

RUN chmod +x /develop/web/entrypoint.sh && \
    chmod +x /develop/celery/entrypoint.sh && \
    chmod +x /prod/web/entrypoint.sh && \
    chmod +x /prod/cron_runner/entrypoint.sh && \
    chmod +x /prod/celery/entrypoint.sh

COPY / /app/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1