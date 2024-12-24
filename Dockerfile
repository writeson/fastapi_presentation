# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set all environment variables together to reduce layers
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/project/app:$PYTHONPATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /project

# Create non-root user early
USER root
RUN useradd -r -s /bin/false appuser && \
    mkdir -p /project/.venv && \
    mkdir -p /home/appuser/.cache && \
    chmod -R 777 /home/appuser/.cache && \
    chown -R appuser:appuser /project && \
    chown -R appuser:appuser /home/appuser
    
# Copy only the files needed for dependency installation first
COPY --chown=appuser:appuser project/pyproject.toml project/uv.lock ./

# Switch to non-root user before installing dependencies
USER appuser

# Install dependencies without cache mounting
RUN uv sync --frozen --no-dev --no-cache

# Copy only the necessary application code
COPY --chown=appuser:appuser project/app ./app

# Expose the port (documentation purposes)
EXPOSE 8000

# Use exec form of CMD with specific uvicorn settings for better performance
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4", "--loop", "uvloop", "--http", "httptools"]
