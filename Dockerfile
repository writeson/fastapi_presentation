# Use Python 3.12 base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/project:$PYTHONPATH"

WORKDIR /project

# Create non-root user
RUN useradd -r -s /bin/false appuser && \
    mkdir -p /project && \
    mkdir -p /home/appuser/.cache && \
    chmod -R 777 /home/appuser/.cache && \
    chown -R appuser:appuser /project && \
    chown -R appuser:appuser /home/appuser

# Install dependencies
RUN pip install --no-cache-dir \
    uvicorn[standard] \
    httpx \
    aiosqlite \
    sqlmodel \
    fastapi

# Copy the project files
COPY --chown=appuser:appuser project/ ./

# Switch to non-root user
USER appuser

# Expose the port
EXPOSE 8000

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "4", "--loop", "uvloop", "--http", "httptools"]
