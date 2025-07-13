# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster AS base

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Set workdir
WORKDIR /app

FROM base AS builder

# Install build dependencies (if any needed, e.g., gcc, for some pip packages)
# RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt only, using bind mount for cache and link for performance
COPY --link requirements.txt ./

# Create virtual environment and install dependencies using pip cache
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt

FROM base AS final

# Copy app source code (excluding .env and secrets via .dockerignore)
COPY --from=builder /app/.venv /app/.venv
COPY --link . .

# Set environment to use virtualenv
ENV PATH="/app/.venv/bin:$PATH"

# Create directory for uploaded files
RUN mkdir -p /app/uploaded_files && chown -R appuser:appgroup /app

# Expose the port
EXPOSE 8000

# Switch to non-root user
USER appuser

# Default command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
