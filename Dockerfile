FROM python:3.11.9-slim-bullseye AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential=12.9 \
    libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR $PYSETUP_PATH

FROM python:3.11.9-slim-bullseye AS runtime

ENV FASTAPI_ENV=production \
    PYTHONPATH=/app

COPY --from=builder /opt/pysetup/.venv /opt/pysetup/.venv
ENV PATH="/opt/pysetup/.venv/bin:$PATH"

RUN apt-get update && \
    apt-get install --no-install-recommends -y libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m app
RUN mkdir -p /app/logs && chown -R app:app /app/logs

WORKDIR /app
USER app

COPY --chown=app:app ./app ./app

CMD ["sh", "-c", "python ./app/main.py"]
