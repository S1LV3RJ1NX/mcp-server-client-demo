FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.5.29 /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends

# Create non-root user - single layer
RUN addgroup --system --gid 999 appuser && \
    adduser --system --group --uid 999 --home /home/appuser appuser

# Set work directory and ownership once
WORKDIR /app
RUN chown appuser:appuser /app

# Create and set permissions for UV cache directory
RUN mkdir -p /tmp/uv && \
    chmod -R 777 /tmp && \
    chown -R appuser:appuser /tmp/uv

# Copy only pyproject.toml first for better caching
COPY --chown=appuser:appuser pyproject.toml .
COPY --chown=appuser:appuser uv.lock .

# Create venv and install dependencies - combined into single layer
RUN python -m venv /app/.venv && \
    chown -R appuser:appuser /app/.venv && \
    chmod -R 755 /app/.venv && \
    chmod -R 777 /app/.venv/lib/python3.12/site-packages && \
    . /app/.venv/bin/activate && \
    uv sync --frozen --no-cache

# Create cache directory with permissions
RUN mkdir -p /app/cache && \
    chown -R appuser:appuser /app/cache && \
    chmod -R 777 /app/cache

# Copy the application code with correct ownership
COPY --chown=appuser:appuser . .

# Switch to non-root user
USER appuser

RUN rm -rf /tmp/*

ENV HOME=/home/appuser \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app:$PYTHONPATH"
