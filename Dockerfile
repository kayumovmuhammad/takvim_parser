# syntax=docker/dockerfile:1.4

# --- Builder Stage ---
FROM python:3.12-slim AS builder

# Install uv (from official ghcr.io image)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files (pyproject.toml and optional uv.lock)
COPY pyproject.toml uv.lock ./

# Install dependencies into a virtual environment
RUN uv sync --frozen --no-cache

# Copy the application source code
COPY app ./app

# --- Runtime Stage ---
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy virtual environment and app code from the builder stage
COPY --from=builder /app /app

# Expose the port the app runs on
EXPOSE 80

# Command to run the application with Uvicorn (production server)
# The virtual environment executable is at /app/.venv/bin/uvicorn
CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
