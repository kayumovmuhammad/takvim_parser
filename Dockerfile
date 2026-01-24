FROM python:3.12-slim AS builder


COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    
RUN apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb && \
    apt-get clean

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-cache

COPY app ./app
COPY chromedriver ./chromedriver

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /app /app

EXPOSE 80

CMD ["/app/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
