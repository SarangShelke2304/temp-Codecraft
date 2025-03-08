

FROM python:3.11.9-slim-bullseye

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install dependencies
RUN apt-get update && \
    apt-get install --no-install-recommends -y \
    libmagic1 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
ENV PATH="/opt/pysetup/.venv/bin:$PATH"
# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create app user and directory
RUN useradd -m app
RUN mkdir -p /app/logs && chown -R app:app /app/logs

# Set working directory and user
WORKDIR /app
USER app

# Copy application code
COPY --chown=app:app ./app ./app

# Set command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]