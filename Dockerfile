# Stage 1: Builder
FROM python:3.11.9-slim-bullseye AS builder

# Set environment variables
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

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    curl \
    build-essential \
    libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11.9-slim-bullseye AS runtime

# Set environment variables
ENV PYTHONPATH=/app
ENV PATH="/opt/pysetup/.venv/bin:$PATH"

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create app user and directory
RUN useradd -m app
RUN mkdir -p /app/logs && chown -R app:app /app/logs

# Set working directory and user
WORKDIR /app
USER app

# Copy application code
COPY --chown=app:app ./app ./app

# Set command to run the application
CMD ["python", "./app/main.py"]
