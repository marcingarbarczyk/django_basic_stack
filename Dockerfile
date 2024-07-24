FROM python:3.12.2

RUN apt-get update && \
    apt-get install -y locales locales-all && \
    locale-gen pl_PL

COPY requirements/ /requirements

RUN pip install -r requirements/requirements.txt

COPY prod /prod
COPY dev /develop

RUN chmod +x /develop/web/entrypoint.sh && \
    chmod +x /develop/celery/entrypoint.sh && \
    chmod +x /prod/web/entrypoint.sh && \
    chmod +x /prod/cron_runner/entrypoint.sh && \
    chmod +x /prod/celery/entrypoint.sh

COPY / /app/

WORKDIR /app