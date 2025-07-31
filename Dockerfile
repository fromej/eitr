FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apk add --no-cache supervisor

COPY pyproject.toml .

RUN uv sync

COPY foodfetcher .

RUN .venv/bin/python manage.py collectstatic --noinput

RUN .venv/bin/python manage.py migrate

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]